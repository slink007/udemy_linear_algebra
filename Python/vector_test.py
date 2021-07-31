import unittest
from vector import Vector


# unittest requires CamelCase
class TestVector(unittest.TestCase):
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    v3 = Vector([1, 2, 3, 4])
    
    # unittest requires all methods begin with 'test_'
    def test_creation(self):
        self.assertRaises(IndexError, lambda: Vector([1,]))
        self.assertRaises(TypeError, lambda: Vector(1))
        self.assertRaises(ValueError, lambda: Vector(None))


    def  test_addition(self):
        self.assertEqual(self.v1 + self.v2, Vector([5, 7, 9]))
        self.assertEqual(self.v2 + self.v1, Vector([5, 7, 9]))
        # The lambda is required because without it the exception
        # is raised before unittest can look for it and the test
        # fails.
        self.assertRaises(IndexError, lambda: self.v1 + self.v3)
        self.assertRaises(IndexError, lambda: self.v3 + self.v1)

