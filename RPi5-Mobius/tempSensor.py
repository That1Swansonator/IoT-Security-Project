#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    # Open serial port
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    # Send and receive data
    while True:
        line = ser.readline().decode('utf8').rstrip()  # read a '\n' terminated line
        humidity, temperature = map(float, line.split(','))
        print(f"Humidity: {humidity}% Temperature: {temperature}°C")
        time.sleep(1)