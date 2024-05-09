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

def main():
    # Loki is the server
    serverside()
    pass

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

                # If this does not work, send the items separately
                cmd, msg, ecs = conn.recv(msg_lenght).decode(FORMAT)

                if msg == disconnect_msg:
                    connected = False

                print(f"[{address}] {msg}")
                conn.send("!RECIEVED".encode(FORMAT))

                # If the message is a command !KEP, send back the public key of the server
                if cmd == "!KEP":
                    # Generate a public key and send it back to the client
                    compressed_public_key = ecc.compress(public_key)
                    conn.send(compressed_public_key.encode(FORMAT))

                    # Compute the shared key, msg is the other public key
                    shared_key = ecc.compute_shared_secret(private_key, msg)

                # If the command is !PKE, decrypt the message using the shared key
                elif cmd == "!PKE":
                    # Encrypt
                    return None

                # if the command is AUTH, start the OTP authentication process
                elif cmd == "!AUTH":
                    # Start OTP authentication and exchange
                    pass

                if end or cmd == "!END":
                    #kill the server
                    server.close()

                else:
                    msg_interpreter(cmd, msg, ecs)


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


def msg_interpreter(cmd, arg, encrypted):
    # If the encryption status is true, decrypt the message. Decrypt using the shared key
    # This will break without the shared key
    try:
        if encrypted:
            # Decrypt the message
            arg = ecc.decrypt_ECC(arg, shared_key) # Ignore this error
    except Exception as e:
        print("Error decrypting message, Did you forget to run the key exchange process?")
        print(e)


    # Start the shared secret process. The argument is the public key of the incoming client
    if cmd == "!KEP":
        shared_key = ecc.compute_shared_secret(private_key, arg)

    # Start new server instance
    elif cmd == "!NE":
        # Create a new instance of the server at a different port if needed and
        # kills the instance after running
        serverside(arg, True)

    elif cmd == "!TEMP":
        pass

    elif cmd == "!AUTH":
        # Start OTP authentication and exchange
        pass

    else:
        print("Invalid Command")


if __name__ == '__main__':
    main()
