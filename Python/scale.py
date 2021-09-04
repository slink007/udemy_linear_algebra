import numpy as np
import matplotlib.pyplot as plt
import math
from linear import Vector, Matrix


def gen_circle(theta):
    '''
    Returns a Vector which contains a point on a circle.  Point is a function
    of theta.
    '''
    return Vector([math.cos(theta), math.sin(theta)])


# Build out the original circle.  Here the Matrix is composed of Vectors
# and each Vector has an x-value and y-value for a point on the circle.
angles = np.linspace(-np.pi, np.pi, 100)
circle = Matrix([gen_circle(x) for x in angles])
plt.plot([c[0] for c in circle], [c[1] for c in circle], 'o')

# An impure rotation matrix to stretch and rotate the original circle.
t1 = Matrix([Vector([1, 0]), Vector([1.25, 2])])

# Since Matrix is a collection of Vectors we can use the rotation matrix to
# scale each of them.
circle2 = circle.scale(t1)
plt.plot([c[0] for c in circle2], [c[1] for c in circle2], '-')

plt.axis([-3.0, 3.0, -2.5, 2.5])  # [xmin, xmax, ymin, ymax]
plt.legend(['original', 'scaled'])
plt.grid(linewidth = 0.5)
plt.show()
