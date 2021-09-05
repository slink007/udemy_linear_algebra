from random import seed, randint
from linear import RandomVector, Matrix


def is_symmectric(matrix):
    """
    Tests a matrix to determine if it symmectric or not.  Returns True if it is
    symmetric.
    """
    return matrix == matrix.transpose()

def form_symmetric(matrix):
    """
    Uses 'matrix' as a base to form a new symmetric matrix.  If successful
    returns the symmetric matrix.
    """
    return matrix + matrix.transpose()

def form_matrix(side):
    """
    Form a square matrix, of dimension side x side, which is filled with random
    integers.  Return the matrix.
    """
    vectors = []
    for _ in range(side):
        vectors.append(RandomVector(quantity=side))
    return Matrix(vectors)

def test_add():
    """
    Generate 10 pairs of symmetric matrices.  Tests to determine if their sum
    produces a symmetric matrix or not.
    """
    num_pass = 0
    for _ in range(10):
        side = randint(2, 11)
        m1 = form_symmetric(form_matrix(side))
        m2 = form_symmetric(form_matrix(side))
        if is_symmectric(m1 + m2):
            num_pass += 1
    print("Added 10 pairs of symmetric matrices and got " +
          "{} symmetric results.".format(num_pass))

def test_mult():
    """
    Generate 10 pairs of symmetric matrices.  Tests to determine if their
    product produces a symmetric matrix or not.
    """
    num_pass = 0
    for _ in range(10):
        side = randint(2, 11)
        m1 = form_symmetric(form_matrix(side))
        m2 = form_symmetric(form_matrix(side))
        if is_symmectric(m1 * m2):
            num_pass += 1
    print("Multiplied 10 pairs of symmetric matrices and got " +
          "{} symmetric results.".format(num_pass))

def test_hadamard():
    """
    Generate 10 pairs of symmetric matrices.  Tests to determine if their
    product produces a symmetric matrix or not.
    """
    num_pass = 0
    for _ in range(10):
        side = randint(2, 11)
        m1 = form_symmetric(form_matrix(side))
        m2 = form_symmetric(form_matrix(side))
        if is_symmectric(m1.hadamard(m2)):
            num_pass += 1
    print("Hadamard multiplication on 10 pairs of symmetric matrices and got " +
          "{} symmetric results.".format(num_pass))



if __name__ == "__main__":
    seed(randint(1, 11))
    test_add()
    test_mult()
    test_hadamard()
