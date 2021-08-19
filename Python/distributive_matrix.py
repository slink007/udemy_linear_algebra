# Quick test to determine if matrix scaling is distributive or not.

from vector import RandomVector
from matrix import Matrix
import random


def compare(k, m1, m2):
    m3 = m1 + m2
    print("k(M1 + M2) is ", end='')
    if m3.scale(k) != (m1.scale(k) + m2.scale(k)):
        print("not ", end='')
    print("equal to kM1 + kM2")


random.seed()
for _ in range(10):
    k = random.randint(-20, 20)
    m1 = Matrix([RandomVector(3), RandomVector(3), RandomVector(3)])
    m2 = Matrix([RandomVector(3), RandomVector(3), RandomVector(3)])
    compare(k, m1, m2)
