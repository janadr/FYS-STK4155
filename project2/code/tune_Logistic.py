"""
Use the tune_hyperparameter function from projectfunctions to run the logistic
regression for different values of learning rate and minibatch size.
"""

import pandas as pd
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn import linear_model
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, r2_score


import sys
sys.path.append("class/")
from Regression import LogisticRegression
import projectfunctions as pf


def learning_schedule(decreaser, learning_rate_init=0.1):
    return learning_rate_init/(decreaser + 1)

np.random.seed(42)


sns.set()
sns.set_style("whitegrid")
sns.set_palette("husl")


filepath = "../data/input/"
filename = "default_of_credit_card_clients_partial_clean.pkl"

df = pd.read_pickle(filepath + filename)

# preparing designmatrix by scaling and using one hot encoding for cat data
designMatrix = df.loc[:, df.columns != 'default payment next month']
column_indices = pf.pca(designMatrix, 1e-1)
print(designMatrix.columns[column_indices])
designMatrix = designMatrix.iloc[:, column_indices]

designMatrix_num = designMatrix.drop(["SEX", "EDUCATION", "MARRIAGE"], axis=1)
designMatrix_cat = designMatrix.iloc[:, 1:4]

num_attributes = list(designMatrix)
cat_attributes = list(designMatrix_cat)
design_pipeline = ColumnTransformer([
                                    ("scaler", StandardScaler(), num_attributes),
                                    ("onehot", OneHotEncoder(categories="auto"), cat_attributes)
                                    ],
                                    remainder="passthrough"
                                    )
designMatrix_prepared = design_pipeline.fit_transform(designMatrix)

# exporting labels to a numpy array
labels = df.loc[:, df.columns == 'default payment next month'].to_numpy().ravel()

seed = 42
logreg = LogisticRegression()

rate_range = np.logspace(0.01, 1, 50, dtype=float)
batch_range = np.linspace(50, 2000, 50, dtype=int)

#run tune hyperparameter funcition
df_tuned = pf.tune_hyperparameter(designMatrix_prepared, labels, logreg, seed,
                                rate_range,
                                batch_range,
                                learning_schedule,
                                n_epochs=20,
                                )

#store results
datadir = "../data/output/LogisticRegression/"
pf.create_directories(datadir)
filename = "logistic_test.csv"
df_tuned.to_csv(datadir + filename)
print(df_tuned.head())
