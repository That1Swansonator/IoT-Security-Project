
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
def clientside(cmd, stuff):
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

        if cmd == "!PKE":
            other_public_key = client.recv(2048).decode()
            print(other_public_key)

    # send("!TEST","Hello World!", False)
    send(stuff)

def msg_interpreter(cmd, arg, encryption_status):
    # If the encryption status is true, decrypt the message. Decrypt using the shared key
    if encryption_status:
        # Decrypt the message
        pass


# Main Functions
def main():
    # Public Key Exchange
    command = "!KEP"
    key = ecc.compress_point(public_key[1])
    encrypted = "False"
    message = f"{command}:{key}:{encrypted}"
    clientside(command, message)
    shared_key = ecc.compute_shared_secret(private_key, other_public_key)

    # Private Key Exchange
    command = "!PKE"
    encrypted = "True"
    # encrypted_private_key = ecc.encrypt_ECC(private_key, shared_key)
    # print(encrypted_private_key)



if __name__ == '__main__':
    main()
