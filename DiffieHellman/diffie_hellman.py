import random
import time
import sympy

MIN = 100
MAX = 200


class KeyEchangeParty:

    def __init__(self, name, n, g):
        self.name = name
        self.n = n
        self.g = g
        self.private_key = 0
        self.received_public_key = 0
        self.shared_secret = 0
        print(f'{self.name}: I agree to use n={self.n} and g={self.g}')
        time.sleep(1)

    def generate_private_key(self):
        self.private_key = random.randint(MIN, MAX)
        print(f'{self.name}: My super secret private key={self.private_key} [Shouldn`t be shared]')
        time.sleep(1)

    def exchange_public_key(self):
        public_key = self.g ** self.private_key % self.n
        print(f'{self.name}: My public key={public_key}')
        time.sleep(1)
        return public_key

    def calculate_shared_secret(self, received_public_key):
        self.received_public_key = received_public_key
        self.shared_secret = self.received_public_key ** self.private_key % self.n
        print(f'{self.name}: Received public key={self.received_public_key} and calculated symmetric key={self.shared_secret}')
        time.sleep(1)


def generate_prime():
    n = sympy.randprime(MIN, MAX)
    return n


def generate_prime_factors(phi):
    prime_factors = sympy.primefactors(phi)
    return prime_factors


def check_if_is_primitive_root(i, phi, n, prime_factors):
    for prime_factor in prime_factors:
        if (i ** (phi/prime_factor)) % n == 1:
            return False
    return True


def generate_primitive_root(n):
    phi = n-1
    prime_factors = generate_prime_factors(phi)
    primitive_roots = []
    for i in range(2, phi+1):
        if check_if_is_primitive_root(i, phi, n, prime_factors):
            primitive_roots.append(i)
    return random.choice(primitive_roots)


if __name__ == "__main__":
    n = generate_prime()
    g = generate_primitive_root(n)
    alice = KeyEchangeParty('Alice', n, g)
    bob = KeyEchangeParty('Bob', n, g)
    alice.generate_private_key()
    bob.generate_private_key()
    alices_public_key = alice.exchange_public_key()
    bobs_public_key = bob.exchange_public_key()
    alice.calculate_shared_secret(bobs_public_key)
    bob.calculate_shared_secret(alices_public_key)
