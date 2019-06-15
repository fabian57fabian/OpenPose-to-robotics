#!/usr/bin/python
import serial
import syslog
import time
import sys
import glob
import time


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class ArduinoConnector:
    defaultPort = '/dev/ttyUSB1'

    def __init__(self, port=defaultPort):
        self.baudrate = 9600
        self.port = port
        self.arduino = None
        self.initialized = False

    """
    Takes the given string and sends it thru serial
    """

    def write(self, string):
        if self.initialized:
            self.arduino.write(string)

    def initialize(self):
        self.arduino = serial.Serial(self.port, self.baudrate)
        time.sleep(2)
        self.initialized = True
