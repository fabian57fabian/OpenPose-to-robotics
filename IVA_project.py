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
params["alpha_pose"] = 1
# enable this to save data to json
# params["write_json"] = "IVA_pose_estimation_results"

# Front direction min and max angle
min_angle_front = -3
max_angle_front = 3

# Steering direction. Change to flip directions
FLIP_STEER = False

# Optimization for steer and speed.
# Higher means safer but much more noise-affected
SPEED_MAX_VARIATION = 150
STEER_MAX_VARIATION = 90

right_UI_status_X = 520

# Colors for steering line
steer_front = (0, 255, 0)
steer_right = (255, 0, 0)
steer_left = (255, 0, 0)


class VarNoList:

    def __init__(self):
        self.value = 0

    def append(self, val):
        self.value = val

    def __getitem__(self, count):
        return self.value

    def __len__(self):
        return 1


###Global using vars
# Wirsts keypoints arrays
RightWirst_x = VarNoList()  # []
RightWirst_y = VarNoList()  # []
LeftWirst_x = VarNoList()  # []
LeftWirst_y = VarNoList()  # []

# Appending first wirsts keypoints
RightWirst_x.append(0.0)
RightWirst_y.append(0.0)
LeftWirst_x.append(0.0)
LeftWirst_y.append(0.0)

# Max y speed on CAM, (MAX value = 380)
MAX_SPEED_Y = 200
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

# Counter for errors in body. 1 means fps count. 0.5 means a half of fps count....
MAX_OP_MULTIPLIER = .8

# moving average filter parameter
# alpha regulates the update speed (how fast the accumulator “forgets” about earlier images)
alpha = 0.8


