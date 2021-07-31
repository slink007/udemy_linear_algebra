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

        # Verify that vectors have to be the same size to be added.
        self.assertRaises(IndexError, lambda: self.v1 + self.v3)
        self.assertRaises(IndexError, lambda: self.v3 + self.v1)

if __name__ == "__main__":
    unittest.main()
