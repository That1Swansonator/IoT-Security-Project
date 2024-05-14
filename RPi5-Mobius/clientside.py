
import socket
import threading
import os
import ecc
# If running as a client, this file will be imported by tempSensor.py

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
def clientside():
    server = "192.168.1.59"
    address = (server, port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    def send(msg):
        message = msg.encode(FORMAT)

        msg_len = len(message)

        # Operations Block
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (header - len(send_len))
        client.send(send_len)
        client.send(message)
        print(client.recv(2048).decode())

    # send("!TEST","Hello World!", False)
    send("!TEST")
    send("Hello World!")
    send("False")
def msg_interpreter(cmd, arg, encryption_status):
    # If the encryption status is true, decrypt the message. Decrypt using the shared key
    if encryption_status:
        # Decrypt the message
        pass


# Main Functions
def main():
    clientside()
    # start key exchange process
    # clientside("!KEP", ecc.compress(public_key), "False")
    # shared_key = ecc.compute_shared_secret(private_key, other_public_key)

    # securely send the private key to the other party
    # Encrypt the private key using the shared key
    # encrypted_private_key = ecc.
    # clientside("!PKE", )


if __name__ == '__main__':
    main()
