"""
From the Udemy course 'Complete linear algebra: theory and implementation'.
The code challenge is from Video 17.

The idea is to see if Vector dot product sign will change based on scaling
a Vector.  The directions said to generate two 3-element Vectors and find
the dot products.  Then we want to scale both Vectors, find the dot
products again, and see if the sign has changed.

I am reusing code from previous challenges so I have lists of Vectors.  I
also have random numbers in my Vectors even though the challenge doesn't
specify that.

Result:  If both Vectors are scaled by the same amount then polarity does not
change.  If only one Vector is scaled then polarity WILL change if that scale
is negative but will NOT change if that scale is positive.
"""
from random import seed, gauss, randint
from linear import Vector

NUMBER_VECTORS = 6
NUMBER_VALUES = 3

seed(randint(0, 10))


def gen_matrix():
    matrix = []
    for vector in range(NUMBER_VECTORS):
        elements = []
        for value in range(NUMBER_VALUES):
            elements.append(10 * gauss(0, 1))
        matrix.append(Vector(elements))
    return matrix


def scale_matrix(matrix, k):
    """
    The 'matrix' input is really a list of Vectors.
    This scales each Vector by the constant 'k' and puts the new Vector
    into a new matrix.  The new matrix is returned.
    """
    new_matrix = []
    for v in range(NUMBER_VECTORS):
        new_matrix.append(matrix[v].scale(k))
    return new_matrix


def list_of_signs(base_dot_prods):
    base_signs = []
    for bdp in base_dot_prods:
        if bdp > 0:
            base_signs.append('pos.')
        elif bdp < 0:
            base_signs.append('neg.')
        else:
            base_signs.append('zero')
    return base_signs

def test(scale):
    m1 = gen_matrix()
    m2 = gen_matrix()
    m3 = scale_matrix(m1, scale)
    m4 = scale_matrix(m2, scale)

    base_dot_prods = [m1[v] @ m2[v] for v in range(NUMBER_VECTORS)]
    scaled_dot_prods = [m3[v] @ m4[v] for v in range(NUMBER_VECTORS)]
    mixed_dot_prods = [m1[v] @ m4[v] for v in range(NUMBER_VECTORS)]

    msg = "Scaling two Vectors by {} does not change the sign of their" + \
          " resulting dot product: {}"
    print(msg.format(scale, list_of_signs(base_dot_prods) == list_of_signs(scaled_dot_prods)))
    msg2 = "Scaling a single Vector by {} does not change the sign of the resulting" +\
           " dot product: {}\n"
    print(msg2.format(scale, list_of_signs(base_dot_prods) == list_of_signs(mixed_dot_prods)))

if __name__ == "__main__":
    scales = [-5, -4, -3, -2, -1, 2, 3, 4, 5]
    for s in scales:
        test(s)
