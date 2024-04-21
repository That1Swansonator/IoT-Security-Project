#!/usr/bin/env python3
import serial
import time
import socket

class HVACControls:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.command = "off"

    # set up network socket to recieve command from server
    def recieveCommand(self):
        # open a socket to listen for commands
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1234))
        s.listen(5)
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        while True:
            # recieve command from server
            command = clientsocket.recv(1024)

            if not command:
                break

            print(command.decode())

            # send command to arduino
            self.sendCommand(command.decode())

            # send response to server
            clientsocket.send(bytes("Command recieved", "utf-8"))


    def sendCommand(self, command):
        self.ser.write(command.encode())
        line = self.ser.readline().decode('utf-8').rstrip()
        return line

    def closeSerial(self):
        self.ser.close()

if __name__ == '__main__':
    hvac = HVACControls()
    # hvac.sendCommand("ac")
    hvac.recieveCommand()

    # Open serial port
    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.reset_input_buffer()
    # command = "off"
    #
    # # Send and receive data
    # while True:
    #     command = str(input("Enter command for HVAC (off, ac, hc): "))
    #     ser.write(command.encode()) # Send data over usb
    #     line = ser.readline().decode('utf-8').rstrip()
    #     print(line)
    #     time.sleep(1)