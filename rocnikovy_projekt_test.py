import rocnikovy_projekt
import pytest
import subprocess
import sys
import os
import random


def test_random_positive_square():
    for _ in range(5000):
        n = random.randint(1,10**12)
        assert rocnikovy_projekt.is_square(n**2) is True

def test_random_positive_not_square():
    for _ in range(5000):
        m = random.randint(2,10**12)
        n = random.randint(m**2 + 1, (m + 1)**2 - 1)
        assert rocnikovy_projekt.is_square(n) is False

def test_random_negative():
    for _ in range(5000):
        n = - random.randint(1,10**12)
        assert rocnikovy_projekt.is_square(n) is False

def test_zero():
    assert rocnikovy_projekt.is_square(0) is True

