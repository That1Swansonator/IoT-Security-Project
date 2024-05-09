#!/usr/bin/env python3

# tempSensor libraries
import serial
import time
import mysql.connector as mysql
import os
from datetime import datetime

import ecc
import comms_mobius as comms

# The key bay
private_key = ecc.generate_private_key()
public_key = ecc.generate_public_key(private_key)
shared_key = None
other_public_key = None
other_private_key = None

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

def main():
    # start key exchange process
    other_public_key = comms.clientside("!KEP", ecc.compress(public_key), "False")
    shared_key = ecc.compute_shared_secret(private_key, other_public_key)
    print(shared_key)

    # securely send the private key to the other party
    # Encrypt the private key using the shared key
    # encrypted_private_key = ecc.encrypt_ECC(private_key, shared_key)
    # other_private_key = comms.clientside("!PKE", encrypted_private_key, True)

    # Run getData function every 3 minutes
    # while True:
    #     getData()
    #     time.sleep(180)

def dht11():
    # create an array to store 10 temperature values
    temp_arr = []
    # create a variable loopControl to control the loop
    loopControl = 0

    # Send and receive data. Default is True
    while loopControl < 10:
        line = ser.readline().decode('utf8').rstrip()  # read a '\n' terminated line

        try:
            humidity, temperature = map(float, line.split(','))
            print(f"Humidity: {humidity}% Temperature: {temperature}°C")
            temp_arr.append(temperature)

            loopControl += 1

        except ValueError as e:
            # This will catch twice at initialization and if the ground leeds are not connected
            print(f"Error converting data to float: {e}")
        time.sleep(1)

    # Calculate the average temperature
    avg_temp = sum(temp_arr) / len(temp_arr)
    avg_temp = round(avg_temp, 2)
    # avg_temp = float(avg_temp)
    print(f"Average temperature: {avg_temp}°C")

    # return the average temperature
    return avg_temp

def getData():
    # call dht11 function to get data every 5 minutes
    avg_temp = dht11()

def close():
    ser.close()

def send_to_server():
    # This will format the data into a usable state
    pass

def init_communication():
    # Send a message to the server to initialize communication for key exchange
    pass




