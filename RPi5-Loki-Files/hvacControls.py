#!/usr/bin/env python3
import serial
import time
import os


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
command = "off"

# Setting thw default goal temperature to 20.0 C
goalTemp = None

# Ask User to set a goal temperature
def setGoalTemp(user_temp):
    # goalTemp = float(input("Enter goal temperature: "))
    # Get goal temperature from environment variable
    goalTemp = user_temp
    print(f"Goal Temp: {goalTemp}")

def set_mode(recieved_temp):
    # This function will compare the received temperature with the goal temperature
    # and set the mode of the HVAC system
    received_temp = float(recieved_temp)

    print(f"Goal Temp: {goalTemp}, Current Temp: {received_temp}")

    if received_temp < goalTemp:
        sendCommand("hc")

    elif received_temp > goalTemp:
        sendCommand("ac")
        
    else:
        sendCommand("off")



# send command to arduino
def sendCommand(command):
    ser.write(command.encode())
    line = ser.readline().decode('utf-8').rstrip()
    print(line)

def closeSerial():
    ser.close()

def main():
    # goalTemp = setGoalTemp()
    # goalTemp = float(goalTemp)
    #
    # while True:
    #     temp = getLatestData()
    #     currentTemp = float(temp[0])
    #
    #     print(f"Goal Temp: {goalTemp}, Current Temp: {currentTemp}")
    #
    #     if currentTemp < goalTemp:
    #         command = "hc"
    #
    #     elif currentTemp > goalTemp:
    #         command = "ac"
    #     else:
    #         command = "off"
    #
    #     sendCommand(command)
    #     time.sleep(1)
    #     print("Command sent to HVAC")
    pass


if __name__ == '__main__':
    main()