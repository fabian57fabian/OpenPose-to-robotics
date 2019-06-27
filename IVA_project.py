#!/usr/bin/python
import os
import sys
import time
from sys import *
import numpy as np
import cv2
import math
from SerialManager import ConnectToSerial
from Utils import parseArgs
from analytics import ProcessAnalytics

sendCommandsToCar, source, args = parseArgs()

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python')
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
params["alpha_pose"] = 0
# enable this to save data to json
# params["write_json"] = "IVA_pose_estimation_results"

# Front direction min and max angle
min_angle_front = -3
max_angle_front = 3

# Steering direction. Change to flip directions
FLIP_STEER = True

# Optimization for steer and speed.
# Higher means safer but much more noise-affected
SPEED_MAX_VARIATION = 150
STEER_MAX_VARIATION = 90

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

# Max y speed on CAM, (MAX value = 380)
MAX_SPEED_Y = 150
# Car state: 0 (stop), 1 (go) (INT)
status = 0
last_status = 0
# Car selected direction: 1 (backward), 2 (forward) (INT)
selected_direction = 0
# Steering Angle
steeringAngle = 0.0
_last_angle = 0.0
# Speed
speed = 0
last_speed = 0
# Car connector
carSerial = None

# Analytics vars
accelerations = []
no_opt_accelerations = []
steering_angles = []
no_opt_steering_angles = []


