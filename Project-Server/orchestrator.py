import socket
import time
import mysql.connector as mysql
import os

# Create a class ochestrator to get the latest data from the database and send it to the RPi
class Orchestrator:
    def __init__(self):
        print("Orchestrator initialized")

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

    # Send the temperature to the RPi at the specified IP address and port
    def sendTemp(self, temp):
        loop = True

        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while loop:
            try:
                # Connect to the RPi
                s.connect(('192.168.1.73', 1234))

                # Send the temperature
                s.sendall(str(temp[0]).encode())
                print("Temperature sent to RPi")
                loop = False

            except Exception as e:
                print(f"Error connecting to RPi: {e}")
                # exit()

        # Close the socket
        s.close()

    # Run the orchestrator every 5 minutes
    def run(self):
        while True:
            temp = self.getLatestData()
            self.sendTemp(temp)
            time.sleep(300)

if __name__ == '__main__':
    orchestrator = Orchestrator()
    orchestrator.run()