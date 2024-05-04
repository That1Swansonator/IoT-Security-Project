import socket
import threading

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

send("Hello World")