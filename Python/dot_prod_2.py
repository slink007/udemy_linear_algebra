"""
From the Udemy course 'Complete linear algebra: theory and implementation'.
The code challenge is from Video 14.

The idea is to see if Vector dot products are commutative or not.  The
directions said to generate two 100-element Vectors with random elements
and find the dot products (V1 dot V2 and V2 dot V1).  I chose to not do 
it that way as we don't submit these for grades and most of the work
is already done in dot_prod_1.py.  

Now we simply do the dot products and visually inspect the results.
"""
from random import seed
from random import gauss
from random import randint
from vector import Vector


NUMBER_VECTORS = 6
NUMBER_VALUES = 4

seed(randint(0, 10))

def gen_matrix():
    matrix = []
    for vector in range(NUMBER_VECTORS):
        elements = []
        for value in range(NUMBER_VALUES):
            elements.append(10 * gauss(0, 1))
        matrix.append(Vector(elements))
    return matrix


m1 = gen_matrix()
m2 = gen_matrix()

print("First set:\n{}\n".format([m1[v] @ m2[v] for v in range(NUMBER_VECTORS)]))
print("Second set:\n{}".format([m2[v] @ m1[v] for v in range(NUMBER_VECTORS)]))
