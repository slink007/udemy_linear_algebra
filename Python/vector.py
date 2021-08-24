from numbers import Complex
import math
from random import seed, randint, random
from matrix import Matrix


class Vector(object):
    """
    A Vector is an ordered group of two or more numbers.
    """

    def __init__(self, elements):
        try:
            if not elements:
                raise ValueError
            # Better to use a list?  Would number of elements ever change?
            # If not maybe scale method could just alter the current Vector
            # in place.
            self.elements = tuple(elements)
            self.dimension = len(elements)
            if self.dimension < 2:
                raise IndexError

            # For my purposes a Vector contains only numbers
            for e in self.elements:
                assert isinstance(e, Complex)

        except ValueError:
            raise ValueError("Require elements to form vector")
        except TypeError:
            raise TypeError("Elements must be within an iterable")
        except IndexError:
            raise IndexError("Vector requires at least two elements")
        except AssertionError:
            raise TypeError("All elements must numbers")

        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index < self.dimension:
            return self.elements[self.index]
        raise StopIteration

    def __str__(self):
        string = "Vector: ("
        string += '{}, '.format(self.elements[0])
        # string += '{:.4e}, '.format(self.elements[0])
        for e in self.elements[1:]:
            string += '{}, '.format(e)
            # string += '{:.4e}, '.format(e)
        return string[:-2] + ")"

    def __eq__(self, v):
        """
        Determines if two Vectors are equal or not.  Rounds off to 6
        significant figures so if things are "close enough", like
        comparing 0.999 and 1, returns True.
        """
        if (isinstance(v, Vector)):
            if self.dimension != v.dimension:
                return False
            length = len(self.elements)
            return all([(math.isclose(self.elements[i].real, v.elements[i].real,
                                      abs_tol=10 ** -6) and math.isclose(self.elements[i].imag,
                                                                         v.elements[i].imag, abs_tol=10 ** -6)) for i in
                        range(length)])
        return False

    def __getitem__(self, i):
        return self.elements[i]

    def __add__(self, v):
        """
        Use '+' operator to add Vectors.  Result is returned as a new Vector
        whose elements are the sum of this Vector's elements and the elements
        of Vector 'v'.
        """
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        if self.dimension != v.dimension:
            raise IndexError("Vectors must be same size.")
        temp = [self.elements[i] + v.elements[i] for i, j in
                enumerate(self.elements)]
        return Vector(temp)

    def __sub__(self, v):
        """
        Use '-' operator to subtract Vectors.  Result is returned as a new
        Vector whose elements are the difference of this Vector's elements and
        the elements of Vector 'v'.
        """
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        return self.__add__(v.scale(-1))

    def __mul__(self, m):
        """
        Use '*' operator to multiply things with this Vector.  If 'm' is a
        Matrix then post-multiply it with this Vector.  If 'm' is a Vector
        then return the dot product of this Vector and 'm'.  If 'm' is
        neither a Vector nor a Matrix then attempt to scale this Vector by
        'm'.
        """
        if isinstance(m, Vector):
            return self.__matmul__(m)
        elif isinstance(m, Matrix):
            if m.rows != self.dimension:
                raise IndexError("Matrix is wrong size")

            # Extract vectors from Matrix
            vectors = []
            for c_index in range(m.columns):
                values = [m[r_index][c_index] for r_index in range(m.rows)]
                vectors.append(Vector(values))

            # Make a list of dot products
            products = [self.__matmul__(v) for v in vectors]
            return Vector(products)
        else:
            return self.scale(m)

    def __matmul__(self, v):
        """
        Use '@' operator to perform a dot product on two Vectors.  Result is
        returned as an integer.
        """
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        if self.dimension != v.dimension:
            raise IndexError("Vectors must be same size")
        return sum([self.elements[i] * v.elements[i] for i in
                    range(self.dimension)])

    def scale(self, k):
        """
        Returns a Vector where all elements are scaled up/down by the
        constant 'k'.
        """
        if not isinstance(k, Complex):
            raise TypeError('Scalar needs to be a number')

        new_elements = [k * e for e in self.elements]
        return Vector(new_elements)

    def magnitude(self):
        """
        Finds the magnitude of the Vector and returns it.
        """
        return math.sqrt(self.__matmul__(Vector(self.elements)))

    def angle(self, v):
        """
        Finds the angle between this Vector and Vector 'v'
        and returns it in degrees.
        """
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        top = self.__matmul__(v)
        bottom = self.magnitude() * v.magnitude()
        angle = math.acos(top / bottom)
        # We express our angles in degrees, the way that God
        # intended for it to be.
        return math.degrees(angle)

    def unit(self):
        """
        Finds the unit vector which is aligned with this Vector and
        returns is as a new Vector object.
        """
        try:
            magnitude = self.magnitude()
            mu = 1 / magnitude
        except ZeroDivisionError:
            raise ZeroDivisionError("{} has no unit vector.".format(self))
        return self.scale(mu)

    def cross(self, v):
        """
        Returns a Vector which is the result of the cross product of
        this Vector and Vector 'v'.
        """
        SIZE_MSG = "Cross product only valid for 3D Vector"

        if self.dimension != 3 or v.dimension != 3:
            raise IndexError(SIZE_MSG)
        first = (self.elements[1] * v.elements[2]) - \
                (self.elements[2] * v.elements[1])
        second = (self.elements[2] * v.elements[0]) - \
                 (self.elements[0] * v.elements[2])
        third = (self.elements[0] * v.elements[1]) - \
                (self.elements[1] * v.elements[0])
        return Vector([first, second, third])


class RandomVector(Vector):
    """
    A RandomVector is like a Vector except that instead of specifying the
    contents we only specify the quantity of elements, and the type, and
    the RandomVector is filled with that quantity of the specified type of
    element.
    """

    def __init__(self, quantity=2, element_type='int'):
        try:
            assert isinstance(element_type, str)
            element_type = element_type.lower()
            assert element_type in ('int', 'float')
        except AssertionError:
            raise TypeError("{} is not a supported element type"
                            .format(element_type))
        if not isinstance(quantity, int):
            raise TypeError("Must use int for quantity")
        if quantity < 2:
            raise ValueError("Need at least 2 values")

        seed()
        if element_type == 'int':
            values = [randint(-100, 100) for _ in range(quantity)]
        else:
            values = [(-100.0 + (random() * 200.0)) for _ in range(quantity)]
        super().__init__(values)
