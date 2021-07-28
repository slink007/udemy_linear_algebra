import numpy as np


class Vector(object):
    def __init__(self, elements):
        try:
            if not elements:
                raise ValueError
            # Better to use a list?  Would number of elements ever change?
            self.elements = np.array(elements)
            self.dimension = len(elements)
            if self.dimension < 2:
                raise IndexError

        except ValueError:
            raise ValueError("Require elements to form vector")
        except TypeError:
            raise TypeError("Elements must be within an iterable")
        except IndexError:
            raise IndexError("Vector requires at least two elements")


    def __iter__(self):
        self.index = 0
        return self


    def __next__(self):
        if self.index < self.dimension:
            e = self.elements[self.index]
            self.index += 1
            return e
        raise StopIteration


    def __str__(self):
        return 'Vector: {}'.format(self.elements)


    def __eq__(self, v):
        return self.elements == v.elements
