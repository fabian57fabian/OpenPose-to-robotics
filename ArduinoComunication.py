#!/usr/bin/python
import serial
import time


class ArduinoConnector:
    defaultPort = '/dev/ttyUSB1'

    def __init__(self, port=defaultPort):
        self.baudrate = 38400
        self.port = port
        self.arduino = None
        self.initialized = False
        self.last_speed = self.last_steer = self.last_direction = chr(126)

    """
    Takes the given cahr and sends it thru serial
    """

    def writeChar(self, char):
        if self.initialized:
            self.arduino.write(char.encode())
            print("Sent '" + char + "'")

    """
    Takes a speed in range [0,100] and sends it
    """

    def SetSpeed(self, speed):
        if speed is not None:
            # print("Try to SET SPEED " + str(speed))
            sp = chr(int(self.map(speed, 0, 100, 48, 57)))
            if not sp == self.last_speed:
                self.last_speed = sp
                self.writeChar(sp)

    def Stop(self):
        if not self.last_direction == 'S':
            self.last_direction = 'S'
            self.writeChar('S')
            self.SetSpeed(0)

    def Forward(self):
        if not self.last_direction == 'F':
            self.last_direction = 'F'
            self.writeChar('F')

    def Backward(self):
        if not self.last_direction == 'B':
            self.last_direction = 'B'
            self.writeChar('B')

    """
        Takes a steer value in range [-90,90] and sends it correctly
    """

    def Steer(self, angle):
        print("Try to STEER " + str(angle))
        grades = int(angle)
        final_command = '.'
        if -90 <= grades < -50:
            final_command = 'L'
        elif -50 <= grades <= 50:
            val = int(grades) + 50
            print("Steering " + str(val) + " from [0,100]")
            converted_angle = int(self.map(grades + 50, 0, 100, 97, 122))
            print("Converted char: " + str(converted_angle))
            final_command = chr(converted_angle)
        elif 50 < grades <= 90:
            final_command = 'R'
        else:
            print("Angle not right:" + str(angle))
            return

        if not self.last_steer == final_command:
            self.last_steer = final_command
            self.writeChar(final_command)

    def initialize(self):
        self.arduino = serial.Serial(self.port, self.baudrate)
        time.sleep(2)
        self.initialized = True

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
