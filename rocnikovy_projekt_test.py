from math import gcd, isqrt
from random import randint
from rocnikovy_projekt import is_square, add_all_pairs, get_pairs
from unittest import main, TestCase

class SquareTest(TestCase):
    def setUp(self):
        self.iterations = 1000
        self.square_range = 10**12
        self.relatively_prime_range = 100
        
    def test_square_random_positive_square(self):
        for _ in range(self.iterations):
            n = randint(1, self.square_range)
            self.assertTrue(is_square(n**2))

    def test_square_random_positive_not_square(self):
        for _ in range(self.iterations):
            m = randint(2, self.square_range)
            n = randint(m**2 + 1, (m + 1)**2 - 1)
            self.assertFalse(is_square(n))

    def test_square_random_negative(self):
        for _ in range(self.iterations):
            n = - randint(1, self.square_range)
            self.assertFalse(is_square(n))

    def test_square_zero(self):
        self.assertTrue(is_square(0))

    def test_relatively_prime_one_one_relatively_prime(self):
        add_all_pairs(1)
        self.assertTrue([1, 1] in get_pairs())

    def test_relatively_prime_random_relatively_prime(self):
        add_all_pairs(self.relatively_prime_range+1)
        for _ in range(self.iterations):
            a = randint(1, self.relatively_prime_range)
            b = randint(1, self.relatively_prime_range)
            d = gcd(a, b)
            a = a//d
            b = b//d
            if a > b:
                a, b = b, a
            self.assertTrue([a, b] in get_pairs())

    def test_relatively_prime_random_not_relatively_prime(self):
        add_all_pairs(self.relatively_prime_range+1)
        for _ in range(self.iterations):
            d = randint(2, isqrt(self.relatively_prime_range))
            a = d*randint(1, self.relatively_prime_range//d)
            b = d*randint(1, self.relatively_prime_range//d)
            if a > b:
                a, b = b, a
            self.assertTrue([a, b] not in get_pairs())

if __name__ == '__main__':
    main()

