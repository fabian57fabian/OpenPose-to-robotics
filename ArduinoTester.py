from ArduinoComunication import ArduinoConnector
from ArduinoComunication import serial_ports
from SerialManager import ConnectToSerial
import time


def main():
    carSerial = ConnectToSerial()
    _continue = True
    # say_hi(connector)
    # test1(connector)
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
        carSerial.writeChar(data)
    exit()


def test1(connector):
    connector.writeString('100170055')
    time.sleep(.5)
    connector.writeString('105170055')
    time.sleep(.5)
    connector.writeString('110170055')
    time.sleep(.5)
    connector.writeString('115170055')
    time.sleep(.5)
    connector.writeString('120170055')
    time.sleep(.5)
    connector.writeString('125170055')
    time.sleep(.5)
    connector.writeString('130170055')
    time.sleep(.5)


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




if __name__ == "__main__":
    main()