def main():
    global speed, steeringAngle, status, last_status, selected_direction, RightWirst_y, RightWirst_x, LeftWirst_y, LeftWirst_x, carSerial, accelerations, steering_angles, alpha,MAX_OP_MULTIPLIER
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
    cv2.namedWindow('OPtoROBO', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('OPtoROBO', 1000, 750)
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

    error_op_counter = 0

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

        # Bilateral Filtering
        img = cv2.bilateralFilter(img, 9, 40, 75)

        datum = op.Datum()
        datum.cvInputData = img
        opWrapper.emplaceAndPop([datum])

        # Detecting people control
        if (not datumChecks(datum.poseKeypoints) or str(datum.poseKeypoints) == str(2.0) or str(
                datum.poseKeypoints) == str(0.0)
                or str(datum.poseKeypoints) == str(1e-45)):
            print('NO DETECTED PEOPLE, YOU SHOULD GO IN FRONT OF YOUR WEBCAM')
            # time.sleep(.5)
            error_op_counter += 1
            if error_op_counter > (int(fps / MAX_OP_MULTIPLIER)):
                RightWirst_x.append(400.0)
                RightWirst_y.append(440.0)
                LeftWirst_x.append(250.0)
                LeftWirst_y.append(440.0)
            else:
                RightWirst_x.append(RightWirst_x[len(RightWirst_y) - 1])
                RightWirst_y.append(RightWirst_y[len(RightWirst_y) - 1])
                LeftWirst_x.append(LeftWirst_x[len(LeftWirst_x) - 1])
                LeftWirst_y.append(LeftWirst_x[len(LeftWirst_x) - 1])
        else:
            error_op_counter = 0
            try:
                RightWirst_x.append(datum.poseKeypoints[0][7][0])
                RightWirst_y.append(datum.poseKeypoints[0][7][1])
                LeftWirst_x.append(datum.poseKeypoints[0][4][0])
                LeftWirst_y.append(datum.poseKeypoints[0][4][1])
            except Exception as e1:
                print(e1)
                c = 0

        steeringAngle = steering_angle(LeftWirst_x[counter], -LeftWirst_y[counter],
                                       RightWirst_x[counter], -RightWirst_y[counter])

        # Direction and Stop
        # if both hands up
        if (LeftWirst_y[counter] < 380 or RightWirst_y[counter] < 380) and selected_direction != 0:
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
        # if last_status == 1 and status == 0:
        #    selected_direction = 0

        # Gestures detection
        if status == 1:
            speed = int(speed_value(RightWirst_y[counter], LeftWirst_y[counter]))
            if speed < 0:
                speed = 0
            if (min_angle_front < steeringAngle < max_angle_front and RightWirst_y[counter] < 380.0 and LeftWirst_y[
                counter] < 380.0):
                print('----FRONT----. STATUspeedMS: ', status_to_str(), '. SPEED:  ', speed, '. ANGLE: ', 0)
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

        # Stop Line
        cv2.line(img2, (160, 380), (480, 380), (0, 0, 255), thickness=3)
        cv2.putText(img2, 'STOP', (260, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), thickness=2)
        cv2.putText(img2, 'B', (65, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), thickness=2)
        cv2.putText(img2, 'F', (545, 420), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 0, 0), thickness=2)
        # Show speedometer
        cv2.putText(img2, "SPD: " + str(speed), (right_UI_status_X, 30), cv2.FONT_HERSHEY_TRIPLEX, .5, (0, 0, 0),
                    thickness=2)
        # Show Speed ui
        cv2.rectangle(img2, (610, (370 - speed)), (630, 370), (0, 255, 0), thickness=-2)
        # Show steerAngle
        cv2.putText(img2, "STR: " + str(int(steeringAngle)), (right_UI_status_X, 60), cv2.FONT_HERSHEY_TRIPLEX, .5,
                    (0, 0, 0),
                    thickness=2)
        # Show Fps
        cv2.putText(img2, "FPS: " + str(round(fps, 1)), (right_UI_status_X, 90), cv2.FONT_HERSHEY_TRIPLEX, .5,
                    (0, 0, 0),
                    thickness=2)
        # Show Mode
        if status == 0:
            cv2.putText(img2, 'STOP MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), thickness=2)
            if selected_direction == 1:
                cv2.putText(img2, 'BACKWARD', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img2, 'FORWARD', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        elif status == 1:
            cv2.putText(img2, 'GO MODE', (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            if selected_direction == 1:
                cv2.putText(img2, 'BACKWARD', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
            elif selected_direction == 2:
                cv2.putText(img2, 'FORWARD', (170, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 0, 0), thickness=2)
        # Quitting progress bar
        if quit_count != 0:
            cv2.putText(img2, ' Quitting...', (10, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), thickness=2)
            cv2.rectangle(img2, (22, 70), (122, 90), (0, 255, 0), thickness=-2)
            cv2.rectangle(img2, (22 + 5 * quit_count, 70), (122, 90), (255, 255, 255), thickness=-2)

        # Backward/Forward zones
        cv2.rectangle(img2, (0, 380), (160, 480), (0, 255, 0), thickness=2)
        cv2.rectangle(img2, (480, 380), (640, 480), (255, 0, 0), thickness=2)

        img2 = imshow_img(img2, avg, alpha)

        cv2.imshow('OPtoROBO', img2)

        if speed >= 370:
            c = 0

        counter = counter + 1
        last_status = status

        # Quit gesture
        try:
            if (380 < LeftWirst_y[counter] < 480 and 0 < LeftWirst_x[counter] < 160
                    and 380 < RightWirst_y[counter] < 480 and 480 < RightWirst_x[counter] < 640):
                cv2.rectangle(img, (160, 400), (480, 420), (0, 255, 0), thickness=2)
                quit_count = quit_count + 1
                if quit_count > 21:
                    break
            else:
                quit_count = 0
        except Exception as e1:
            print(e1)
            c = 0

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
    average_wirsts = (y1 + y2) / 2
    average_wirsts -= 10
    if average_wirsts < 0:
        average_wirsts = 0
    speed = 370 - average_wirsts
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
            carSerial.SetSpeed(int(speed / (MAX_SPEED_Y / 100)))
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


def imshow_img(img, avg, alpha):
    if args.moving_average_filter:
        cv2.accumulateWeighted(img, avg, alpha)
        res = cv2.convertScaleAbs(avg)
        return res
    else:
        return img


def datumChecks(keypoints):
    try:
        if keypoints is None:
            return False
        if keypoints.shape is None:
            return False
        if len(keypoints.shape) == 0:
            return False
        if keypoints.shape[0] < 1:
            return False
        if keypoints.shape[1] < 8:
            return False
        if keypoints[0][7][0] == 0.0 and keypoints[0][7][1] == 00.0 or keypoints[0][4][0] == 00.0 and keypoints[0][4][
            1] == 00.0:
            return False
        return True
    except Exception as ee:
        print(ee)
        c = 0


if __name__ == "__main__":
    # rimesso apposto il main
    # metto un commento
    main()
    try:
        ProcessAnalytics(accelerations, no_opt_accelerations, steering_angles, no_opt_steering_angles, args)
    except Exception as e:
        print(e)
        sys.exit(-1)
