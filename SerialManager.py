from ArduinoComunication import ArduinoConnector
import syslog
import time
import sys
import glob
import time
import serial

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

def ConnectToSerial():
    ports = serial_ports()
    if ports == None or len(ports) == 0:
        print('Unable to find available ports')
        exit()
    port = choosePort(ports)
    connector = ArduinoConnector(port)
    print('Initializing serial port...')
    connector.initialize()
    return connector


def choosePort(ports):
    exit = False
    selected_index = 0
    while not exit:
        for i, p in enumerate(ports):
            print('Port ' + str(i) + ": " + str(p))
        number = input("Choose the port (type number): ")
        try:
            selected_index = int(number)
            if 0 <= selected_index < len(ports):
                exit = True
        except ValueError:
            pass
    return ports[selected_index]