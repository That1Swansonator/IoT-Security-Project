from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket
import threading
import os

import ecc
import tempSensor


# If running as a server, import the hvacControls module
# import hvacControls

# If running as a client, this file will be imported by tempSensor.py

# The key bay
private_key = ecc.generate_private_key()
public_key = ecc.generate_public_key(private_key)
shared_key = None
other_public_key = None
other_private_key = None
default_port = 5050


# Main Functions
def main():
    # start key exchange process
    clientside("!KEP", ecc.compress(public_key), "False")
    shared_key = ecc.compute_shared_secret(private_key, other_public_key)

    # securely send the private key to the other party
    # Encrypt the private key using the shared key
    # encrypted_private_key = ecc.
    # clientside("!PKE", )



header = 64
port = 5050
FORMAT = 'utf-8'
disconnect_msg = "!Disconnect"


# Clientside Communications. Run this function to connect to a server. Runs once per call
def clientside(command, argument, encryption_status, d_port=port):
    # Get a name  from environment variable
    server = os.getenv('DESTINATION_SERVER')
    address = (server, d_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    def send(msg):
        header = command.encode(FORMAT)
        message = msg.encode(FORMAT)
        encrypt = encryption_status.encode(FORMAT)

        hed_len = len(header)
        msg_len = len(message)
        ens_len = len(encrypt)

        send_len = str(hed_len+msg_len+ens_len).encode(FORMAT)
        send_len += b' ' * (header - len(send_len))

        client.send(send_len)

        # If this does not work, send the items separately
        client.send(header, message, encrypt)
        print(client.recv(2048).decode())

        if command == "!KEP":
            other_public_key = client.recv(2048).decode()

    send(argument)

# Serverside communications
def serverside(d_port=port, end=False):
    server = socket.gethostbyname(socket.gethostname())
    address = (server, d_port)

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
                conn.send("!RECIEVED".encode(FORMAT))

                if end:
                    #kill the server
                    server.close()
                    msg_interpreter(msg)

                msg_interpreter(msg)

        conn.close()

    def start():
        server.listen()
        print(f"[LISTENING] Server is listening on {server}")

        while True:
            conn, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    print("[STARTING] server is starting")
    start()


def msg_interpreter(cmd, arg, encryption_status):
    # If the encryption status is true, decrypt the message. Decrypt using the shared key
    if encryption_status:
        # Decrypt the message
        pass


    # Start the key exchange process. The argument is the public key of the incoming client
    # if cmd == "!KEP":
    #     clientside()

    # Start new server instance
    if cmd == "!NE":
        # Create a new instance of the server at a different port if needed and
        # kills the instance after running
        serverside(arg, True)


    if cmd == "!TEMP":
        pass

    else:
        print("Invalid Command")


if __name__ == '__main__':
    main()
