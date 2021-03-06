import unittest
import cmath
from linear import Vector, Matrix


# unittest requires CamelCase
class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector([-1, 0, 1, 42])
        self.v2 = Vector([-1, 0, 1])
        self.v3 = Vector([-10, 1, 10])
        self.m1 = Matrix([self.v2, self.v3])
        self.m2 = Matrix([self.v2, self.v3])
        self.m3 = Matrix([self.v2, self.v3, self.v3])
        self.m4 = Matrix([self.v1, self.v1])
        self.m5 = Matrix([self.v2, self.v2])
        self.m6 = Matrix([self.v3, self.v3])


    def tearDown(self):
        del self.v1
        del self.v2
        del self.v3
        del self.m1
        del self.m2
        del self.m3
        del self.m4
        del self.m5
        del self.m6


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


    def test_add(self):
        # Verify that Matrices can only add to other Matrices
        self.assertRaises(TypeError, lambda: self.m1 + 1)
        self.assertRaises(TypeError, lambda: self.m1 + -1.0)
        self.assertRaises(TypeError, lambda: self.m1 + 'text')
        self.assertRaises(TypeError, lambda: self.m1 + None)
        self.assertRaises(TypeError, lambda: self.m1 + self.v1)

        # Verify that Matrices with diff. rows do not add
        self.assertRaises(IndexError, lambda: self.m2 + self.m3)
        self.assertRaises(IndexError, lambda: self.m3 + self.m2)

        # Verify that Matrices with same number of rows, but diff.
        # number of columns, do not add.
        self.assertRaises(IndexError, lambda: self.m2 + self.m4)
        self.assertRaises(IndexError, lambda: self.m4 + self.m2)

        # Verify that Matrices of like size do add
        self.assertEqual(Matrix([Vector([-1, 0, 1]), Vector([2, 3, 4])]) +
                         Matrix([Vector([5, 6, 7]), Vector([8, 9, 10])]),
                         Matrix([Vector([4, 6, 8]), Vector([10, 12, 14])]))


    def test_scale(self):
        # Verify that non-numeric scales are not permitted
        self.assertRaises(TypeError, lambda: self.m1.scale('text'))
        self.assertRaises(TypeError, lambda: self.m1.scale([1, 2, 3]))
        self.assertRaises(TypeError, lambda: self.m1.scale(None))

        # Verify that Matrix scales correctly
        self.assertEqual(self.m1.scale(2), Matrix([Vector([-2, 0, 2]),
                                                   Vector([-20, 2, 20])]))

        # Verify that when scaling one Matrix with another, the other Matrix
        # is multiplied by each row within the original Matrix.
        v = Vector([1, 2])
        w = Vector([3, 4])
        x = Vector([5, 6])
        y = Vector([7, 8])
        m = Matrix([v, w])
        n = Matrix([x, y])
        self.assertEqual(m.scale(n), Matrix([Vector([17, 23]),
                                             Vector([39, 53])]))

    def test_subtract(self):
        # Subtraction is primarily done in the addition method (after scaling
        # by -1) so not much testing here.
        self.assertEqual(self.m5 - self.m6, Matrix([Vector([9, -1, -9]),
                                                    Vector([9, -1, -9])]))


    def test_multiply(self):
        # Verify that multiplication with another Matrix does not happen if
        # dimensions are wrong.
        self.assertRaises(IndexError, lambda: self.m1 * self.m1)

        # Verify that multiplication with another Matrix does happen if
        # dimensions are correct.
        self.assertEqual(self.m1 * self.m3, Matrix([Vector([-9, 1, 9]),
                                                    Vector([-100, 11, 100])]))

        # Verify that multiplication with a Vector does not happen if the
        # Vector size is wrong.
        self.assertRaises(IndexError, lambda: self.m1 * Vector([2, 3]))

        # Verify that multiplication with a Vector does happen if the Vector
        # is correctly sized
        v = Vector([1, 2, 3])
        w = Vector([4, 5, 6])
        x = Vector([7, 8, 9])
        m = Matrix([v, w, x])
        self.assertEqual(m * v, Vector([14, 32, 50]))

    def test_identity(self):
        v = Vector([1, 2, 3])
        w = Vector([4, 5, 6])
        x = Vector([7, 8, 9])
        m1 = Matrix([v, w])
        m2 = Matrix([v, w, x])
        
        # Verify we do not create identity Matrix from non-square Matrix
        self.assertRaises(TypeError, lambda: m1.identity())

        # Verify that identity Matrix is correctly created
        self.assertEqual(m2.identity(), Matrix([Vector([1, 0, 0]),
                                                Vector([0, 1, 0]),
                                                Vector([0, 0, 1])]))


    def test_shift(self):
        # Feature builds entirely off of other features tested here so only
        # verify that the basic functionality works.
        v = Vector([1, 2])
        w = Vector([2, 4])
        m1 = Matrix([v, w])
        self.assertEqual(m1.shift(3), Matrix([Vector([4, 2]),
                                              Vector([2, 7])]))

    def test_transpose(self):
        v = Vector([1, 2, 3, 4])
        w = Vector([5, 6, 7, 8])
        m = Matrix([v, w])

        # Verify that rows and columns are swapped.
        self.assertEqual(m.transpose(), Matrix([Vector([1, 5]),
                                                Vector([2, 6]),
                                                Vector([3, 7]),
                                                Vector([4, 8])]))

    def test_ht(self):
        v = Vector([1, 2, complex(3, 4), 4])
        w = Vector([5, 6, 7, 8])
        m = Matrix([v, w])

        # Verify that rows and columns are swapped and that complex
        # numbers are correctly adjusted.
        self.assertEqual(m.ht(), Matrix([Vector([1, 5]),
                                         Vector([2, 6]),
                                         Vector([complex(3, -4), 7]),
                                         Vector([4, 8])]))


    def test_diagonal(self):
        # Verify diagonal from rectangular Matrix
        self.assertEqual(self.m1.diagonal(), Vector([-1, 1]))

        # Verify diagonal from square Matrix
        self.assertEqual(self.m3.diagonal(), Vector([-1, 1, 10]))


    def test_trace(self):
        # Verify that trace not valid on rectangular Matrix
        self.assertRaises(TypeError, lambda: self.m1.trace())

        # Verify trace feature on square Matrix
        self.assertEqual(self.m3.trace(), 10)

if __name__ == "__main__":
    unittest.main()
