import sympy
import itertools
import operator
import numpy
from collections import Counter

MIN = 100_000_000
MAX = 999_999_999
NUM_OF_BITS = 200_00


def generate_pretty_big_primes():
    while True:
        p = sympy.randprime(MIN, MAX)
        if p % 4 == 3:
            break
    while True:
        q = sympy.randprime(MIN, MAX)
        if q % 4 == 3 and q != p:
            return p, q


def gcd(n, x):
    while x != 0:
        n, x = x, n % x
    return n


def generate_seed(N):
    x = sympy.randprime(MIN, MAX)
    while gcd(N, x) != 1:
        x = sympy.randprime(MIN, MAX)
    return x


def generate_bits(x, N):
    bits = []
    for _ in range(NUM_OF_BITS):
        x = x*x % N
        bit = x % 2
        bits.append(bit)
    return bits


def test_single_bits(bits):
    min, max, counter = 9725, 10275, 0
    for bit in bits:
        if bit == 1:
            counter += 1
    return min < counter < max


def test_series(bits):
    ranges = {'1': [2315, 2685], '2': [1114, 1386], '3': [527, 723], '4': [240, 384], '5': [103, 209]}
    ones = Counter(sum(1 for item in group) for head, group in itertools.groupby(bits) if head == 1)
    zeros = Counter(sum(1 for item in group) for head, group in itertools.groupby(bits) if head == 0)
    six_up_ones, six_up_zeros = sum(ones.values()), sum(zeros.values())
    for key, value in ranges.items():
        seq_num_ones, seq_num_zeros = ones[int(key)], zeros[int(key)]
        floor, ceil = value[0], value[1]
        if floor <= seq_num_ones <= ceil and floor <= seq_num_zeros <= ceil:
            six_up_ones -= seq_num_ones
            six_up_zeros -= seq_num_zeros
        else:
            return False
    return True if 103 <= six_up_ones <= 209 and 103 <= six_up_zeros <= 209 else False


def test_long_series(bits):
    zeros = len(max((list(y) for (x, y) in itertools.groupby((enumerate(bits)), operator.itemgetter(1)) if x == 0), key=len))
    ones = len(max((list(y) for (x, y) in itertools.groupby((enumerate(bits)), operator.itemgetter(1)) if x == 1), key=len))
    return max(zeros, ones) < 26


def test_poker(bits):
    min_val, max_val, x = 2.16, 46.17, 0.0
    four_bit_parts = numpy.array_split(bits, 5000)
    decimal_values = []
    for quartet in four_bit_parts:
        decimal_values.append(int("".join(str(x) for x in quartet), 2))
    grouped_dec_count = dict(Counter(decimal_values))
    for count in grouped_dec_count.values():
        x += count * count
    x = float(16/5000) * x - 5000
    return min_val < x < max_val


if __name__ == "__main__":
    p, q = generate_pretty_big_primes()
    N = p*q
    x = generate_seed(N)
    bits = generate_bits(x, N)
    print(f'p: {p}, q: {q}\nN: {N}, seed: {x}\n')
    print('Single bits test passed') if test_single_bits(bits) else print('Single bits test failed')
    print('Series test passed') if test_series(bits) else print('Series test failed')
    print('Long series test passed') if test_long_series(bits) else print('Longe series test failed')
    print('Poker test passed') if test_poker(bits) else print('Poker series test failed')
