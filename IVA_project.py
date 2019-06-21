#!/usr/bin/python
import cv2
import sys
from sys import *
import math
import os
import time
from SerialManager import ConnectToSerial

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

###Params that can be changed
# Parameters OpenPose
params = dict()
params["model_folder"] = "../../../models/"
params["number_people_max"] = 1
params["body"] = 1
params["alpha_pose"] = 1
# enable this to save data to json
# params["write_json"] = "IVA_pose_estimation_results"

# Front direction min and max angle
min_angle_front = -3
max_angle_front = 3

# Colors for steering line
steer_front = (0, 255, 0)
steer_right = (255, 0, 0)
steer_left = (255, 0, 0)

###Global using vars
# Wirsts keypoints arrays
RightWirst_x = []
RightWirst_y = []
LeftWirst_x = []
LeftWirst_y = []

# Appending first wirsts keypoints
RightWirst_x.append(0.0)
RightWirst_y.append(0.0)
LeftWirst_x.append(0.0)
LeftWirst_y.append(0.0)

# Car state: 0 (stop), 1 (backward), 2 (forward) (INT)
status = 0
# Steering Angle
steeringAngle = 0.0
# Speed
speed = 0


def main():
    global speed, steeringAngle, status, RightWirst_y, RightWirst_x, LeftWirst_y, LeftWirst_x
    # Starting serial bluetooth connection
    carSerial = ConnectToSerial()
    if carSerial is None:
        print("No port selected, exiting...")
        sys.exit(-2)

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Start webcam with VideoCapture. 0 -> use default webcam
    # WINDOWS_NORMAL dynamic window resize at running time
    # resizeWindow output windows webcam dimension. RESOLUTION -> 4:3
    cv2.namedWindow('DETECTED KEYPOINTS', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('DETECTED KEYPOINTS', 1000, 750)
    stream = cv2.VideoCapture(0)

    # Frame counter
    counter = 0
    # Execution time
    start = time.time()
    fps = 0.0
    fps_last_time = time.time()
    fps_last_counter = counter

    while True:
        # Update fps
        if counter % 5 == 0:
            fps = (counter - fps_last_counter) / (time.time() - fps_last_time)
            fps_last_time = time.time()
            fps_last_counter = counter

        # Frame reader. Each frame will be processed by OpenPose
        ret, img = stream.read()
        # Output flip
        cv2.flip(img, 1, img)
        # Stop Line
        cv2.line(img, (160, 380), (480, 380), (0, 0, 255), thickness=3)
        cv2.putText(img, 'STOP', (260, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), thickness=2)
        cv2.putText(img, 'B', (65, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), thickness=2)
        cv2.putText(img, 'F', (545, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 0, 0), thickness=2)
        # Show speedometer
        cv2.putText(img, "SPD: " + str(speed), (540, 30), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 0), thickness=2)
        # Show steerAngle
        cv2.putText(img, "STR: " + str(round(steeringAngle, 1)), (540, 60), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 0),
                    thickness=2)
        # Show Fps
        cv2.putText(img, "FPS: " + str(round(fps, 1)), (540, 90), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 0), thickness=2)
        # show Mode
        if status == 0:
            cv2.putText(img, 'STOP MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), thickness=2)
        if status == 1:
            cv2.putText(img, 'BACKWARD MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
        if status == 2:
            cv2.putText(img, 'FORWARD MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)

        # Backward/Forward zones
        cv2.rectangle(img, (0, 380), (160, 480), (0, 255, 0), thickness=2)
        cv2.rectangle(img, (480, 380), (640, 480), (255, 0, 0), thickness=2)

        # Show line between hands
        steer_color = steer_front
        if steeringAngle < min_angle_front:
            steer_color = steer_left
        if steeringAngle > max_angle_front:
            steer_color = steer_right
        if not RightWirst_x[counter] == 0 and not LeftWirst_x[counter] == 0:
            cv2.line(img, pt1=(int(RightWirst_x[counter]), int(RightWirst_y[counter])),
                     pt2=(int(LeftWirst_x[counter]), int(LeftWirst_y[counter])), color=steer_color, thickness=5)
        """Removed frame saving to file, better performances
        # Frame writer"
        cv2.imwrite("frame.png", img)

        # Frame processor by OpenPose (datum class)
        datum = op.Datum()
        #imageToProcess = cv2.imread("frame.png")
        datum.cvInputData = imageToProcess
        """
        datum = op.Datum()
        datum.cvInputData = img
        opWrapper.emplaceAndPop([datum])

        # Detecting people control
        if (str(datum.poseKeypoints) == str(2.0) or str(datum.poseKeypoints) == str(0.0)
                or str(datum.poseKeypoints) == str(1e-45)):
            print('NO DETECTED PEOPLE, YOU SHOULD GO IN FRONT OF YOUR WEBCAM')
            time.sleep(2)

            RightWirst_x.append(0.0)
            RightWirst_y.append(0.0)
            LeftWirst_x.append(0.0)
            LeftWirst_y.append(0.0)

        else:
            RightWirst_x.append(datum.poseKeypoints[0][7][0])
            RightWirst_y.append(datum.poseKeypoints[0][7][1])
            LeftWirst_x.append(datum.poseKeypoints[0][4][0])
            LeftWirst_y.append(datum.poseKeypoints[0][4][1])

        steeringAngle = steering_angle(LeftWirst_x[counter], -LeftWirst_y[counter],
                                       RightWirst_x[counter], -RightWirst_y[counter])

        # Direction and Stop
        if ((status == 0 and 380 < LeftWirst_y[counter] < 480 and 0 < LeftWirst_x[counter] < 160)
                and RightWirst_y[counter] > 380):
            status = 1
            carSerial.Backward()
            print('<-------BACKWARD', status)
        else:
            if (status == 0 and 380 < RightWirst_y[counter] < 480 and 480 < RightWirst_x[counter] < 640
                    and LeftWirst_y[counter] > 380):
                status = 2
                carSerial.Forward()
                print('FORWARD-------->', status)
            else:
                if (((LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] > 380.0) or (
                        LeftWirst_y[counter] == 0.0
                        and RightWirst_y[
                            counter] == 0.0) or (
                             LeftWirst_y[counter] == 0.0 and RightWirst_y[counter] > 380.0)
                     or (LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] == 0.0))
                        and (160 < LeftWirst_x[counter] < 640 and 0 < RightWirst_x[counter] < 480)
                        or (LeftWirst_x[counter] == 0.0 and RightWirst_x[counter] == 0.0)):
                    speed = 0
                    status = 0
                    print('------STOP------', status)
                    carSerial.Stop()

        # Gestures detection
        if (status != 0 and min_angle_front < steeringAngle < max_angle_front
                and RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0):
            speed = int(speed_value(RightWirst_y[counter], LeftWirst_y[counter]))
            print('----FRONT----. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ', 0)
            sendSpeed(carSerial, speed)
        else:
            if (status != 0 and max_angle_front < steeringAngle < 90.0
                    and RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0):
                speed = int(speed_value(RightWirst_y[counter], LeftWirst_y[counter]))
                print('LEFT---------. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                      round(steeringAngle, 2))
                sendSpeed(carSerial, speed)
                carSerial.Steer(- steeringAngle)
            else:
                if (status != 0 and -90.0 < steeringAngle < min_angle_front
                        and RightWirst_y[counter] < 380.0 and LeftWirst_y[counter] < 380.0):
                    speed = int(speed_value(RightWirst_y[counter], LeftWirst_y[counter]))
                    print('--------RIGHT. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                          round(steeringAngle, 2))
                    sendSpeed(carSerial, speed)
                    carSerial.Steer(- steeringAngle)

        # Output with OpenPose skeleton
        cv2.imshow('DETECTED KEYPOINTS', datum.cvOutputData)
        counter = counter + 1

        # q, Q == quit, STOP SCRIPT; NB: waitKey MUST BE 1
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break

    end = time.time()
    # Resources release
    stream.release()
    cv2.destroyAllWindows()
    total_time = end - start

    # Time and fps
    print(
        '-----------------------------------------------------------------------------------------------------------')
    print('Total script execution time : ', total_time)
    print('FPS: ', counter / total_time)
    print(
        '-----------------------------------------------------------------------------------------------------------')


# Utils
def status_to_str():
    global status
    if status == 0:
        return "STOP"
    if status == 1:
        return "BACKWARD"
    if status == 2:
        return "FORWARD"
    return "UNKNOWN"


# Steering functions
def steering_angle(x1, y1, x2, y2):
    if (x2 - x1 == 0):
        angle = 0.0
    else:
        m = (y2 - y1) / (x2 - x1)
        angle = math.degrees(math.atan(m))
    return angle


def speed_value(y1, y2):
    speed = 380 - (y1 + y2) / 2
    return speed


# Commands to Controller
def sendSpeed(serial, speed):
    if speed > 200:
        serial.SetSpeed(100)
    else:
        serial.SetSpeed(int(speed / 2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(-1)
