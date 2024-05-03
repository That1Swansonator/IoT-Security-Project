import socket
import threading

header= 64
port = 5050
server = socket.gethostbyname(socket.gethostname())
address = (server, port)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)

def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    while connected:
        msg_lenght = conn.recv(header).decode()

        msg = conn.recv()

def start():
    server.listen()
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[STARTING] server is starting")
start()