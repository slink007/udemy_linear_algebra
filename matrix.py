from vector import Vector


class Matrix(object):
    """
    A Matrix is a list of Vector objects.  Each row in the Matrix is a Vector.
    """
    
    def __init__(self, rows = None):
        if rows == None:
            raise IndexError("Need Vector or list of Vectors to form Matrix.")
        self.columns = 0
        self.rows = 0
        
        try:
            if (isinstance(rows, list) or isinstance(rows, tuple)):
                # All rows must be Vectors
                for r in rows:
                    assert isinstance(r, Vector)
                # All Vectors must be same size
                self.columns = rows[0].dimension
                for r in rows[1:]:
                    assert self.columns == r.dimension
                self.rows = len(rows)
                    
            if (isinstance(rows, Vector):
                self.columns = rows.dimension
                self.rows = 1
        except AssertionError:
            raise TypeError("Need Vector or list of Vectors and all Vectors" +\
                "must be same size.")

        # Input was not a Vector or list/tuple of Vectors
        if self.columns == 0:
            raise TypeError("Need Vector or list of Vectors")
