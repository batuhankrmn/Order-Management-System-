# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 20:42:42 2021

@author: Karainci
"""

import numpy as np
import pandas as pd 
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error, r2_score, roc_auc_score, roc_curve, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

X = np.array([[35,35,3,1],
	[22,50,2,0],
	[63,200,1,0],
	[59,170,1,0],
	[25,40,4,1]])

from sklearn.svm import SVR

df = pd.read_excel("data.xlsx")
df = df.dropna()
df

y = df["yanıt"]
X = df.drop(['yanıt'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.3, 
                                                    random_state=42)
knn_model = KNeighborsClassifier().fit(X_train, y_train)
knn_model

#y_pred = knn_model.predict(X_test)
knn = KNeighborsClassifier()
knn_params = {"n_neighbors": np.arange(1,50)}

knn_tuned = KNeighborsClassifier(n_neighbors = 3).fit(X_train, y_train)
y_pred = knn_tuned.predict(X_test)
accuracy_score(y_test, y_pred)



yaş=37
gelir=50
kredi_karti=2

x_degerler = np.array([[yaş,gelir,kredi_karti]])

print("x_yeni: {}".format(x_degerler.shape))


prediction = knn_tuned.predict(x_degerler)

print("tahmin: {}".format(prediction))

print("tahmin sonucu: {}".format(prediction))