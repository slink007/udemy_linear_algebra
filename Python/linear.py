from numbers import Complex
import cmath
import math
from random import seed, randint, random


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
            # self.elements = tuple(elements)
            self.elements = list(elements)
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
                         abs_tol=10 ** -6) and
                         math.isclose(self.elements[i].imag, v.elements[i].imag,
                         abs_tol=10 ** -6)) for i in range(length)])
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


class Matrix(object):
    """
    A Matrix is a list of Vector objects.  Each row in the Matrix is a Vector.
    """

    def __init__(self, rows=None):
        if rows is None:
            raise IndexError("Need Vector or list of Vectors to form Matrix.")
        self.columns = 0
        self.rows = 0

        try:
            # Creation via list or tuple of Vectors
            if (isinstance(rows, list) or isinstance(rows, tuple)):
                # All rows must be Vectors
                for r in rows:
                    assert isinstance(r, Vector)
                # All Vectors must be same size
                self.columns = rows[0].dimension
                for r in rows[1:]:
                    assert self.columns == r.dimension
                self.rows = len(rows)
                self.row_list = [r for r in rows]

            # Creation via single Vector
            if (isinstance(rows, Vector)):
                self.columns = rows.dimension
                self.rows = 1
                self.row_list = [rows, ]
        except AssertionError:
            raise TypeError("Need Vector or list of Vectors and all Vectors" +
                            " must be same size.")

        # Input was not a Vector or list/tuple of Vectors
        if self.columns == 0:
            raise TypeError("Need Vector or list of Vectors")

    def __getitem__(self, i):
        return self.row_list[i]

    def __str__(self):
        string = "Matrix:\n"
        for r in self.row_list:
            string += r.__str__()[8:]
            string += "\n"
        return string

    def __eq__(self, m):
        """
        Compare two matrices with == operator.  Return True if equal, False
        if not.
        """
        if not isinstance(m, Matrix):
            return False
        if self.rows != m.rows:
            return False
        comparison = [self.row_list[i] == m.row_list[i] for i in
                      range(self.rows)]
        return all(comparison)

    def __add__(self, m):
        """
        Adds this Matrix to Matrix M with the '+' operator.  Returns the result
        as a new Matrix.
        """
        if not isinstance(m, Matrix):
            raise TypeError("Other item must be a Matrix")
        try:
            if self.rows != m.rows:
                raise IndexError
            new_rows = [self.row_list[i] + m.row_list[i] for i in
                        range(self.rows)]
        except IndexError:
            raise IndexError("Matrices must be same size to add")

        return Matrix(new_rows)

    def scale(self, k):
        """
        Scales each element within this Matrix by the value 'k' and returns
        the result as a new Matrix.  Since each row of Matrix is a Vector we
        just let Vector code do the checking and scaling.  This includes
        letting TypeError bubble up in case 'k' is not a number.
        """
        new_rows = [r.scale(k) for r in self.row_list]
        return Matrix(new_rows)

    def __sub__(self, m):
        """
        Subtract Matrix 'm' from this Matrix with the '-' operator.
        Returns the result as a new Matrix.
        """
        return self.__add__(m.scale(-1))

    def __mul__(self, m):
        """
        Use '*' operator to multiply things with this Matrix.  If 'm' is a
        Matrix then post-multiply it with this Matrix.  If 'm' is a Vector
        then post-multiply it with this Matrix.  If 'm' is not a Vector or
        a Matrix then attempt to scale this Matrix with 'm'.
        """
        if isinstance(m, Vector):
            if self.columns != m.dimension:
                raise IndexError("Vector is wrong size")

            elements = [r @ m for r in self.row_list]
            return Vector(elements)
        elif isinstance(m, Matrix):
            if m.rows != self.columns:
                raise IndexError("Matrix is wrong size")

            # Column Vectors from 'm'
            vectors = []
            for c_index in range(m.columns):
                values = [m[r_index][c_index] for r_index in range(m.rows)]
                vectors.append(Vector(values))

            # Find products and build resulting Matrix
            new_rows = []
            for r in self.row_list:
                row = [r @ v for v in vectors]
                new_rows.append(Vector(row))
            return Matrix(new_rows)
        else:
            return self.scale(m)

    def _matrix_not_square(self):
        """
        Return True if this is not a square Matrix.  Return False if this is a
        square Matrix.
        """
        return self.columns != self.rows

    def identity(self):
        """
        Generates and returns an identity Matrix based on the dimensions of
        this Matrix.
        """
        if self._matrix_not_square():
            raise TypeError("Identity only valid on square Matrix")
        new_rows = []
        one_index = 0
        for r in self.row_list:
            temp = [0] * self.columns
            temp[one_index] = 1
            one_index += 1
            new_rows.append(Vector(temp))
        return Matrix(new_rows)

    def shift(self, k):
        """
        Uses constant 'k' to shift the Matrix.  Result is returned as new
        Matrix.
        """
        m1 = self.identity()
        return self.__add__(m1.scale(k))

    def transpose(self):
        """
        Determines the transpose of this Matrix and returns it as a new Matrix.
        The first row of this Matrix is the first column of the transpose, the
        second row of this Matrix is the second column of the transpose, and
        so on.

        This is NOT a Hermitian transpose.
        """
        new_rows = []
        for c in range(self.columns):
            temp = [self.row_list[r][c] for r in range(self.rows)]
            new_rows.append(Vector(temp))
        return Matrix(new_rows)

    def ht(self):
        """
        Determines the Hermitian transpose of this Matrix and returns it as
        a new Matrix.  The first row of this Matrix is the first column of
        the transpose, the second row of this Matrix is the second column
        of the transpose, and so on.
        """
        new_rows = []
        for c in range(self.columns):
            temp = [complex(self.row_list[r][c]).conjugate() for r in
                    range(self.rows)]
            new_rows.append(Vector(temp))
        return Matrix(new_rows)

    def diagonal(self):
        """
        Finds the diagonal of the Matrix and returns it as a Vector.
        """
        elements = []
        column_index = 0
        for r in range(self.rows):
            elements.append(self.row_list[r][column_index])
            column_index += 1
        return Vector(elements)

    def trace(self):
        """
        Finds the trace of the Matrix (sum of elements on the diagonal)
        and returns this as an integer/float (depends on what is on the
        diagonal).
        """
        if self._matrix_not_square():
            raise TypeError("Trace only valid on square Matrix")
        return sum(self.diagonal().elements)
