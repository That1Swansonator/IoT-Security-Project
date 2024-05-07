import secrets
from tinyec import registry
import ecc_example


def main():
    curve = ecc_example.get_curve()
    privKey, pubKey = ecc_example.generate_key_pair(curve)
    pubKey = ecc_example.compress(pubKey)

    # save the private key to a file psk.txt
    with open('psk.txt', 'w') as f:
        f.write(str(pubKey))

if __name__ == '__main__':
    main()