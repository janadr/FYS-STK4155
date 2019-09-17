from sklearn.utils import shuffle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from random import random, seed

import projectfunctions as pf

def plot_mseVSdegree(n, max_degree, reg, hyperparam, k=10,noise=1):

    degrees = np.arange(1,max_degree+1)

    x_val = np.linspace(0,1,n)
    y_val = np.linspace(0,1,n)

    #making an x and y grid
    x_grid, y_grid = np.meshgrid(x_val, y_val)

    #flatten x and y
    x = x_grid.flatten()
    y = y_grid.flatten()

    #compute z and flatten it
    #z_grid = pf.frankefunction(x_grid, y_grid, noise=error)*5
    z_grid = pf.frankefunction(x, y, noise=noise)
    z = z_grid.flatten()

    k_fold_mse = []
    k_fold_bias = []
    k_fold_r2 = []
    k_fold_var = []
    mse = []

    for degree in degrees:
        """Performing a k-fold cross-validation on training data"""
        evaluation_scores = pf.k_fold_cross_validation(x,y,z, reg, degree=degree,hyperparam=hyperparam,k=k)

        """Calculate bias, variance r2 and mse"""
        k_fold_mse.append(evaluation_scores[0])
        k_fold_r2.append(evaluation_scores[1])
        k_fold_bias.append(evaluation_scores[2])
        k_fold_var.append(evaluation_scores[3])


        """Simple training with no folds for comparison"""
        X = pf.generate_design_2Dpolynomial(x, y, degree)
        beta = reg(X, z, hyperparam=hyperparam)
        z_model = X @ beta


        #computing the MSE when no train test split is used
        mse.append(pf.mse(z, z_model))

    plt.figure()
    plt.plot(degrees, k_fold_var,'--',
        label="variance"
        )
    plt.plot(degrees, k_fold_bias,'--',
        label="bias"
        )

    plt.plot(degrees, k_fold_mse,
        label="test mse")
    plt.plot(degrees, mse,
        label="training mse"
        )
    plt.plot(degrees, np.array(k_fold_var) + np.array(k_fold_bias),
        label="variance + bias"
        )
    plt.xlabel("degrees")
    plt.legend()

    plt.figure()
    plt.plot(degrees, k_fold_mse,
            label="test mse")
    plt.plot(degrees, mse,
        label="training mse"
        )

    plt.xlabel("degrees")
    plt.legend()

n = 50
noise = 1
k = 10
reg = pf.ridge_regression
max_degree = 7

plot_mseVSdegree(n, max_degree, reg, hyperparam=0)
plot_mseVSdegree(n, max_degree, reg, hyperparam=1)
plot_mseVSdegree(n, max_degree, reg, hyperparam=2)
plot_mseVSdegree(n, max_degree, reg, hyperparam=3)

plt.show()
