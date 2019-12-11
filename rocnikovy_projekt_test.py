import rocnikovy_projekt
import pytest
import random
import math

iterations = 5000
square_range = 10**12
relatively_prime_range = 100


def test_square_random_positive_square():
    for _ in range(iterations):
        n = random.randint(1,square_range)
        assert rocnikovy_projekt.is_square(n**2) is True


def test_square_random_positive_not_square():
    for _ in range(iterations):
        m = random.randint(2,square_range)
        n = random.randint(m**2 + 1, (m + 1)**2 - 1)
        assert rocnikovy_projekt.is_square(n) is False


def test_square_random_negative():
    for _ in range(iterations):
        n = - random.randint(1,square_range)
        assert rocnikovy_projekt.is_square(n) is False


def test_square_zero():
    assert rocnikovy_projekt.is_square(0) is True


def test_relatively_prime_one_one_relatively_prime():
    rocnikovy_projekt.add_all_pairs(1)
    assert [1,1] in rocnikovy_projekt.get_pairs()


def test_relatively_prime_random_relatively_prime():
    rocnikovy_projekt.add_all_pairs(relatively_prime_range+1)
    for _ in range(iterations):
        a = random.randint(1,relatively_prime_range)
        b = random.randint(1,relatively_prime_range)
        d = math.gcd(a,b)
        a = a//d
        b = b//d
        assert [a,b] in rocnikovy_projekt.get_pairs()


def test_relatively_prime_random_not_relatively_prime():
    rocnikovy_projekt.add_all_pairs(relatively_prime_range+1)
    for _ in range(iterations):
        d = random.randint(2,int(math.sqrt(relatively_prime_range)))
        a = d*random.randint(1,relatively_prime_range//d)
        b = d*random.randint(1,relatively_prime_range//d)
        assert [a,b] not in rocnikovy_projekt.get_pairs()




