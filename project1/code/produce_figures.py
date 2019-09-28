import numpy as np
import matplotlib.pyplot as plt
import projectfunctions as pf
import plottingfunctions as plf
import seaborn as sns

#for reprodusability
np.random.seed(2019)

figdir = "../figures/"
sns.set()
sns.set_style("whitegrid")
sns.set_palette("Set2")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#compare test and training for OLS
reg = pf.ridge_regression
n = 20
noise = 0.1
max_degree = 12
hyperparam = 0

#set up intervalls for x and y
x = np.linspace(0,1,n)
y = np.linspace(0,1,n)

#making an x and y grid
x_grid, y_grid = np.meshgrid(x, y)

#flatten x and y
x = x_grid.flatten()
y = y_grid.flatten()

#compute z and flatten it
z_grid = pf.frankefunction(x_grid, y_grid) + np.random.normal(0,noise,x_grid.shape)
z = z_grid.flatten()


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

plf.plot_test_vs_degree_boot(ax, x, y, z, reg, max_degree, hyperparam, linewidth=2)
plf.plot_train_vs_degree(ax, x, y, z, reg, max_degree, hyperparam,linewidth=2)

ax.legend(fontsize=18,loc='upper center', bbox_to_anchor=(0.5, 1.15),frameon=False, ncol=2)
ax.tick_params(axis='both', labelsize=14)
ax.set_xlabel('degree', fontsize=18)
ax.set_ylabel('value', fontsize=18)

plt.savefig(figdir+'mseVSdegreeOLS.pdf')


fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

plf.plot_test_vs_degree_kfold(ax2, x, y, z, reg, max_degree, hyperparam, plot_r2= True, linewidth=2)
plf.plot_train_vs_degree(ax2, x, y, z, reg, max_degree, hyperparam, plot_r2=True, linewidth=2)

ax2.legend(fontsize=18,loc='upper center', bbox_to_anchor=(0.5, 1.15),frameon=False, ncol=2)
ax2.tick_params(axis='both', labelsize=14)
ax2.set_xlabel('degree', fontsize=18)
ax2.set_ylabel('value', fontsize=18)

plt.savefig(figdir+'r2VSdegreeOLS.pdf')


fig3 = plt.figure()
ax3 = fig3.add_subplot(1,1,1)

plf.plot_test_vs_degree_boot(ax3, x, y, z, reg, max_degree, hyperparam, show_bias_var=True ,linewidth=2)

ax3.legend(fontsize=18,loc='upper center', bbox_to_anchor=(0.5, 1.15),frameon=False, ncol=3)
ax3.tick_params(axis='both', labelsize=14)
ax3.set_xlabel('degree', fontsize=18)
ax3.set_ylabel('value', fontsize=18)

plt.savefig(figdir+'biasvarianceOLS.pdf')



hyperparams = list(np.logspace(-5, -1, 5))
hyperparams.insert(0, 0)

fig4 = plt.figure()
ax4 = fig4.add_subplot(1,1,1)

plf.plot_test_vs_degree_multiple_lambda(ax4, x, y, z, reg, max_degree, hyperparams)
ax4.legend(frameon=False, fontsize=14)
ax4.set_xlabel("Degrees", fontsize=18)
ax4.set_ylabel("MSE", fontsize=18)
plt.savefig(figdir+"lambdavsdegreesRIDGE.pdf")



fig5 = plt.figure()
ax5 = fig5.add_subplot(1,1,1)

degree = 5
reg = pf.least_squares

plf.plot_bias_confidence(ax5, x, y, z, reg, degree, hyperparam, linewidth = 2)
ax5.set_xlabel(r'$i$', fontsize=18)
ax5.set_ylabel(r'$\beta_i$', fontsize=18)
plt.savefig(figdir + "betaconfidence.pdf")

reg = pf.lasso_regression
hyperparams = list(np.logspace(-6, -1, 6))

fig6 = plt.figure()
ax6 = fig6.add_subplot(1,1,1)

plf.plot_test_vs_degree_multiple_lambda(ax6, x, y, z, reg, max_degree, hyperparams)
ax6.legend(frameon=False, fontsize=14)
ax6.set_xlabel("Degrees", fontsize=14)
ax6.set_ylabel("MSE", fontsize=14)
plt.savefig(figdir+"lambdavsdegreesLASSO.pdf")

plt.show()
