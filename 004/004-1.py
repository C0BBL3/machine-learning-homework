from sklearn.neighbors  import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from generate_data import generate_graph, correct_data
import random

def KNN_f(training_x, testing_x, training_y, testing_y, k): # k is num neighbors
    KNN = KNeighborsClassifier(n_neighbors = k)
    KNN.fit(training_x, training_y)
    return KNN.score(testing_x, testing_y)

def DTC_f(training_x, testing_x, training_y, testing_y, k): # k is min size split
    DTC = DecisionTreeClassifier(min_samples_split = k, random_state=2)
    DTC.fit(training_x, training_y)
    return DTC.score(testing_x, testing_y)

def RFC_f(training_x, testing_x, training_y, testing_y, k): # k is num trees
    RFC = RandomForestClassifier(n_estimators = k, random_state=2)
    RFC.fit(training_x, training_y)
    return RFC.score(testing_x, testing_y)

import matplotlib.pyplot as plt

random.seed(0)
one = generate_graph((0.75, 0.75), 1.70, 100) # 1 red
two = generate_graph((3.25, 0.75), 1.70, 100) # 0 blue
three = generate_graph((0.75, 3.25), 1.70, 100) # 0 blue
four = generate_graph((3.25, 3.25), 1.70, 100) # 1 red

plt.scatter(one[0], one[1], color='red')
plt.scatter(two[0], two[1], color='blue')
plt.scatter(three[0], three[1], color='blue')
plt.scatter(four[0], four[1], color='red')
plt.axis([-1, 5, -1, 5])
plt.savefig('images/004-1-data.png')

plt.clf()

training_one_1, testing_one_1, training_one_2, testing_one_2 = train_test_split(*one, test_size=0.8, random_state=1)
training_two_1, testing_two_1, training_two_2, testing_two_2 = train_test_split(*two, test_size=0.8, random_state=2)
training_three_1, testing_three_1, training_three_2, testing_three_2 = train_test_split(*three, test_size=0.8, random_state=3)
training_four_1, testing_four_1, training_four_2, testing_four_2 = train_test_split(*four, test_size=0.8, random_state=4)

training_uno = list(zip(training_one_1, training_one_2))
training_dos = list(zip(training_two_1, training_two_2))
training_tres = list(zip(training_three_1, training_three_2))
training_quatro = list(zip(training_four_1, training_four_2))

plt.scatter(training_one_1, training_one_2, color='red')
plt.scatter(training_two_1, training_two_2, color='blue')
plt.scatter(training_three_1, training_three_2, color='blue')
plt.scatter(training_four_1, training_four_2, color='red')
plt.axis([-1, 5, -1, 5])
plt.savefig('images/004-1-training.png')

plt.clf()

testing_uno = list(zip(testing_one_1, testing_one_2))
testing_dos = list(zip(testing_two_1, testing_two_2))
testing_tres = list(zip(testing_three_1, testing_three_2))
testing_quatro = list(zip(testing_four_1, testing_four_2))

plt.scatter(testing_one_1, testing_one_2, color='red')
plt.scatter(testing_two_1, testing_two_2, color='blue')
plt.scatter(testing_three_1, testing_three_2, color='blue')
plt.scatter(testing_four_1, testing_four_2, color='red')
plt.axis([-1, 5, -1, 5])
plt.savefig('images/004-1-testing.png')

plt.clf()

training_x, training_y = correct_data([training_uno, training_dos, training_tres, training_quatro], [1,0,0,1])
testing_x, testing_y = correct_data([testing_uno, testing_dos, testing_tres, testing_quatro], [1,0,0,1])

plt.plot(list(range(1,50)), [KNN_f(training_x, testing_x, training_y, testing_y, k) for k in range(1,50)])
plt.plot(list(range(2,50)), [DTC_f(training_x, testing_x, training_y, testing_y, k) for k in range(2,50)])
plt.plot(list(range(1,50)), [RFC_f(training_x, testing_x, training_y, testing_y, k) for k in range(1,50)])
plt.legend(['KNN', 'DTC', 'RFC'])
plt.savefig('images/004-1-three-plots')