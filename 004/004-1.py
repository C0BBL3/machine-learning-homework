from sklearn.neighbors  import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import pandas as pd
from generate_data import generate_graph

def correct_data(data, labels): # data = [[(1,1),(1,1.3),...], [(3,1),(3,1.3),...],...] labels = [1,0...]
    data_2 = []
    for group in data:
        for element in group:
            data_2.append(element)
    corrected_data = np.array(data_2)
    labels_2 = []
    for i, label in enumerate(labels):
        for _ in range(len(data[i])):
            labels_2.append(label)
    corrected_labels = np.array(labels_2)
    return corrected_data, corrected_labels

def KNN_f(x,y,k): # k is num neighbors
    training_x, testing_x, training_y, testing_y = train_test_split(x, y, test_size=0.5, random_state=1)
    KNN = KNeighborsClassifier(n_neighbors = k)
    KNN.fit(training_x, training_y)
    return KNN.score(testing_x, testing_y)

def DTC_f(x,y,k): # k is min size split
    training_x, testing_x, training_y, testing_y = train_test_split(x, y, test_size=0.5, random_state=1)
    DTC = DecisionTreeClassifier(min_samples_split = k)
    DTC.fit(training_x, training_y)
    return DTC.score(testing_x, testing_y)

def RFC_f(x,y,k): # k is num trees
    training_x, testing_x, training_y, testing_y = train_test_split(x, y, test_size=0.5, random_state=1)
    RFC = RandomForestClassifier(n_estimators = k)
    RFC.fit(training_x, training_y)
    return RFC.score(testing_x, testing_y)

oneone = generate_graph((1,1), 1.25, 50)
uno = [[oneone[0][i], oneone[1][i]] for i in range(len(oneone[0]))]
onethree = generate_graph((1,3), 1.25, 50)
dos = [[onethree[0][i], onethree[1][i]] for i in range(len(onethree[0]))]
threeone = generate_graph((3,1), 1.25, 50)
tres = [[threeone[0][i], threeone[1][i]] for i in range(len(threeone[0]))]
threethree = generate_graph((3,3), 1.25, 50)
quatro = [[threethree[0][i], threethree[1][i]] for i in range(len(threethree[0]))]

x, y = correct_data([uno, dos, tres, quatro], [1,0,1,0])

import matplotlib.pyplot as plt

plt.plot(list(range(1,100)), [KNN_f(x,y,k) for k in range(1,100)])
plt.plot(list(range(2,100)), [DTC_f(x,y,k) for k in range(2,100)])
plt.plot(list(range(1,100)), [RFC_f(x,y,k) for k in range(1,100)])
plt.legend(['KNN', 'DTC', 'RFC'])
plt.axis([1, 100, 0, 1])
plt.savefig('004-1')