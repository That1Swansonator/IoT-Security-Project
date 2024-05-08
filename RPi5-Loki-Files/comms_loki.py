from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket
import threading
import os
import ecc
import hvacControls

# IMPORTANT: This file will use a protocol format for messages. The format is as follows:
# ![COMMAND]:[ARGUMENT]

# The key bay
private_key = ecc.generate_private_key()
public_key = ecc.generate_public_key(private_key)
shared_key = None
other_public_key = None
other_private_key = None

default_port = 5050
header = 64
port = 5050
FORMAT = 'utf-8'
disconnect_msg = "!Disconnect"

# Clientside Communications. Run this function to connect to a server. Runs once per call
def clientside(message, d_port=port):
    # Get a name  from environment variable
    server = os.getenv('DESTINATION_SERVER')
    address = (server, d_port)

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

    send(message)


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


def msg_interpreter(msg):
    # IMPORTANT: This file will use a protocol format for messages. The format is as follows:
    # ![COMMAND]:[ARGUMENT]
    # The command cannot contain any spaces nor be encrypted. The argument can be encrypted

    # split the message into a command and an argument on the : character. Might add more splitting later
    cmd, arg = msg.split(":")

    # Start the Key Exchange Process. The argument is the public key of the incoming client
    if cmd == "!KEP":
        clientside()

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