def main():
    global speed, steeringAngle, status, last_status, selected_direction, RightWirst_y, RightWirst_x, LeftWirst_y, LeftWirst_x, carSerial, accelerations, steering_angles
    # Starting serial bluetooth connection
    if sendCommandsToCar:
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
    # resizeWindow output windows webcam dimension. RESOLUSpeedsTION -> 4:3
    cv2.namedWindow('DETECTED KEYPOINTS', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('DETECTED KEYPOINTS', 1000, 750)
    stream = cv2.VideoCapture(source)
    time.sleep(2)
    if stream is None:
        print("No stream at " + str(source))
        sys.exit(-3)
    if not stream.isOpened():
        print("Stream at " + str(source) + " unvailable. Unable to open.")
        sys.exit(-4)

    # Frame counter
    counter = 0
    # Execution time
    start = time.time()
    fps = 0.0
    fps_last_time = time.time() - 1000
    fps_last_counter = counter - 1
    quit_count = 0

    # moving average filter
    ret, img = stream.read()
    avg = np.float32(img)


    while True:
        # Update fps
        if counter % 5 == 1:
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
        # Show Mode
        if status == 0:
            cv2.putText(img, 'STOP MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), thickness=2)
            if selected_direction == 1:
                cv2.putText(img, 'B selected', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img, 'F selected', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        elif status == 1 :
            cv2.putText(img, 'GO MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            if selected_direction == 1:
                cv2.putText(img, 'B selected', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img, 'F selected', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        # Quitting progress bar
        if quit_count != 0:
            cv2.putText(img, ' Quitting...', (10, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            cv2.rectangle(img, (22, 70), (122, 90), (0, 255, 0), thickness=-2)
            cv2.rectangle(img, (22 + 5 * quit_count, 70), (122, 90), (255, 255, 255), thickness=-2)

        # Backward/Forward zones
        cv2.rectangle(img, (0, 380), (160, 480), (0, 255, 0), thickness=2)
        cv2.rectangle(img, (480, 380), (640, 480), (255, 0, 0), thickness=2)

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
        # if both hands up
        if LeftWirst_y[counter] < 380 and RightWirst_y[counter] < 380 and selected_direction != 0:
            # Go time
            status = 1
        else:
            # if one or both hands down into command part
            status = 0
            Stop()
            if (380 < LeftWirst_y[counter] < 480 and 0 < LeftWirst_x[counter] < 160
                    and RightWirst_y[counter] > 380):
                selected_direction = 1
                print('<-------BACKWARD', status)
            elif (380 < RightWirst_y[counter] < 480 and 480 < RightWirst_x[counter] < 640
                  and LeftWirst_y[counter] > 380):
                selected_direction = 2
                print('FORWARD-------->', status)
            elif (((LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] > 380.0) or (
                    LeftWirst_y[counter] == 0.0
                    and RightWirst_y[
                        counter] == 0.0) or
                   (LeftWirst_y[counter] == 0.0 and RightWirst_y[counter] > 380.0)
                   or (LeftWirst_y[counter] > 380.0 and RightWirst_y[counter] == 0.0))
                  and (160 < LeftWirst_x[counter] < 640 and 0 < RightWirst_x[counter] < 480)
                  or (LeftWirst_x[counter] == 0.0 and RightWirst_x[counter] == 0.0)):
                speed = 0
                Stop()
                print('------STOP------', status)

        # If we just exited from stop zone, a Forward of Backward call is needed
        if status == 1 and last_status == 0:
            if selected_direction == 1:
                Backward()
            elif selected_direction == 2:
                Forward()
        if last_status == 1 and status == 0:
            selected_direction = 0

        # Gestures detection
        if status == 1:
            speed = int(speed_value(RightWirst_y[counter], LeftWirst_y[counter]))
            if (min_angle_front < steeringAngle < max_angle_front and RightWirst_y[counter] < 380.0 and LeftWirst_y[
                counter] < 380.0):
                print('----FRONT----. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ', 0)
                sendSpeed()
            else:
                if (max_angle_front < steeringAngle < 90.0 and RightWirst_y[counter] < 380.0
                        and LeftWirst_y[counter] < 380.0):

                    print('LEFT---------. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                          round(steeringAngle, 2))
                    sendSpeed()
                    if FLIP_STEER:
                        steeringAngle = -steeringAngle
                    Steer()
                else:
                    if (-90.0 < steeringAngle < min_angle_front and RightWirst_y[counter] < 380.0
                            and LeftWirst_y[counter] < 380.0):

                        print('--------RIGHT. STATUS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ',
                              round(steeringAngle, 2))
                        sendSpeed()
                        if FLIP_STEER:
                            steeringAngle = -steeringAngle
                        Steer()

        # Output with OpenPose skeleton
        img2 = datum.cvOutputData
        # Show line between hands
        steer_color = steer_front
        if steeringAngle < min_angle_front:
            steer_color = steer_left
        if steeringAngle > max_angle_front:
            steer_color = steer_right
        if not RightWirst_x[counter] == 0 and not LeftWirst_x[counter] == 0:
            cv2.line(img2, pt1=(int(RightWirst_x[counter]), int(RightWirst_y[counter])),
                     pt2=(int(LeftWirst_x[counter]), int(LeftWirst_y[counter])), color=steer_color, thickness=5)

        if args.moving_average_filter:
            img2 = moving_average_filter(img2, avg, 0.1)

        cv2.imshow('DETECTED KEYPOINTS', img2)
        counter = counter + 1
        last_status = status

        # Quit gesture
        if (380 < LeftWirst_y[counter] < 480 and 0 < LeftWirst_x[counter] < 160
                and 380 < RightWirst_y[counter] < 480 and 480 < RightWirst_x[counter] < 640):
            cv2.rectangle(img, (160, 400), (480, 420), (0, 255, 0), thickness=2)
            quit_count = quit_count + 1
            if quit_count > 21:
                break
        else:
            quit_count = 0

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
def sendSpeed():
    global last_speed, speed, MAX_SPEED_Y
    if args.compute_analytics:
        no_opt_accelerations.append(speed)
    optimize_speed()
    if sendCommandsToCar:
        if speed > MAX_SPEED_Y:
            carSerial.SetSpeed(100)
        else:
            carSerial.SetSpeed(int(speed / (MAX_SPEED_Y/100)))
    last_speed = speed
    if args.compute_analytics:
        accelerations.append(speed)


def optimize_speed():
    global speed, last_speed, SPEED_MAX_VARIATION
    if args.unoptimized_speed:
        return
    if abs(last_speed - speed) > SPEED_MAX_VARIATION:
        speed = last_speed


def Backward():
    if sendCommandsToCar:
        carSerial.Backward()


def Forward():
    if sendCommandsToCar:
        carSerial.Forward()


def Stop():
    if sendCommandsToCar:
        carSerial.Stop()


def Steer():
    global _last_angle, steeringAngle
    if args.compute_analytics:
        no_opt_steering_angles.append(steeringAngle)
    optimize_steering()
    if sendCommandsToCar:
        carSerial.Steer(steeringAngle)
    _last_angle = steeringAngle
    if args.compute_analytics:
        steering_angles.append(steeringAngle)


def optimize_steering():
    global steeringAngle, _last_angle, STEER_MAX_VARIATION
    if args.unoptimized_steer:
        return
    if abs(_last_angle - steeringAngle) > STEER_MAX_VARIATION:
        steeringAngle = _last_angle

def moving_average_filter(img, avg, alpha):
    # alpha regulates the update speed (how fast the accumulator “forgets” about earlier images)
        cv2.accumulateWeighted(img, avg, alpha)
        res = cv2.convertScaleAbs(avg)
        return res

if __name__ == "__main__":
    # rimesso apposto il main
    # metto un commento
    try:
        main()
        ProcessAnalytics(accelerations, no_opt_accelerations, steering_angles, no_opt_steering_angles, args)
    except Exception as e:
        print(e)
        sys.exit(-1)
