from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

curve = registry.get_curve('brainpoolP256r1')

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

# For Asymmetrical Encryption
def generate_public_key(privKey):
    pubKey = privKey * curve.g
    return privKey, pubKey

def generate_private_key():
    privKey = secrets.randbelow(curve.field.n)
    return privKey

def compute_shared_secret(privKey, pubKey):
    shared_secret = privKey * pubKey

    # Hash the shared secret to get a 256-bit key
    shared_secret = hashlib.sha256(int.to_bytes(shared_secret, length=32, byteorder='big')).digest()
    return shared_secret

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

# For Symmetrical Encryption
def ecc_calc_encryption_keys(pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    sharedECCKey = pubKey * ciphertextPrivKey
    return (sharedECCKey, ciphertextPubKey)

def ecc_calc_decryption_key(privKey, ciphertextPubKey):
    sharedECCKey = ciphertextPubKey * privKey
    return sharedECCKey

# The encryption and decryption functions
def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext


def main():
    pass

if __name__ == '__main__':
    main()