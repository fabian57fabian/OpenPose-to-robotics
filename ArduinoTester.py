from ArduinoComunication import ArduinoConnector
from ArduinoComunication import serial_ports
import time


def main():
    ports = serial_ports()
    if ports == None or len(ports) == 0:
        print('Unable to find available ports')
        exit()
    port = choosePort(ports)
    connector = ArduinoConnector(port)
    print('Initializing serial port...')
    connector.initialize()
    _continue = True
    say_hi(connector)
    while (_continue):
        """
        data = input("Write the angle(°) to send: ")
        try:
            angle = int(data)
            if angle == -1:
                _continue = False
            else:
                if 0 <= angle <= 180:
                    connector.writeAngle(data)
        except ValueError:
            print("This is not an integer value.")
        """
        print("Format: 'XXXYYYZZZ' where XXX is X angle, YYY is Y angle, ZZZ is z angle (if <100 add zeros)")
        data = input("Write data to send")
        connector.writeString(data)
    exit()


def say_hi(connector):
    print("Sending hi command")
    connector.writeString('100170055')
    time.sleep(3)
    connector.writeString('150010060')
    time.sleep(2)
    connector.writeString('150010030')
    time.sleep(1)
    connector.writeString('150010060')
    time.sleep(1)
    connector.writeString('150010030')
    time.sleep(1)
    connector.writeString('150010060')
    time.sleep(2)
    connector.writeString('100170055')


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


if __name__ == "__main__":
    main()
