#!/usr/bin/env python3
import serial
import time
import socket

class HVACControls:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.command = "off"

    # Ask User to set a goal temperature
    def setGoalTemp(self):
        goalTemp = float(input("Enter goal temperature: "))
        return goalTemp

    # Recieve the current temperature from server at 192.168.1.30 port 1234
    def recieveTemp(self):
        loop = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while loop
            try:
                s.connect(('192.168.1.30', 1234))
                temp = s.recv(1024).decode()
                loop = False

            except Exception as e:
                print(f"Error connecting to server: {e}")


        s.close()
        return temp

    # send command to arduino
    def sendCommand(self, command):
        self.ser.write(command.encode())
        line = self.ser.readline().decode('utf-8').rstrip()
        return line

    def closeSerial(self):
        self.ser.close()

    def run(self):
        while True:
            goalTemp = float(self.setGoalTemp())
            currentTemp = float(self.recieveTemp())
            print(f"Goal Temp: {goalTemp}, Current Temp: {currentTemp}")

            if currentTemp < goalTemp:
                command = "ac"
            elif currentTemp > goalTemp:
                command = "hc"
            else:
                command = "off"

            self.sendCommand(command)
            time.sleep(1)
            print("Command sent to HVAC")

            #wait 5 minutes
            time.sleep(300)

if __name__ == '__main__':
    hvac = HVACControls()
    hvac.run()

