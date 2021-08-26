# Quick test to determine if matrix trace is linear or not.

from linear import RandomVector, Matrix
import random


def compare_trace(m1, m2):
    m3 = m1 + m2
    tr_a = m1.trace()
    tr_b = m2.trace()
    tr_c = m3.trace()
    print("{} + {} == {} : {}".format(tr_a, tr_b, tr_c, (tr_a + tr_b) == tr_c))

def compare_scale(k, m1):
    m2 = m1.scale(k)
    tr_a = m2.trace()
    print("{} == {} : {}".format(tr_a, k * m1.trace(), tr_a == k * m1.trace()))

random.seed()
for _ in range(10):
    k = random.randint(-20, 20)
    m1 = Matrix([RandomVector(3), RandomVector(3), RandomVector(3)])
    m2 = Matrix([RandomVector(3), RandomVector(3), RandomVector(3)])
    compare_trace(m1, m2)
    compare_scale(k, m1)
    print('')
