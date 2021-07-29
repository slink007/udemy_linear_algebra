class Vector(object):
    def __init__(self, elements):
        try:
            if not elements:
                raise ValueError
            # Better to use a list?  Would number of elements ever change?
            self.elements = tuple(elements)
            self.dimension = len(elements)
            if self.dimension < 2:
                raise IndexError
            base_type = type(self.elements[0])

            # While vectors can contain many types of elements all elements
            # within the same vector must be of the same type.
            for e in self.elements[1:]:
                assert base_type == type(e)

        except ValueError:
            raise ValueError("Require elements to form vector")
        except TypeError:
            raise TypeError("Elements must be within an iterable")
        except IndexError:
            raise IndexError("Vector requires at least two elements")
        except AssertionError:
            raise TypeError("All elements must be of the same type")

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


    def __add__(self, v):
        if self.dimension != v.dimension:
            raise IndexError("Vectors must be same size to be added.")
        temp = [self.elements[i] + v.elements[i] for i, j in
                enumerate(self.elements)]
        return Vector(temp)


if __name__ == "__main__":
    v1 = Vector([1, 2, 3])
    v2 = Vector([1, 2, 3])
    v3 = Vector([1, 2, 4])
    v4 = Vector([1, 2, 3, 4])
    print("v1 == v2: {}".format(v1 == v2))
    print("v1 == v3: {}".format(v1 == v3))
    print("v1 == v4: {}".format(v1 == v4))

    print(type(v1))
    print(v1)

    print(v1 + v2)
