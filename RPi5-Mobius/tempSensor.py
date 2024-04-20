#!/usr/bin/env python3
from datetime import datetime

import serial
import time
import mysql.connector as mysql
import os

class tempSensor:
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

            # Save data to database
            # self.save_to_db(temperature)
    def close(self):
        self.ser.close()

    def save_to_db(avg_temp):
        try:
            # Get password from environment variable
            password = os.getenv('MY_PASSWORD')

            # get username from environment variable
            user = os.getenv('MY_USER')

            # get hostname from environment variable
            host = os.getenv('MY_HOST')

            # get database name from environment variable
            database = os.getenv('MY_DATABASE')

            # Connect to database
            db = mysql.connect(
                host=host, user=user, passwd=password, database=database)

        except Exception as e:
            print(f"Error connecting to database: {e}")

        # Create a cursor
        cursor = db.cursor()

        # get the current date and time
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        # Insert data into table
        cursor.execute(f"insert into TempHistory (tempC, tempDate, tempTime) values (avg_temp, date, time)")

        # Close cursor and database
        cursor.close()
        db.close()


if __name__ == '__main__':
    sensor = tempSensor()
    sensor.run()
