# Copied From https://cryptobook.nakov.com/asymmetric-key-ciphers/ecdh-key-exchange-examples

from tinyec import registry
import secrets

class ecdh_key_exchange:
    def compress(pubKey):
        return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

    def get_curve(self):
        secret = secrets.randbelow(100)
        print(secret)

        curve = registry.get_curve('brainpoolP256r1')
        return curve

    def generate_key_pair(self, curve):
        privKey = secrets.randbelow(curve.field.n)
        pubKey = privKey * curve.g
        return privKey, pubKey

if __name__ == '__main__':
    ecdh = ecdh_key_exchange()
    curve = ecdh.get_curve()
    privKey, pubKey = ecdh.generate_key_pair(curve)

    # curve = registry.get_curve('brainpoolP256r1')

    # alicePrivKey = secrets.randbelow(curve.field.n)
    # alicePubKey = alicePrivKey * curve.g
    # print("Alice public key:", compress(alicePubKey))
    #
    # bobPrivKey = secrets.randbelow(curve.field.n)
    # bobPubKey = bobPrivKey * curve.g
    # print("Bob public key:", compress(bobPubKey))
    #
    # print("Now exchange the public keys (e.g. through Internet)")
    #
    # aliceSharedKey = alicePrivKey * bobPubKey
    # print("Alice shared key:", compress(aliceSharedKey))
    #
    # bobSharedKey = bobPrivKey * alicePubKey
    # print("Bob shared key:", compress(bobSharedKey))
    #
    # print("Equal shared keys:", aliceSharedKey == bobSharedKey)