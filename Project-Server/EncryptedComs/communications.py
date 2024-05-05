from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket
import threading
import pyotp

import ecc_example as ecc

# If running as a server, import the hvacControls module
# import hvacControls

# If running as a client, this file will be imported by tempSensor.py


# Create a global variable psk that contains a key saved in psk.txt
def get_psk():
    with open('psk.txt', 'r') as f:
        psk = f.read()
    return psk

psk = get_psk()
default_port = 5050

# Main Functions
def main():
   pass


# Encryption and Decryption Function
# call ecc_example for these functions

# Clientside Communications
def client(d_port):
    pass


# Serverside communications
# d_port is the port that the server will listen on. Can be called recursively.
def server(d_port):
    header= 64
    port = d_port
    server = socket.gethostbyname(socket.gethostname())
    address = (server, port)
    FORMAT = 'utf-8'
    disconnect_msg = "!Disconnect"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)

    def handle_client(conn, address):
        print(f"[NEW CONNECTION] {address} connected")

        connected = True
        while connected:
            msg_lenght = conn.recv(header).decode(FORMAT)

            if msg_lenght:
                msg_lenght = int(msg_lenght)
                msg = conn.recv(msg_lenght).decode(FORMAT)

                if msg == disconnect_msg:
                    connected = False

                print(f"[{address}] {msg}")
                conn.send("Msg Recieved".encode(FORMAT))

        conn.close()

    def msg_interpreter(msg):
        msg = decrypt_AES_GCM(msg, psk)
        # slip the message into a command and an argument on the : character
        cmd, arg = msg.split(":")

        if cmd == "!START":
            print(f"Starting Server at port {arg}")
            server(arg)

        if cmd == "!TEMP":
            pass

        if cmd == "!END":
            print("Ending Server")
            server.close()

        else:
            print("Invalid Command")

    def start():
        server.listen()
        print(f"[LISTENING] Server is listening on {server}")

        while True:
            conn, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

    print("[STARTING] server is starting")
    start()

def client():
    header= 64
    port = 5050
    FORMAT = 'utf-8'
    disconnect_msg = "!Disconnect"
    server = "192.168.1.59"
    address = (server, port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    def send(msg):
        message = msg.encode(FORMAT)
        msg_len = len(message)

        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (header - len(send_len))

        client.send(send_len)
        client.send(message)
        print(client.recv(2048).decode())

if __name__ == '__main__':
    main()