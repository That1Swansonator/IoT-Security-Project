#!/usr/bin/env python3
import serial
import time

class TempSensor:
    def __init__(self):
        # Open serial port
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def run(self):
        # Send and receive data
        while True:
            line = self.ser.readline().decode('utf8').rstrip()  # read a '\n' terminated line

            try:
                humidity, temperature = map(float, line.split(','))
                print(f"Humidity: {humidity}% Temperature: {temperature}°C")

            except ValueError as e:
                print(f"Error converting data to float: {e}")
            time.sleep(1)

if __name__ == '__main__':
    sensor = TempSensor()
    sensor.run()
