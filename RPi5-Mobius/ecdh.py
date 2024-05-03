# key_exchange libraries
import os
from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket
import pyDH


# Get a key from enviroment variable
psk = os.getenv('PSK')

# This method operates the key exchange
def key_exchange():
    # Step 1: Generate keys
    privKey, pubKey = generate_key_pair(get_curve())

    # Step 2: Send public key
    send_key(compress(pubKey))

    # Step 3: Receive public key
    client_pubKey = receive_key()

    # Step 4: Compute shared secret
    shared_secret = compute_shared_secret(privKey, client_pubKey)

    return shared_secret


# The next 3 methods are used for key gen, compression, and shared secret computation
def get_curve(self):
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
    # Send the key to the client using the socket
    HOST = os.getenv('HOST')  # The server's hostname or IP address
    PORT = 5050  # The port used by the server

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")

        data = s.recv(1024)

    print(f"Received {data!r}")

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

