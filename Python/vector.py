from numbers import Complex


class Vector(object):
    """
    A Vector is an ordered group of two or more numbers.
    """

    def __init__(self, elements):
        try:
            if not elements:
                raise ValueError
            # Better to use a list?  Would number of elements ever change?
            self.elements = tuple(elements)
            self.dimension = len(elements)
            if self.dimension < 2:
                raise IndexError

            # For my purposes a Vecctor contains only numbers
            for e in self.elements:
                assert (type(e) == int) or (type(e) == float)

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
        return 'Vector: {}'.format(self.elements)

    def __eq__(self, v):
        # Better to raise error instead of returning False?
        if self.dimension != v.dimension:
            return False
        return all([self.elements[i] == v.elements[i] for i, j in
                    enumerate(self.elements)])

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
        Returns a Vector where all elements are scaled up/down  by the
        constant 'k'.
        """
        if not isinstance(k, Complex):
            raise TypeError('Scalar needs to be a number')

        new_elements = [k * e for e in self.elements]
        return Vector(new_elements)
