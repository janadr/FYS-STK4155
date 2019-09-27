'''
Brukt Anna Linas k-fold cross-validation kode og implementert bias variance
'''
from sklearn.utils import shuffle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from random import random, seed

import projectfunctions as pf

'''
plotter feil mot kompleksitet
'''
#np.random.seed(108)
n = 60
error = 0.1
degrees = np.arange(1,15)

x_random = np.random.uniform(0, 1, n)
#x_sorted = np.sort(x_random, axis=0)
x_sorted = np.linspace(0,1,n)

y_random = np.random.uniform(0, 1, n)
#y_sorted = np.sort(y_random,axis=0)
y_sorted = np.linspace(0,1,n)
#making an x and y grid
x_grid, y_grid = np.meshgrid(x_sorted, y_sorted)

#flatten x and y
x = x_grid.flatten()
y = y_grid.flatten()

#compute z and flatten it
z_grid = pf.frankefunction(x_grid, y_grid) + np.random.normal(0,np.sqrt(error),(n,n))
z = z_grid.flatten()

k_fold_mse = []
k_fold_bias = []
k_fold_r2 = []
k_fold_var = []
mse = []

'''

print("degree |  mse  | bias  |  var  |")
for degree in degrees:
    """Performing a k-fold cross-validation on training data"""
    #evaluation_scores = k_fold_cross_validation(x,y,z,degree)
    evaluation_scores, beta = pf.k_fold_cross_validation(x,y,z,pf.least_squares,degree=degree)

    """Calculate bias, variance r2 and mse"""

    k_fold_mse.append(evaluation_scores[0])
    k_fold_r2.append(evaluation_scores[1])
    k_fold_bias.append(evaluation_scores[2])
    k_fold_var.append(evaluation_scores[3])


    """Simple training with no folds for comparison"""
    X = pf.generate_design_2Dpolynomial(x, y, degree)


    beta = pf.least_squares(X,z)
    z_model = X @ beta

    #computing the MSE when no train test split is used
    mse.append(pf.mse(z, z_model))
    print(f"{degree:6.0f} | {k_fold_mse[-1]:5.3f} | {k_fold_bias[-1]:5.3f} | \
{k_fold_var[-1]:5.3f}")


plt.plot(degrees, k_fold_var,'--',
        label="variance"
        )
plt.plot(degrees, k_fold_bias,'--',
        label="bias"
        )

plt.plot(degrees, mse,
        label="regular mse training"
        )
plt.plot(degrees, k_fold_mse,
        label="total error w/testing"
        )

plt.xlabel("degrees")
plt.legend()
plt.title(f"Least Squares: Error, bias and variance for n={n}, $\sigma^2$ = {error}")
#plt.savefig("../selected results/fig1.pdf")
plt.show()

'''
plt.figure(3)
X = pf.generate_design_2Dpolynomial(x, y)

beta = pf.least_squares(X,z)
z_model = X @ beta

#var_beta = pf.variance(z_model)*np.linalg.pinv(X.T.dot(X))
weight = np.sqrt( np.diag( np.linalg.inv(X.T.dot(X))))*1.96
plt.errorbar(np.arange(1,len(beta)+1), beta, yerr=2*weight,fmt='o',label=f"beta confidence interval")
#plt.plot(np.arange(1,len(beta)+1),beta,'r-',label=f"beta-values")
plt.legend()
#plt.xlabel("$\beta$-value index")
plt.show()

###3D plot ###
'''
# Plot the surfacese
fig = plt.figure(2)
ax = fig.gca(projection="3d")

#reshape z_model to matrices so it can be plottet as a surface
z_model_grid = np.reshape(z_model,(n,n))

surf = ax.plot_surface(x_grid, y_grid, z_model_grid,
                        cmap=cm.Blues,
                        linewidth=0,
                        antialiased=False,
                        alpha = 0.5,
                        )

ax.scatter(x_grid, y_grid, z_grid,
                        #cmap=cm.coolwarm,
                        linewidth=0,
                        antialiased=False,
                        marker = '.',
                        s = 0.1,
                        label="data",
                        c='k'
                        )

# Customize the z axis.
ax.set_zlim(-0.10, 1.40)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
# Add a color bar which maps values to colors.
fig.colorbar(surf,
            shrink=0.5,
            aspect=5,
            label="model"
            )

ax.legend()
plt.show()
'''
