#!/usr/bin/env python3

# tempSensor libraries
import serial
import time
import mysql.connector as mysql
import os
from datetime import datetime

# key_exchange libraries
from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket


class tempSensor:
    def __init__(self):
        # Open serial port
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def scheduler(self):
        # Run getData function every 3 minutes
        while True:
            self.getData()
            time.sleep(180)

    def getData(self):
        # call dht11 function to get data every 5 minutes
        avg_temp = self.dht11()

        # Save data to database
        self.save_to_db(avg_temp)


    def dht11(self):
        # create an array to store 10 temperature values
        temp_arr = []
        # create a variable loopControl to control the loop
        loopControl = 0

        # Send and receive data. Default is True
        while loopControl < 10:
            line = self.ser.readline().decode('utf8').rstrip()  # read a '\n' terminated line

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


    def close(self):
        self.ser.close()

    def save_to_db(self, avg_temp):
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

        # get the current date and time
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        print("Date and Time Created")

        try:
            # Insert data into table TempHistory, columns: tempc, tempdate, temptime
            query = "INSERT INTO TempHistory (tempc, tempdate, temptime) VALUES (%s, %s, %s)"
            values = (avg_temp, date, time)
            cursor.execute(query, values)

            db.commit()
            print(f"Data inserted into database: {avg_temp}°C, {date}, {time}")

        except Exception as e:
            print(f"Error inserting data into database: {e}")
            db.rollback()
            exit()

        # Close cursor and database
        cursor.close()
        db.close()

# Class to handle key exchange and secure communications
class key_exchange:
    # Get a key from enviroment variable
    psk = os.getenv('PSK')

    # This method operates the key exchange
    def key_exchange(self):
        # Step 1: Generate keys
        privKey, pubKey = self.generate_key_pair(self.get_curve())

        # Step 2: Send public key
        self.send_key(self.compress(pubKey))

        # Step 3: Receive public key
        client_pubKey = self.receive_key()

        # Step 4: Compute shared secret
        shared_secret = self.compute_shared_secret(privKey, client_pubKey)

        return shared_secret


    # The next 3 methods are used for key gen, compression, and shared secret computation
    def get_curve(self):
        secret = secrets.randbelow(100)
        print(secret)

        curve = registry.get_curve('brainpoolP256r1')
        return curve

    def compress(pubKey):
        return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

    def generate_key_pair(self, curve):
        privKey = secrets.randbelow(curve.field.n)
        pubKey = privKey * curve.g
        return privKey, pubKey

    def compute_shared_secret(self, privKey, pubKey):
        shared_secret = privKey * pubKey

        # Hash the shared secret to get a 256-bit key
        shared_secret = hashlib.sha256(int.to_bytes(shared_secret, length=32, byteorder='big')).digest()

        return shared_secret

    # The next 2 methods are used for sending and receiving keys
    def send_key(self, pub_key):
            # Send the key to the client using the socket
            HOST = os.getenv('HOST')  # The server's hostname or IP address
            PORT = 65432  # The port used by the server

            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(b"Hello, world")

                data = s.recv(1024)

            print(f"Received {data!r}")

    def receive_key(self):
        # Receive the key from the client using the socket
        HOST = os.getenv('HOST')
        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)







if __name__ == '__main__':
    sensor = tempSensor()
    # sensor.getData()
    sensor.scheduler()