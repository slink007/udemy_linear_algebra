import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3-dimensional vector
v3 = [ 4, -3, 2 ]

# transpose into a vertical vector
v3t = np.transpose(v3)

fig = plt.figure(figsize=plt.figaspect(1))
ax = plt.axes(None, projection='3d')

# draw the vector
# origin is at (0, 0, 0)
# x-tail at element in v3[0]
# y-tail at element in v3[1]
# z-tail at element in v3[3]
ax.plot([0, v3[0]],[0, v3[1]],[0, v3[2]],linewidth=3)

# draw the axes and use dotted lines
ax.plot([0, 0],[0, 0],[-4, 4],'k--')
ax.plot([0, 0],[-4, 4],[0, 0],'k--')
ax.plot([-4, 4],[0, 0],[0, 0],'k--')

# show the plot on the screen
plt.show()

