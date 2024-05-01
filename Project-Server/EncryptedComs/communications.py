from tinyec import registry
import secrets
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import socket

global psk

class communications:
    # This class is used to handle all communications between the server and the client
    # It is used to encrypt and decrypt messages and to manage the OTP distribution

    def key_exchange(self):
        # Step 1: Generate keys
        privKey, pubKey = self.generate_key_pair(self.get_curve())
        

        # Step 2: Send public key
        self.send_key(self.compress(pubKey))

        # Step 3: Receive public key
        client_pubKey = self.receive_key()

        # Step 4: Compute shared secret
        shared_secret = self.compute_shared_secret(privKey, client_pubKey)

        return shared_secret

    # This method is used to generate a key pair for the device this is running on
    def generate_key_pair(self, curve):
        privKey = secrets.randbelow(curve.field.n)
        pubKey = privKey * curve.g
        return privKey, pubKey

    def compute_shared_secret(self, privKey, pubKey):
        shared_secret = privKey * pubKey

        # Hash the shared secret to get a 256-bit key
        shared_secret = hashlib.sha256(int.to_bytes(shared_secret, length=32, byteorder='big')).digest()

        return shared_secret


    # This method is used to send a key to the client
    def send_key(self, pub_key):
        # Send the key to the client using the socket
        HOST = "192.168.1.X"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server

        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")

            data = s.recv(1024)

        print(f"Received {data!r}")


    def compress(pubKey):
        return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

    def get_curve(self):
        secret = secrets.randbelow(100)
        print(secret)

        curve = registry.get_curve('brainpoolP256r1')
        return curve

class OTP:
    def __init__(self, key):
        self.key = key





        

