from vector import Vector


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
