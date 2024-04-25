#!/usr/bin/env python3
import serial
import time
import mysql.connector as mysql
import os

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
    def getLatestData(self):
        # Connect to the database
        try:
            # Get password from environment variable
            password = os.getenv('MY_PASSWORD')
            print("Passed password")

            # get username from environment variable
            user = os.getenv('MY_USER')
            print("User: ", user)

            # get hostname from environment variable
            host = os.getenv('MY_HOST')
            print("Host: ", host)

            # get database name from environment variable
            database = os.getenv('MY_DATABASE')
            print("Database: ", database)

            # Connect to database
            db = mysql.connect(
                host=host, user=user, passwd=password, database=database)

            print("Connected to database")

        except Exception as e:
            print(f"Error connecting to database: {e}")
            exit()

        # Create a cursor
        cursor = db.cursor()
        print("Cursor created")

        # Get the latest data from the database
        cursor.execute("SELECT tempC FROM TempHistory ORDER BY tempTime DESC LIMIT 1")
        temp = cursor.fetchone()
        print("Data fetched from database", temp)

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
            temp = self.getLatestData()
            currentTemp = float(temp[0])

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

