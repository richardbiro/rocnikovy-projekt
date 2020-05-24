from math import gcd, sqrt
from random import randint
from rocnikovy_projekt import is_square, add_all_pairs, get_pairs, evaluate_square
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
            self.assertTrue([a, b] in get_pairs())


    def test_relatively_prime_random_not_relatively_prime(self):
        add_all_pairs(self.relatively_prime_range+1)
        for _ in range(self.iterations):
            d = randint(2, int(sqrt(self.relatively_prime_range)))
            a = d*randint(1, self.relatively_prime_range//d)
            b = d*randint(1, self.relatively_prime_range//d)
            self.assertTrue([a, b] not in get_pairs())



    def test_evaluate_simple_square(self):
        solution = [2, 7, 6,
                    9, 5, 1,
                    4, 3, 8]
        
        self.assertTrue(evaluate_square([2, None, 6,
                                         None, 5, None,
                                         4, None, 8]) == solution)
        
        self.assertTrue(evaluate_square([2, 7, None,
                                         None, 5, None,
                                         None, 3, 8]) == solution)
        
        self.assertTrue(evaluate_square([None, 7, None,
                                         9, 5, 1,
                                         None, 3, None]) == solution)

        

    def test_evaluate_seven_squares_square(self):
        solution = [42025, 277729, 222121,
                    360721, 180625, 529,
                    139129, 83521, 319225]
        
        self.assertTrue(evaluate_square([42025, None, 222121,
                                         None, 180625, None,
                                         139129, None, 319225]) == solution)
        
        self.assertTrue(evaluate_square([42025, 277729, None,
                                         None, 180625, None,
                                         None, 83521, 319225]) == solution)
        
        self.assertTrue(evaluate_square([None, 277729, None,
                                         360721, 180625, 529,
                                         None, 83521, None]) == solution)

        

    def test_evaluate_random_acegi_square(self):
        for _ in range(self.iterations):
            x = randint(1, self.square_range)
            y = randint(1, self.square_range)
            z = randint(1, self.square_range)

            solution = [2*x+1, 6*z-2*x-2*y+1, 2*y+1,
                        2*z-2*x+2*y+1, 2*z+1, 2*z+2*x-2*y+1,
                        4*z-2*y+1, 2*x+2*y-2*z+1, 4*z-2*x+1]
            
            self.assertTrue(evaluate_square([2*x+1, None, 2*y+1,
                                             None, 2*z+1, None,
                                             4*z-2*y+1, None, 4*z-2*x+1]) == solution)


    def test_evaluate_random_abehi_square(self):
        for _ in range(self.iterations):
            x = randint(1, self.square_range)
            y = randint(1, self.square_range)
            z = randint(1, self.square_range)

            solution = [2*x+1, 2*y+1, 6*z-2*x-2*y+1,
                        8*z-4*x-2*y+1, 2*z+1, 4*x+2*y-4*z+1,
                        2*x+2*y-2*z+1, 4*z-2*y+1, 4*z-2*x+1]
            
            self.assertTrue(evaluate_square([2*x+1, 2*y+1, None,
                                             None, 2*z+1, None,
                                             None, 4*z-2*y+1, 4*z-2*x+1]) == solution)



    def test_evaluate_random_bdefh_square(self):
        for _ in range(self.iterations):
            x = randint(1, self.square_range)
            y = randint(1, self.square_range)
            z = randint(1, self.square_range)

            solution = [4*z-x-y+1, 2*x+1, 2*z-x+y+1,
                        2*y+1, 2*z+1, 4*z-2*y+1,
                        2*z+x-y+1, 4*z-2*x+1, x+y+1]
            
            self.assertTrue(evaluate_square([None, 2*x+1, None,
                                             2*y+1, 2*z+1, 4*z-2*y+1,
                                             None, 4*z-2*x+1, None]) == solution)
    


if __name__ == '__main__':
    main()

