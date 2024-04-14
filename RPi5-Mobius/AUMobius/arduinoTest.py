#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    # Open serial port
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    # Send and receive data
    while True:
        ser.write(b"Hello from Raspberry Pi!\n") # Send data over usb 
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)