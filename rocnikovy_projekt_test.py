import rocnikovy_projekt
import pytest
import random
import math
import datetime

iterations = 1000
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



def test_evaluate_simple_square():
    solution = [2,7,6,
                9,5,1,
                4,3,8]
    
    assert rocnikovy_projekt.evaluate_square([2,    None, 6,
                                              None, 5,    None,
                                              4,    None, 8]) == solution
    
    assert rocnikovy_projekt.evaluate_square([2,    7,    None,
                                              None, 5,    None,
                                              None, 3,    8]) == solution
    
    assert rocnikovy_projekt.evaluate_square([None, 7,    None,
                                              9,    5,    1,
                                              None, 3,    None]) == solution

    

def test_evaluate_seven_squares_square():
    solution = [42025,  277729, 222121,
                360721, 180625, 529,
                139129, 83521,  319225]
    
    assert rocnikovy_projekt.evaluate_square([42025,  None,   222121,
                                              None,   180625, None,
                                              139129, None,   319225]) == solution
    
    assert rocnikovy_projekt.evaluate_square([42025,  277729, None,
                                              None,   180625, None,
                                              None,   83521,  319225]) == solution
    
    assert rocnikovy_projekt.evaluate_square([None,   277729, None,
                                              360721, 180625, 529,
                                              None,   83521,  None]) == solution

    

def test_evaluate_random_acegi_square():
    for _ in range(iterations):
        x = random.randint(1,square_range)
        y = random.randint(1,square_range)
        z = random.randint(1,square_range)

        solution = [2*x+1,          6*z-2*x-2*y+1,  2*y+1,
                    2*z-2*x+2*y+1,  2*z+1,          2*z+2*x-2*y+1,
                    4*z-2*y+1,      2*x+2*y-2*z+1,  4*z-2*x+1]
        
        assert rocnikovy_projekt.evaluate_square([2*x+1,None,2*y+1,None,2*z+1,None,4*z-2*y+1,None,4*z-2*x+1]) == solution


def test_evaluate_random_abehi_square():
    for _ in range(iterations):
        x = random.randint(1,square_range)
        y = random.randint(1,square_range)
        z = random.randint(1,square_range)

        solution = [2*x+1,          2*y+1,          6*z-2*x-2*y+1,
                    8*z-4*x-2*y+1,  2*z+1,          4*x+2*y-4*z+1,
                    2*x+2*y-2*z+1,  4*z-2*y+1,      4*z-2*x+1]
        
        assert rocnikovy_projekt.evaluate_square([2*x+1,2*y+1,None,None,2*z+1,None,None,4*z-2*y+1,4*z-2*x+1]) == solution



def test_evaluate_random_bdefh_square():
    for _ in range(3):
        x = random.randint(1,square_range)
        y = random.randint(1,square_range)
        z = random.randint(1,square_range)

        solution = [4*z-x-y+1,      2*x+1,          2*z-x+y+1,
                    2*y+1,          2*z+1,          4*z-2*y+1,
                    2*z+x-y+1,      4*z-2*x+1,      x+y+1]
        
        assert rocnikovy_projekt.evaluate_square([None,2*x+1,None,2*y+1,2*z+1,4*z-2*y+1,None,4*z-2*x+1,None]) == solution
    




