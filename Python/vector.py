from numbers import Complex
import math


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
        # Better to limit number of digits to 3 or 4?
        return 'Vector: {}'.format(self.elements)

    def __eq__(self, v):
        if self.dimension != v.dimension:
            return False
        length = len(self.elements)
        # Gets complicated (no pun intended) due to complex numbers.
        # If numbers are within 6 sig. figures we're saying they're equal.
        return all([(math.isclose(self.elements[i].real, v.elements[i].real, 
            abs_tol=10**-6) and math.isclose(self.elements[i].imag, 
            v.elements[i].imag, abs_tol=10**-6)) for i in range(length)])

    # Addition with '+' operator
    def __add__(self, v):
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        if self.dimension != v.dimension:
            raise IndexError("Vectors must be same size.")
        temp = [self.elements[i] + v.elements[i] for i, j in
                enumerate(self.elements)]
        return Vector(temp)

    # Subtraction with '-' operator
    def __sub__(self, v):
        if not isinstance(v, Vector):
            raise TypeError("Other item must be Vector")
        return self.__add__(v.scale(-1))

    # Dot product with '@' operator
    def __matmul__(self, v):
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
        first = (self.elements[1] * v.elements[2]) -\
            (self.elements[2] * v.elements[1])
        second = (self.elements[2] * v.elements[0]) -\
            (self.elements[0] * v.elements[2])
        third = (self.elements[0] * v.elements[1]) -\
            (self.elements[1] * v.elements[0])
        return Vector([first, second, third])
