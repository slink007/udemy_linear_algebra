import unittest
from linear import Vector, RandomVector, Matrix
from random import seed, randint


# unittest requires CamelCase
class TestVector(unittest.TestCase):
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    v3 = Vector([1, 2, 3, 4])
    v4 = Vector([1.0, 2.0, 3.0])
    v5 = Vector([1, 0, -1.0])
    v6 = Vector([3, complex(4, 5)])
    v7 = Vector([1, 2])

    
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

        # Verify that Vectors containing complex numbers can be added.
        self.assertEqual(self.v6 + self.v7, Vector([4, complex(6, 5)]))


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

        # Verify that Vectors containing complex numbers can be subtracted.
        self.assertEqual(self.v7 - self.v6, Vector([-2, complex(-2, -5)]))

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

        # Verify that dot product can be done when Vectors contain imaginary
        # numbers.
        self.assertEqual(self.v6 @ self.v7, complex(11, 10))

    def test_multiplication(self):
        # Verify that a Vector times a constant is treated as a scale
        # operation.
        self.assertEqual(self.v1 * 3, Vector([3, 6, 9]))

        # Verify that a Vector times another Vector results in the cross
        # product of the two Vectors.
        self.assertEqual(self.v1 * self.v2, self.v1 @ self.v2)

        # Verify that a Vector times a Matrix yields a Vector.
        m = Matrix([Vector([1, 2, 3]),
                    Vector([4, 5, 6]),
                    Vector([7, 8, 9])])
        self.assertEqual(self.v1 * m, Vector([30, 36, 42]))

        # Verify that Matrix must be correct size to multiply
        m = Matrix([Vector([1, 2, 3]),
                    Vector([4, 5, 6])])
        self.assertRaises(IndexError, lambda: self.v1 * m)

        # Verify that vector does not multiply with types which
        # are not a scalar, Vector, or Matrix.
        self.assertRaises(TypeError, lambda: self.v1 * [1, 2, 3])
        self.assertRaises(TypeError, lambda: self.v1 * 'text')
        self.assertRaises(TypeError, lambda: self.v1 * None)

    def test_magnitude(self):
        # Verify correct magnitude of a vector
        self.assertEqual(Vector([3, 4]).magnitude(), 5)
        self.assertEqual(Vector([6, -8]).magnitude(), 10)

    def test_angle(self):
        # Verify that another Vector is needed to find the angle
        self.assertRaises(TypeError, lambda: self.v1.angle(75))
        self.assertRaises(TypeError, lambda: self.v1.angle('string'))
        self.assertRaises(TypeError, lambda: self.v1.angle([2, 3, 4]))

        v1 = Vector([1, 2, -1])
        v2 = Vector([3, 1, 0])
        self.assertEqual(v1.angle(v2), 49.79703411343022)

    def test_unit(self):
        # Verify that we do not produce a unit vector from a vector that
        # has zero magnitude.
        zero = Vector([0, 0])
        self.assertRaises(ZeroDivisionError, lambda: zero.unit())

        # Verify that we can produce a unit vector.
        v = Vector([17.32, -10, -28])
        self.assertEqual(v.unit(), Vector([0.5033560169342258,
                                           -0.2906212568904306,
                                           -0.8137395192932058]))
        vu = v.unit()
        # Used AlmostEqual because Equal failed and said that
        # 0.99999999 != 1
        # Which is true, but c'mon man....
        self.assertAlmostEqual(vu.magnitude(), 1)


    def test_cross(self):
        # Verify that both Vectors need to be 3D to perform cross prod.
        self.assertRaises(IndexError, lambda: self.v1.cross(self.v7))
        self.assertRaises(IndexError, lambda: self.v7.cross(self.v1))
        self.assertRaises(IndexError, lambda: self.v1.cross(self.v3))
        self.assertRaises(IndexError, lambda: self.v3.cross(self.v1))

        # Verify that we can perform a cross product of two Vectors
        self.assertEqual(Vector([5, 3, -2]).cross(Vector([-1, 0, 3])),
            Vector([9, -13, 3]))


    def test_random_default(self):
        # Verify that a RandomVector is a Vector
        self.assertTrue(RandomVector(), Vector)
        
        # Verify that RandomVector defaults to 2 elements
        self.assertEqual(RandomVector().dimension, 2)
        
        # Verify that RandomVector defaults to using integers
        rv = RandomVector()
        for i in range(rv.dimension):
            with self.subTest(i):
                self.assertTrue(isinstance(rv.elements[i], int))


    def test_random_size(self):
        # Verify that size cannot be set too small
        self.assertRaises(ValueError, lambda: RandomVector(1))
        self.assertRaises(ValueError, lambda: RandomVector(0))
        self.assertRaises(ValueError, lambda: RandomVector(-1))

        # Verify that element quantity can be set
        i = 0
        seed()
        while i < 3:
            i = randint(3, 100)
        self.assertEqual(RandomVector(i).dimension, i)
        
        # Verify that setting fill types works
        rv = RandomVector(3, 'int')
        for i in range(rv.dimension):
            with self.subTest(i):
                self.assertTrue(isinstance(rv.elements[i], int))
        rv = RandomVector(3, 'float')
        for i in range(rv.dimension):
            with self.subTest(i):
                self.assertTrue(isinstance(rv.elements[i], float))

if __name__ == "__main__":
    unittest.main()
