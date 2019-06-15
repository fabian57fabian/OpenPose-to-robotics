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
    print("Sending some bytes...")
    connector.write(b'abcdefg')

    print("All bytes sent")
    exit()


def choosePort(ports):
    exit = False
    selected_index = 0
    while not exit:
        for i, p in enumerate(ports):
            print('Port '+str(i)+": " + str(p))
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
