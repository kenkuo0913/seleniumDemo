#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:36:43 2020

@author: kenkuo
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

X,y=make_regression(n_samples=100, n_features=1, noise=20)
# plt.scatter(X,y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Simple Linear Regression
regr=linear_model.LinearRegression()
regr.fit(X_train, y_train)
#plt.scatter(X_train, y_train, color='black')
plt.scatter(X_test, y_test, color='red')
#plt.scatter(X_test, regr.predict(X_test), color='blue')
plt.plot(X_test, regr.predict(X_test),color='blue',linewidth=1)
plt.show()

w_0=regr.intercept_
w_1=regr.coef_
print("Intercept: ",w_0)
print("Cofficient: ",w_1)
regr.score(X_train,y_train)
regr.score(X_test,y_test)

# Gradient Decent
#Parameters
alpha=0.001 #learning rate
repeats=1000

#Initializing variables
w0=0
w1=0
errors=[]
points=[]

for j in range(repeats):
    error_sum=0
    squared_error_sum=0
    error_sum_x=0
    for i in range(len(X_train)):
        predict=w0+(X_train[i]*w1)
        squared_error_sum=squared_error_sum+(y_train[i]-predict)**2
        error_sum=error_sum+y_train[i]-predict
        error_sum_x=error_sum_x+(y_train[i]-predict)*X_train[i]
    w0=w0+(alpha*error_sum)
    w1=w1+(alpha*error_sum_x)
    errors.append(squared_error_sum/len(X_train))

print('w0: %2f' %w0)
print('w1: %2f' %w1)

predicts=[]
mean_error=0
for i in range(len(X_test)):
    predict=w0+(X_test[i]*w1)
    predicts.append(predict)

plt.scatter(X_test,predicts)
plt.scatter(X_test, y_test, color='red')
plt.show()

# Polynomial Regression
size=[5,10,12,14,18,30,33,55,65,80,100,150]
price=[300,400,450,800,1200,1400,2000,2500,2800,3000,3500,9000]
plt.scatter(size,price)
plt.show()
series_dict={'X':size,'y':price}
df=pd.DataFrame(series_dict)
X=df[['X']]
y=df[['y']]
model=make_pipeline(PolynomialFeatures(3),linear_model.LinearRegression())
model.fit(X,y)

plt.scatter(X,y)
plt.plot(X,model.predict(X),color='red')

scores=[]
colors=['green','purple','gold','blue','black']
plt.scatter(X,y,c='red')
for count,degree in enumerate([1,2,3,4,5]):
    model=make_pipeline(PolynomialFeatures(degree),linear_model.LinearRegression())
    model.fit(X,y)
    scores.append(model.score(X,y))
    plt.plot(X,model.predict(X),color=colors[count],label='degree %d' %degree)

plt.legend(loc=2)
plt.show()
print(scores)

# Multivariable Regression
X,y=make_regression(n_samples=100, n_features=5, noise=20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
regr=linear_model.LinearRegression()
regr.fit(X_train, y_train)
regr.intercept_
regr.coef_
regr.score(X_train,y_train)
regr.score(X_test,y_test)
size=[5,10,12,14,18,30,33,55,65,80,100,150]
distance=[50,20,70,100,200,150,30,50,70,35,40,20]
price=[300,400,450,800,1200,1400,2000,2500,2800,3000,3500,9000]
series_dict={'X1':size,'X2':distance,'y':price}
df=pd.DataFrame(series_dict)
X=df[['X1','X2']]
y=df[['y']]
regr=linear_model.LinearRegression()
regr.fit(X, y)
regr.score(X,y)
regr.intercept_
regr.coef_

# To Avoid Overfitting¶
# 1. Lasso Regression
# 2. Ridge Regression
X,y=make_regression(n_samples=1000, n_features=10, noise=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=5)
regr=linear_model.LinearRegression()
regr.fit(X_train, y_train)
print('Training Score: ',regr.score(X_train,y_train))
print('Testing Score: ',regr.score(X_test,y_test))
clf_lasso=linear_model.Lasso(alpha=0.5)
clf_lasso.fit(X_train,y_train)
print('Training Score: ',clf_lasso.score(X_train,y_train))
print('Testing Score: ',clf_lasso.score(X_test,y_test))
clf_ridge=linear_model.Ridge(alpha=10)
clf_ridge.fit(X_train,y_train)
print('Training Score: ',clf_ridge.score(X_train,y_train))
print('Testing Score: ',clf_ridge.score(X_test,y_test))
model=make_pipeline(PolynomialFeatures(4),linear_model.Ridge())
model.fit(X,y)
model.score(X,y)