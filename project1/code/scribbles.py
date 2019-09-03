from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from random import random, seed

import projectfunctions as pf

import seaborn as sns


sns.set()
sns.set_style("whitegrid")
sns.set_palette("husl")



fig = plt.figure()
ax = fig.gca(projection="3d")

# Generating grid in x,y in [0, 1] with n=100 points
n = 1000

x = np.linspace(0, 1, n)
y = np.linspace(0, 1, n)
x, y = np.meshgrid(x,y)

# generating design matrices for both coordinates
x_random = np.random.uniform(0, 1, n)
x_sorted = np.sort(x_random, axis=0)

y_random = np.random.uniform(0, 1, n)
y_sorted = y_random[np.argsort(x_random, axis=0)].flatten()

z = pf.frankefunction(x, y)

X = pf.generate_design_2Dpolynomial(x_sorted, y_sorted, degree=5)
z_model = pf.least_squares(X, z)

print(z)
print(z_model)
# Plot the surface.
surf = ax.plot_surface(x, y, z,
                        cmap=cm.coolwarm,
                        linewidth=0,
                        antialiased=False
                        )
surf = ax.plot_surface(x, y, z_model,
                        cmap=cm.Blues,
                        linewidth=0,
                        antialiased=False
                        )
# Customize the z axis.
ax.set_zlim(-0.10, 1.40)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
# Add a color bar which maps values to colors.
fig.colorbar(surf,
            shrink=0.5,
            aspect=5
            )
plt.show()
