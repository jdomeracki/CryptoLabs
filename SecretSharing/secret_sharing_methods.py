import random
import sympy
import sys
import numpy
import math
from os import system, name
from time import sleep


def trivial_secret_sharing_split(k, n, s):
    shares = []
    for _ in range(n-1):
        shares.append(random.randint(0, k-1))
    tmp = s
    for share in shares:
        tmp -= share
    shares.append(tmp % k)
    return shares


def trivial_secret_sharing_reconstruct(k, shares):
    secret = sum(shares) % k
    return secret


def polynomial_value(factors, x):
    result = factors[0]
    for i in range(1, len(factors)):
        result = result*x + factors[i]
    return result


def shamir_secret_sharing_split(k, n, s, t):
    while True:
        p = random.randint(max(s, n), 2*k)
        if(sympy.isprime(p)):
            break
    factors = []
    for _ in range(t-1):
        factors.append(random.randint(0, s))
    factors.append(s)
    shares = []
    for i in range(1, n+1):
        shares.append(polynomial_value(factors, i) % p)
    print(f'Randomly generated prime number p where p > s: {p}')
    print(f'Randomly generated factors: {factors[:-1]}')
    print(f'Generated shares: {shares}')
    return shares, p


def interpolate(x_coordinates, x):
    counter, denominator = 0, 0
    all_but_x = [xi for xi in x_coordinates if xi != x]
    counter = numpy.prod(all_but_x)
    if(len(all_but_x) % 2 == 1):
        counter = (-1)*counter
    indv_denomintaors = []
    for xi in all_but_x:
        indv_denomintaors.append(x - xi)
    denominator = numpy.prod(indv_denomintaors)
    y_intercept = counter/denominator
    return y_intercept


def shamir_secret_sharing_reconstruct(shares, n, p, t):
    shares_subset = random.sample(shares, t)
    x_coordinates = []
    for share in shares_subset:
        x_coordinates.append(shares.index(share)+1)
    secret = 0
    for x in x_coordinates:
        intercept_param = (interpolate(x_coordinates, x) * shares[x-1])
        # python '%' operator != C-style modulo
        secret += math.fmod(intercept_param, p)
    return int(secret)


def menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Trivial method [1]")
    print("2. Shamir's secret sharing method [2]")
    print("3. Exit [3]")
    print(67 * "-")


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


if __name__ == "__main__":
    while True:
        menu()
        option = int(input('Please choose an option [1-3]:\n'))
        if(option == 1):
            k = int(input('Please enter threshold k:\n'))
            n = int(input('Please enter number of shares n:\n'))
            s = random.randint(0, k-1)
            print(f'Initially generated secret: {s}')
            shares_list = trivial_secret_sharing_split(k, n, s)
            print(f'Randomly generated shares: {shares_list}')
            print(
                f'Reconstructed secret: {trivial_secret_sharing_reconstruct(k, shares_list)}')
            sleep(5)
            clear()
        elif(option == 2):
            k = int(input('Please enter threshold k:\n'))
            n = int(input('Please enter number of shares n:\n'))
            t = int(input('Please enter number of required shares t:\n'))
            s = random.randint(0, k-1)
            print(f'Initially generated secret: {s}')
            shares_list, p = shamir_secret_sharing_split(k, n, s, t)
            print(
                f'Reconstructed secret: {shamir_secret_sharing_reconstruct(shares_list, n, p, t)}')
            sleep(20)
            clear()
        elif(option == 3):
            break
        else:
            print('!Invalid option!')
            sleep(3)
            clear()
