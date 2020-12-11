import random
import time
import math
import string
import json
import sympy
from base64 import b64encode, b64decode

MIN = 1000
MAX = 9999


class RSA:

    def __init__(self):
        self.p = self.q = self.n = self.phi = self.e = self.d = 0

    def generate_primes(self):
        self.p = sympy.randprime(MIN, MAX)
        self.q = sympy.randprime(MIN, MAX)
        while self.q == self.p:
            self.q = sympy.randprime(MIN, MAX)
        self.n = self.p * self.q
        print(f'Four digit primes p={self.p}, q={self.q} and their product n={self.n}')
        time.sleep(1)

    def generate_public_key(self):
        self.phi = (self.p-1)*(self.q-1)
        self.e = sympy.randprime(2, self.phi)
        while math.gcd(self.phi, self.e) != 1:
            self.e = sympy.randprime(2, self.phi)
        print(f'Phi={self.phi} and its coprime e={self.n}')
        time.sleep(1)

    def generate_private_key(self):
        self.d = pow(self.e, -1, self.phi)
        print(f'Private value d={self.d}')
        time.sleep(1)

    def encrypt_message(self, plaintext):
        decimal_values = list(map(lambda x: ord(x), list(plaintext)))
        encrypted_values = list(map(lambda x: pow(x, self.e, self.n), decimal_values))
        serialized_ciphertext = json.dumps(encrypted_values)
        encoded_ciphertext = b64encode((serialized_ciphertext.encode('ascii'))).decode('ascii')
        return encoded_ciphertext

    def decrypt_message(self, ciphertext):
        decoded_ciphertext = b64decode(ciphertext.encode('ascii')).decode('ascii')
        deserialized_ciphertext = json.loads(decoded_ciphertext)
        decrypted_values = list(map(lambda x: pow(x, self.d, self.n), deserialized_ciphertext))
        ascii_chars = list(map(lambda x: chr(x), decrypted_values))
        return ''.join(ascii_chars)


if __name__ == "__main__":
    message = ''.join([random.choice(string.ascii_letters) for _ in range(50)])
    rsa = RSA()
    rsa.generate_primes()
    rsa.generate_public_key()
    rsa.generate_private_key()
    encrypted_message = rsa.encrypt_message(message)
    decrypted_meesage = rsa.decrypt_message(encrypted_message)
    print(f'\nMessage: {message}\n\nEncrypted message: {encrypted_message}\n\nDecrypted message: {decrypted_meesage}')
