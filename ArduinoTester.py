from ArduinoComunication import ArduinoConnector
from ArduinoComunication import serial_ports


def main():
    ports = serial_ports()
    print('Available ports:' + str(ports))
    if ports == None or len(ports) == 0:
        print('Unable to find available ports')
        exit()
    print('Choosing first port: ' + str(ports[0]))
    connector = ArduinoConnector(ports[0])
    connector.initialize()

    print("Sending some bytes...")
    connector.write(b'abcdefg')

    print("All bytes sent")
    exit()


if __name__ == "__main__":
    main()
