# key_exchange libraries
import os
from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket

# import client

# This method operates the key exchange
def main():
    # Step 1: Generate keys
    curve = get_curve()
    privKey, pubKey = generate_key_pair(curve)



# The next 3 methods are used for key gen, compression, and shared secret computation
def get_curve():
    secret = secrets.randbelow(100)
    print(secret)

    curve = registry.get_curve('brainpoolP256r1')
    return curve

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

def generate_key_pair(curve):
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    return privKey, pubKey

def compute_shared_secret(privKey, pubKey):
    shared_secret = privKey * pubKey

    # Hash the shared secret to get a 256-bit key
    shared_secret = hashlib.sha256(int.to_bytes(shared_secret, length=32, byteorder='big')).digest()

    return shared_secret

# The next 2 methods are used for sending and receiving keys
def send_key(pub_key):
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

    send(pub_key)

def receive_key():
    # Receive the key from the client using the socket
    HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
    PORT = 5050  # The port used by the key exchange

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

if __name__ == '__main__':
    main()