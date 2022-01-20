import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

print('\nStarting...')

train_data = pd.read_csv('practice_dataset.csv').sort_values(by=['x'])
test_data = pd.read_csv('competition_dataset.csv').sort_values(by=['x'])

x_train = np.array([[x] for x in train_data['x']])
y_train = np.array([[y] for y in train_data['y']])
x_test = np.array([[x] for x in test_data['x']])
y_test = np.array([[y] for y in test_data['y']])

max_y_train = max(y_train) + precision
min_y_train = min(y_train) - precision
x_transformed = np.array([[x[0], 1] for x in x_train])
y_transformed = np.array([[math.log((max_y_train - y)/(y - min_y_train))] for y in y_train])
beta = ((np.linalg.inv(x_transformed.T @ x_transformed)) @ x_transformed.T) @ y_transformed
a = 0.875 * beta[0][0]
b = 0.875 * beta[1][0]

LGR_prediction_train = [float(min_y_train + (max_y_train - min_y_train) / (1 + math.e ** (a * x + b))) for x in x_train]
train_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_train, LGR_prediction_train)])[0]
print('\nLogistic Train RSS:', train_rss)

max_y_test = max(y_test) + precision
min_y_test = min(y_test) - precision

LGR_prediction_test = [float(min_y_test + (max_y_test - min_y_test) / (1 + math.e ** (a * x + b))) for x in x_test]
test_rss = sum([(y - prediction) ** 2 for y, prediction in zip(y_test, LGR_prediction_test)])[0]
print('Logistic Test RSS:', test_rss)

print('Logistic Total RSS:', train_rss + test_rss)

print('\nFinished!')