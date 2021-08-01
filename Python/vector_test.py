import unittest
from vector import Vector


# unittest requires CamelCase
class TestVector(unittest.TestCase):
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    v3 = Vector([1, 2, 3, 4])
    v4 = Vector([1.0, 2.0, 3.0])
    v5 = Vector([1, 0, -1.0])
    
    # unittest requires all methods begin with 'test_'
    def test_creation(self):
        # Verify that we need an iterable of at least length 2
        self.assertRaises(IndexError, lambda: Vector([1,]))

        # Verify that we need an iterable to form a Vector
        self.assertRaises(TypeError, lambda: Vector(1))

        # Verify that Vector isn't created on None input
        self.assertRaises(ValueError, lambda: Vector(None))

        # Verify that all members of iterable are numbers
        self.assertRaises(TypeError, lambda: Vector([1, '1']))
        self.assertRaises(TypeError, lambda: Vector([1, None, 2]))
        self.assertRaises(TypeError, lambda: Vector("string"))

        # Examples of normal Vector creation
        self.assertEqual(Vector([1, 2, 3]), self.v1)
        self.assertEqual(Vector([1.0, 2.0, 3.0]), self.v4)
        self.assertEqual(Vector([1, 0, -1.0]), self.v5)


    def test_addition(self):
        # Verify we can add Vectors.
        self.assertEqual(self.v1 + self.v2, Vector([5, 7, 9]))
        self.assertEqual(self.v2 + self.v1, Vector([5, 7, 9]))
        self.assertEqual(self.v1 + self.v5, Vector([2, 2, 2.0]))

        # Verify that vectors have to be the same size to be added.
        self.assertRaises(IndexError, lambda: self.v1 + self.v3)
        self.assertRaises(IndexError, lambda: self.v3 + self.v1)

        # Verify that Vectors cannot add other iterable types
        self.assertRaises(TypeError, lambda: self.v1 + [3, 4, 5])


    def test_subtraction(self):
        # Verify we can subtract Vectors.
        self.assertEqual(self.v1 - self.v2, Vector([-3, -3, -3]))
        self.assertEqual(self.v2 - self.v1, Vector([3, 3, 3]))
        self.assertEqual(self.v1 - self.v5, Vector([0, 2, 4.0]))

        # Verify that vectors have to be the same size to be subtracted.
        self.assertRaises(IndexError, lambda: self.v1 - self.v3)
        self.assertRaises(IndexError, lambda: self.v3 - self.v1)

        # Verify that Vectors cannot subtract other iterable types
        self.assertRaises(TypeError, lambda: self.v1 - [3, 4, 5])


    def test_scale(self):
        # Verify that scalar must be a number
        x = [6, 7]
        y = tuple(x)
        self.assertRaises(TypeError, lambda: self.v1.scale('x'))
        self.assertRaises(TypeError, lambda: self.v1.scale(x))
        self.assertRaises(TypeError, lambda: self.v1.scale(y))

        # Verify that Vectors can be scaled up/down
        self.assertEqual(self.v1.scale(2), Vector([2, 4, 6]))
        self.assertEqual(self.v1.scale(0.5), Vector([0.5, 1.0, 1.5]))

    def test_dot_prod(self):
        # Verify a Vector is needed for dot product
        self.assertRaises(TypeError, lambda: self.v1 @ [1, 2, 3])
        self.assertRaises(TypeError, lambda: self.v1 @ 'string')
        self.assertRaises(TypeError, lambda: self.v1 @ tuple([1, 2, 3]))
        self.assertRaises(TypeError, lambda: self.v1 @ 3.14)

        # Verify that Vectors must be same size for dot product
        self.assertRaises(IndexError, lambda: self.v1 @ self.v3)
        self.assertRaises(IndexError, lambda: self.v3 @ self.v1)

        # Verify that dot product can be done on two Vectors
        self.assertEqual(self.v1 @ self.v2, 32)


if __name__ == "__main__":
    unittest.main()