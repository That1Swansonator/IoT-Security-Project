import socket
import threading
import os
import ecc
# import hvacControls

# IMPORTANT: This file will use a protocol format for messages. The format is as follows:
# ![COMMAND]:[ARGUMENT]

# The key bay
private_key = ecc.generate_private_key()
public_key = ecc.generate_public_key(private_key)
shared_key = None
other_public_key = None
other_private_key = None

# Format for messages
command = None
argument = None
encrypted = False

default_port = 5050
header = 64
port = 5050
FORMAT = 'utf-8'
disconnect_msg = "!Disconnect"

def serverside():
    server = socket.gethostbyname(socket.gethostname())
    print(server)
    address = (server, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)

    def handle_client(conn, address):
        print(f"[NEW CONNECTION] {address} connected")

        stage = 0
        connected = True
        while connected:
            msg_lenght = conn.recv(header).decode(FORMAT)

            if msg_lenght:
                msg_lenght = int(msg_lenght)

                # If this does not work, send the items separately
                msg = conn.recv(msg_lenght).decode(FORMAT)

                if msg == disconnect_msg:
                    connected = False

                print(f"[{address}] {msg}")
                conn.send("!RECIEVED".encode(FORMAT))

                # The message interpreter
                cmd, arg, encrypted = msg.split(":")

                if cmd == "!KEP":
                    other_public_key = arg
                    # print(other_public_key)
                    keystring = str(public_key)
                    conn.send(keystring.encode(FORMAT))
                    # close the connection
                    # connected = False

                if cmd == "!PKE":
                    pass

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
    pass

def main():
    serverside()

if __name__ == '__main__':
    main()
