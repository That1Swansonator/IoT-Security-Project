#!/usr/bin/env python3
import serial
import time
import mysql.connector

class HVACControl:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.command = "off"

    def send_receive_data(self):
        while True:
            self.command = str(input("Enter command for HVAC (off, ac, hc): "))
            self.ser.write(self.command.encode()) # Send data over usb
            line = self.ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)

if __name__ == '__main__':
    hvac = HVACControl()
    hvac.send_receive_data()