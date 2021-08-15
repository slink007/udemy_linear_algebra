import unittest
from vector import Vector
from matrix import Matrix


# unittest requires CamelCase
class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector([-1, 0, 1, 42])
        self.v2 = Vector([-1, 0, 1])
        self.v3 = Vector([-10, 1, 10])


    def tearDown(self):
        del self.v1
        del self.v2
        del self.v3


    def test_creation(self):
        # Verify that creation of an empty Matrix is not allowed
        self.assertRaises(IndexError, lambda: Matrix())

        # Verify cannot create matrix from a single number or a string
        self.assertRaises(TypeError, lambda: Matrix(-1))
        self.assertRaises(TypeError, lambda: Matrix(0))
        self.assertRaises(TypeError, lambda: Matrix(1.0))
        self.assertRaises(TypeError, lambda: Matrix('text'))

        # Verify cannot create matrix from list of numbers
        self.assertRaises(TypeError, lambda: Matrix([1, 2, 3]))

        # Verify that all items in list must be Vectors
        self.assertRaises(TypeError, lambda: Matrix([self.v1, 2, 3]))
        self.assertRaises(TypeError, lambda: Matrix([1, self.v1, 3]))
        self.assertRaises(TypeError, lambda: Matrix([self.v1, self.v1, 3]))
        self.assertIsInstance(Matrix([self.v1, self.v1, self.v1]), Matrix)

        # Verify that all Vectors must be of same size
        self.assertRaises(TypeError, lambda: Matrix([self.v1, self.v2]))

        # Verify that a Matrix can be created from a single Vector
        self.assertIsInstance(Matrix(self.v1), Matrix)

        # Verify Matrix attributes when created from single Vector
        m1 = Matrix(self.v1)
        self.assertEqual(m1.rows, 1)
        self.assertEqual(m1.columns, self.v1.dimension)

        # Verify Matrix attributes when created from list of Vectors
        v_list = [self.v2, self.v3, self.v2]
        m2 = Matrix(v_list)
        self.assertEqual(m2.rows, len(v_list))
        self.assertEqual(m2.columns, self.v2.dimension)

        # Verify correct creation from tuple of Vectors
        v_tup = (self.v2, self.v3, self.v2)
        m3 = Matrix(v_tup)
        self.assertEqual(m3.rows, len(v_tup))
        self.assertEqual(m3.columns, self.v2.dimension)


    def test_equal(self):
        # Verify Matrix not equal to non_Matrix object
        self.assertNotEqual(Matrix([self.v2, self.v3]), self.v2)
        self.assertNotEqual(Matrix([self.v2, self.v3]), None)
        self.assertNotEqual(Matrix([self.v2, self.v3]), [-1, 0, 1])

        # Verify that Matrices with different row quantities are not equal
        self.assertNotEqual(Matrix([self.v2, self.v3]),
                            Matrix([self.v2, self.v3, self.v2]))
        self.assertNotEqual(Matrix([self.v2, self.v3, self.v2]),
                            Matrix([self.v2, self.v3]))

        # Verify that Matrices with equal row quantities, but unequal column
        # quantities, are not equal.
        self.assertNotEqual(Matrix([Vector([-1, 0, 1]), Vector([2, 3, 4])]),
                            Matrix([Vector([-1, 0, 1, 2]),
                                    Vector([2, 3, 4, 5])]))

        # Verify that Matrices with equal row and column quantities, but
        # unequal content, are not equal.
        self.assertNotEqual(Matrix([self.v2, self.v3]),
                            Matrix([self.v2, self.v2]))

        # Verify that two equal Matrices are reported being equal
        self.assertEqual(Matrix([self.v2, self.v3]),
                         Matrix([self.v2, self.v3]))

if __name__ == "__main__":
    unittest.main()
