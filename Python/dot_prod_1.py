"""
From the Udemy course 'Complete linear algebra: theory and implementation'.
The code challenge is from Video 13.

We are told to construct a couple of matrices.  Each matrix is assumed to be
a collection of column Vectors.  The matrices are 4 x 6, so that means each
will have 6 Vectors and each Vector will contain 4 elements.

The Vectors are to be filled with random numbers.  We want to compute the dot
products of the Vectors.  It would be first Vector of the first matrix dot first
Vector of the second matrix, then the second Vectors of each, and so on.

The original problem statement doesn't specify what to do with all of these
dot product results so I'm just putting them into a list.
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

print([m1[v] @ m2[v] for v in range(NUMBER_VECTORS)])