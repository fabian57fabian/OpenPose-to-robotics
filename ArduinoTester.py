from ArduinoComunication import ArduinoConnector
from ArduinoComunication import serial_ports


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
    while (_continue):
        data = input("Write the angle(°) to send: ")
        try:
            angle = int(data)
            if angle == -1:
                _continue = False
            connector.writeAngle(data)
        except ValueError:
            print("This is not an integer value.")
    exit()


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
