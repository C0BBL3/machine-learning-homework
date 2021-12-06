from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from generate_data import generate_graph, correct_data

one = generate_graph((0.75, 0.75), 1.70, 100) # 1 red
two = generate_graph((3.25, 0.75), 1.70, 100) # 0 blue
three = generate_graph((0.75, 3.25), 1.70, 100) # 0 blue
four = generate_graph((3.25, 3.25), 1.70, 100) # 1 red

training_one_1, testing_one_1, training_one_2, testing_one_2 = train_test_split(*one, test_size=0.8, random_state=1)
training_two_1, testing_two_1, training_two_2, testing_two_2 = train_test_split(*two, test_size=0.8, random_state=2)
training_three_1, testing_three_1, training_three_2, testing_three_2 = train_test_split(*three, test_size=0.8, random_state=3)
training_four_1, testing_four_1, training_four_2, testing_four_2 = train_test_split(*four, test_size=0.8, random_state=4)

training_uno = list(zip(training_one_1, training_one_2))
training_dos = list(zip(training_two_1, training_two_2))
training_tres = list(zip(training_three_1, training_three_2))
training_quatro = list(zip(training_four_1, training_four_2))

testing_uno = list(zip(testing_one_1, testing_one_2))
testing_dos = list(zip(testing_two_1, testing_two_2))
testing_tres = list(zip(testing_three_1, testing_three_2))
testing_quatro = list(zip(testing_four_1, testing_four_2))

training_x, training_y = correct_data([training_uno, training_dos, training_tres, training_quatro], [1,0,0,1])
testing_x, testing_y = correct_data([testing_uno, testing_dos, testing_tres, testing_quatro], [1,0,0,1])

del training_one_1
del training_two_1
del training_three_1
del training_four_1
del testing_one_1
del testing_two_1
del testing_three_1
del testing_four_1

del training_one_2
del training_two_2
del training_three_2
del training_four_2
del testing_one_2
del testing_two_2
del testing_three_2
del testing_four_2

del training_uno
del training_dos
del training_tres
del training_quatro
del testing_uno
del testing_dos
del testing_tres
del testing_quatro


#MLP = MLPClassifier(solver = 'lbfgs', activation = 'logistic', alpha = 1e-5, hidden_layer_sizes = (3,3,3), max_iter = 25000, learning_rate = 'invscaling', max_fun = 25000, random_state = 1)
#MLP.fit(training_x, training_y)

#red, blue = [[], []], [[], []]

#for ten_x in range(-9, 50):
    #for ten_y in range(-9,50):
        #if MLP.predict([[ten_x / 10, ten_y / 10]]) == 1:
            #red[0].append(ten_x / 10)
            #red[1].append(ten_y / 10)
        #else:
            #blue[0].append(ten_x / 10)
            #blue[1].append(ten_y / 10)

import matplotlib.pyplot as plt

#plt.scatter(one[0], one[1], color='red', alpha = 1.0, s = 15) # 1
#plt.scatter(two[0], two[1], color='blue', alpha = 1.0, s = 15) # 0 
#plt.scatter(three[0], three[1], color='blue', alpha = 1.0, s = 15) # 0
#plt.scatter(four[0], four[1], color='red', alpha = 1.0, s = 15) # 1
#plt.scatter(red[0], red[1], color='red', alpha = 0.25, s = 5) # 1
#plt.scatter(blue[0], blue[1], color='blue', alpha = 0.25, s = 5) # 0 
#plt.axis([-1, 5, -1, 5])
#plt.savefig('images/004-3.png')

#plt.clf()

for activation_function in ['identity', 'logistic', 'tanh', 'relu']:    
    xs = list(range(1, 11))
    ys = []
    for k in xs:
        MLP = MLPClassifier(solver = 'lbfgs', activation = 'logistic', alpha = 1e-5, hidden_layer_sizes = (3 for _ in range(k)), max_iter = 15000, learning_rate = 'invscaling', max_fun = 25000)
        MLP.fit(training_x, training_y)
        ys.append(MLP.score(testing_x, testing_y))
    plt.plot(xs, ys)

plt.legend(['identity', 'logistic', 'tanh', 'relu'])
plt.savefig('images/004-3-num_hidden_layers.png')
plt.clf()

for activation_function in ['identity', 'logistic', 'tanh', 'relu']:    
    xs = list(range(1, 101, 10))
    ys = []
    for k in xs:
        MLP = MLPClassifier(solver = 'lbfgs', activation = 'logistic', alpha = 1e-5, hidden_layer_sizes = (k,k,k), max_iter = 15000, learning_rate = 'invscaling', max_fun = 25000)
        MLP.fit(training_x, training_y)
        ys.append(MLP.score(testing_x, testing_y))
    plt.plot(xs, ys)

plt.legend(['identity', 'logistic', 'tanh', 'relu'])
plt.savefig('images/004-3-num_hidden_units_in_each_layer.png')
plt.clf()

for activation_function in ['identity', 'logistic', 'tanh', 'relu']:    
    xs = list(range(1000, 50001, 1000))
    ys = []
    for k in xs:
        MLP = MLPClassifier(solver = 'lbfgs', activation = 'logistic', alpha = 1e-5, hidden_layer_sizes = (3,3,3), max_iter = k, learning_rate = 'invscaling', max_fun = k)
        MLP.fit(training_x, training_y)
        ys.append(MLP.score(testing_x, testing_y))
    plt.plot(xs, ys)

plt.legend(['identity', 'logistic', 'tanh', 'relu'])
plt.savefig('images/004-3-num_training_iterations.png')
