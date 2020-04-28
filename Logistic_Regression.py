#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:54:25 2020

@author: kenkuo
"""


# 平均一天喝幾杯含糖飲料以上未來易得糖尿病?
# 範例
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

data=pd.read_csv('/Users/kenkuo/Downloads/ml_toturial-master/LogR_data.csv')

X=data['Amount'].values
y=data['Result'].values

X=X.reshape(-1,1)
model=linear_model.LogisticRegression()
model.fit(X,y)
print('coef', model.coef_)
print('intercept',model.intercept_)

w1=float(model.coef_)
w0=float(model.intercept_)

def sigmoid(x,wo,w1):
    ln_odds=wo+w1*x
    return 1/(1+np.exp(-ln_odds))

x=np.arange(0,10,1)
s_x=sigmoid(x,w0,w1)
plt.plot(x,s_x)
plt.axhline(y=0.5, ls='dotted', color='k')
model.predict([[0],[1],[2],[3]])
model.predict_proba(X)
model.score(X,y)

#多元分類
from sklearn import datasets
from sklearn.model_selection import train_test_split

iris=datasets.load_iris()
X=iris.data
y=iris.target
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
model=linear_model.LogisticRegression()
model.fit(X_train,y_train)
model.predict(X_test)
model.predict_proba(X_test)
model.score(X_train,y_train)
model.score(X_test,y_test)