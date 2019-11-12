"""
Read output from tuning scripts and plot heatmaps of the regularization
parameters and their accuracy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()
sns.set_style("white")
sns.set_palette("Set2")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


#df_LogReg = pd.read_csv("../data/output/LogisticRegression/logistic_acc_auc_2.csv")
df_LogReg = pd.read_csv("../data/output/NeuralNetwork/neural_acc_auc.csv")
df_LogReg.rename(columns = {'learning_rate_init':'Initial learning rate', 'minibatch_size':'Mini batch size'}, inplace = True)
print("max accuracy:")
print(df_LogReg.loc[df_LogReg['accuracy'].idxmax()])
print()
print("max AUC:")
print(df_LogReg.loc[df_LogReg['AUC'].idxmax()])

heatmap_LogReg_AUC = pd.pivot_table(df_LogReg, values='AUC',
                     index=['Initial learning rate'],
                     columns='Mini batch size')



x_dim = 25
y_dim = 10

data_LogReg = df_LogReg.values
accuracy = data_LogReg[:,0].reshape(x_dim,y_dim)
learning_rate_init = data_LogReg[:,1].reshape(x_dim,y_dim)
mini_batch_size = data_LogReg[:,2].reshape(x_dim,y_dim)
auc = data_LogReg[:,3].reshape(x_dim,y_dim)
#auc[auc == 0] = np.nan


fig, ax = plt.subplots()

plot_max = x_dim-3

c = ax.pcolormesh(mini_batch_size[0:plot_max,:], learning_rate_init[0:plot_max,:],accuracy[0:plot_max,:]
                ,cmap = 'gnuplot'#'viridis'#'plasma'
                #,vmin = 0.2
                #,vmax = 0.9
                )
#ax.set_title('Accuracy of LogisticRegression')
ax.set_xlabel("minibatch size",fontsize=20)
ax.set_ylabel("initial learning rate",fontsize=20)
ax.tick_params(axis='both', labelsize=14)
ax.set_yscale("log")
ax.set_xscale("log")
fig.colorbar(c, ax=ax)
#plt.savefig("../figures/LogRegTune_accuracy.pdf")


fig, ax = plt.subplots()

c = ax.pcolormesh(mini_batch_size[0:plot_max,:], learning_rate_init[0:plot_max,:],auc[0:plot_max,:]
                  ,cmap = 'gnuplot'#'viridis'#'plasma'
                  #,vmin = 0.3
                  #,vmax = 0.8
                  )
#ax.set_title('AUC of LogisticRegression')
ax.set_xlabel("minibatch size",fontsize=20)
ax.set_ylabel("initial learning rate",fontsize=20)
ax.tick_params(axis='both', labelsize=14)
ax.set_yscale("log")
ax.set_xscale("log")
fig.colorbar(c, ax=ax)
#plt.savefig("../figures/LogRegTune_auc.pdf")



df_NN = pd.read_csv("../data/output/NeuralNetwork/neural_acc_auc_2.csv")
df_NN.rename(columns = {'learning_rate_init':'Initial learning rate', 'minibatch_size':'Mini batch size'}, inplace = True)
print("max accuracy:")
print(df_NN.loc[df_NN['accuracy'].idxmax()])
print()
print("max AUC:")
print(df_NN.loc[df_NN['AUC'].idxmax()])

x_dim = 20
y_dim = 5

data_NN = df_NN.values
accuracy = data_NN[:,0].reshape(x_dim,y_dim)
learning_rate = data_NN[:,1].reshape(x_dim,y_dim)
mini_batch_size = data_NN[:,2].reshape(x_dim,y_dim)
auc = data_NN[:,3].reshape(x_dim,y_dim)


fig, ax = plt.subplots()


cut_off = 1
c = ax.pcolormesh(mini_batch_size[0:-cut_off-1,:], learning_rate[0:-cut_off-1,:],accuracy[0:-cut_off-1,:]
                ,cmap = 'plasma'#'viridis'#'plasma'
                #,vmin = 0.2
                #,vmax = 0.9
                )
#ax.set_title('Accuracy of LogisticRegression')
ax.set_xlabel("minibatch size",fontsize=20)
ax.set_ylabel("learning rate",fontsize=20)
ax.tick_params(axis='both', labelsize=14)
ax.set_yscale("log")
ax.set_xscale("log")
fig.colorbar(c, ax=ax)
plt.savefig("../figures/NNTune_accuracy.pdf")


fig, ax = plt.subplots()

c = ax.pcolormesh(mini_batch_size[0:-cut_off-1,:], learning_rate[0:-cut_off-1,:],accuracy[0:-cut_off-1,:]
                  ,cmap = 'plasma'#'viridis'#'plasma'
                  #,vmin = 0.3
                  #,vmax = 0.8
                  )
#ax.set_title('AUC of LogisticRegression')
ax.set_xlabel("minibatch size",fontsize=20)
ax.set_ylabel("learning rate",fontsize=20)
ax.tick_params(axis='both', labelsize=14)
ax.set_yscale("log")
ax.set_xscale("log")
fig.colorbar(c, ax=ax)
plt.savefig("../figures/NNTune_auc.pdf")

plt.show()
