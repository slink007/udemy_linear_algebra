from vector import Vector


class Matrix(object):
    """
    A Matrix is a list of Vector objects.  Each row in the Matrix is a Vector.
    """
    
    def __init__(self, rows = None):
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
                self.row_list = [rows,]
        except AssertionError:
            raise TypeError("Need Vector or list of Vectors and all Vectors" +\
                " must be same size.")

        # Input was not a Vector or list/tuple of Vectors
        if self.columns == 0:
            raise TypeError("Need Vector or list of Vectors")


    def __getitem__(self, i):
        return self.row_list[i]


    # Addition with '+' operator
    def __add__(self, m):
        if not isinstance(m, Matrix):
            raise TypeError("Matrix must add to Matrix")
        try:
            if self.rows != m.rows:
                raise IndexError
            new_rows = [self.row_list[i] + m.row_list[i] for i in 
                range(self.rows)]
        except IndexError:
            raise IndexError("Matrices must be same size to add")

        return Matrix(new_rows)
