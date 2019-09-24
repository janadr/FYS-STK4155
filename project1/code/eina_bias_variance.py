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


def k_fold_cross_validation(x, y, z, degree, k=10):
    mse = []
    r2 = []
    var = []
    bias = []

    #shuffle the data
    x_shuffle, y_shuffle, z_shuffle = shuffle(x, y, z, random_state=0)

    #split the data into k folds
    x_split = np.split(x_shuffle, k)
    y_split = np.split(y_shuffle, k)
    z_split = np.split(z_shuffle, k)

    #loop through the folds
    for i in range(k):
        #pick out the test fold from data
        x_test = x_split[i]
        y_test = y_split[i]
        z_test = z_split[i]

        x_train = np.concatenate(x_split[0:i] + x_split[i+1:]).ravel()
        y_train = np.concatenate(y_split[0:i] + y_split[i+1:]).ravel()
        z_train = np.concatenate(z_split[0:i] + z_split[i+1:]).ravel()



        #fit a model to the training set
        '''
        Her må vi bruke enten OLS, Ridges eller Lassos.
        '''
        X_train = pf.generate_design_2Dpolynomial(x_train, y_train, degree)

        #Economy sized SVD
        p = int((degree + 1)*(degree + 2)/2)+1
        X_train = X_train[:,0:p]
        beta,z_model = pf.least_squares(X_train,z_train,svd=True)

        '''
        Her må vi bruke modellen til å beregne z_tilde for (x_test, y_test)
        og sammenligne med z_test ved MSE eller R_2_score
        Foreløpig MSE
        '''
        X_test = pf.generate_design_2Dpolynomial(x_test, y_test, degree)

        z_fit = X_test @ beta

        expect_z = np.mean(z_fit)

        mse.append(pf.mse(z_test, z_fit)) #mse
        r2.append(pf.r2(z_test, z_fit)) #r2
        bias.append(pf.mse(z_test,expect_z))
        var.append(pf.mse(z_fit,expect_z))

    return [np.mean(mse),np.mean(r2),np.mean(bias),np.mean(var)]

'''
plotter feil mot kompleksitet
'''
#np.random.seed(108)
n = 30
error = 0.1
degrees = np.arange(1,20)

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

print("degree |  mse  | bias  |  var  | beta 95 % ")
for degree in degrees:
    """Performing a k-fold cross-validation on training data"""
    evaluation_scores = k_fold_cross_validation(x,y,z,degree)

    """Calculate bias, variance r2 and mse"""

    k_fold_mse.append(evaluation_scores[0])
    k_fold_r2.append(evaluation_scores[1])
    k_fold_bias.append(evaluation_scores[2])
    k_fold_var.append(evaluation_scores[3])


    """Simple training with no folds for comparison"""
    p = int((degree + 1)*(degree + 2)/2)+1
    X = pf.generate_design_2Dpolynomial(x, y, degree)
    X = X[:,0:p]

    beta,z_model = pf.least_squares(X,z,svd=True)
    b_ = np.mean(beta)
    std_b = np.std(beta)

    #computing the MSE when no train test split is used
    mse.append(pf.mse(z, z_model))
    print(f"{degree:6.0f} | {k_fold_mse[-1]:5.3f} | {k_fold_bias[-1]:5.3f} | \
{k_fold_var[-1]:5.3f} | <{b_ - 1.96*std_b/np.sqrt(len(beta)):.3f} , {b_ + 1.96*std_b/np.sqrt(len(beta)):.3f}>")


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
plt.title(f"Error, bias and variance for n={n}, $\sigma^2$ = {error}")
#plt.savefig("../selected results/fig1.pdf")
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
#ax.set_zlim(-0.10, 1.40)
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
