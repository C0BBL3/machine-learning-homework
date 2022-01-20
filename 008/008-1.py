import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

print('\nStarting...')

data = pd.read_csv('008/mini_kaggle_1.csv').sort_values(by=['x'])

x = np.array([[x] for x in data['x']])
y = np.array([[y] for y in data['y']])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=42)

plt.scatter(x_train, y_train, color = "black")
plt.scatter(x_test, y_test, color = "red")

print('\nPlotting Part 1: Done')


print('\nData Formatting Done')

print('\nFitting Null')

train_rss = sum([(y - 1.5) ** 2 for y in y_train])[0]
print('\nNull Train RSS:', train_rss)

test_rss = sum([(y - 1.5) ** 2 for y in y_test])[0]
print('Null Test RSS:', test_rss)

print('Null Total RSS:', train_rss+ test_rss)

plt.plot(x, [1.5 for _ in data['x']], color = "purple")

print('\nFitting Linear')

precision = 0.0001

LR = LinearRegression().fit(x_train, y_train)

#print('\nLinear Score:', LR.score(x_test, y_test))
train_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_train, LR.predict(x_train))])[0]
print('\nLinear Train RSS:', train_rss)

test_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_test, LR.predict(x_test))])[0]
print('Linear Test RSS:', test_rss)

print('Linear Total RSS:', train_rss + test_rss)

plt.plot(x, LR.predict(x), color = "green")

print('\nFitting Logistic')

max_y = max(y_train) + precision
min_y = min(y_train) - precision
x_transformed = np.array([[x[0], 1] for x in x_train])
y_transformed = np.array([[math.log((max_y - y)/(y - min_y))] for y in y_train])
beta = ((np.linalg.inv(x_transformed.T @ x_transformed)) @ x_transformed.T) @ y_transformed
a = 0.875 * beta[0][0]
b = 0.875 * beta[1][0]

max_y = max(y_test) + precision
min_y = min(y_test) - precision

LGR_prediction = [float(min_y + (max_y - min_y) / (1 + math.e ** (a * x + b))) for x in x_train]
train_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_train, LGR_prediction)])[0]
print('\nLogistic Train RSS:', train_rss)

LGR_prediction = [float(min_y + (max_y - min_y) / (1 + math.e ** (a * x + b))) for x in x_test]
test_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_test, LGR_prediction)])[0]
print('Logistic Test RSS:', test_rss)

print('Logistic Total RSS:', train_rss + test_rss)

LGR_prediction = [float(min_y + (max_y - min_y) / (1 + math.e ** (a * x + b))) for x in data['x']]

plt.plot(x, LGR_prediction, color = "blue")

print('\nFitting Polynomial with degree 3')

Poly = make_pipeline(PolynomialFeatures(3),LinearRegression()).fit(x_train, y_train)

train_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_train, Poly.predict(x_train))])[0]
print('\nPolynomial Train RSS:', train_rss)

test_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_test, Poly.predict(x_test))])[0]
print('Polynomial Test RSS:', test_rss)

print('Polynomial Total RSS:', train_rss + test_rss)

plt.plot(x, Poly.predict(x), color = "orange")

print('\nRegression Finished!')

plt.legend(['Train', 'Test', 'Null', 'Linear', 'Logistic', 'Polynomial'])
plt.savefig('images/008-1.png')

print('\nPlotting Part 2: Done')