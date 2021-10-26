from neural_network import NeuralNetwork
import math
import time

data_points = [
    {'input': [1, 2], 'output': lambda pred: pred},
]

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for data_point in data_points:
            nn.calc_prediction(data_point)
            for node in nn.nodes[::-1]:
                nn.update_neuron_gradients(data_point, node.index)
            for edge in nn.weights.keys():
                nn.update_weight_gradients(data_point, edge)
        #if list(nn.misclassifications.values()).count(True) < 1:
         #   break
        nn.update_weights(print_output=False, iteration=i)
    nn.print_outputs(i)    

def run_da_ting(l):
    uno = time.time()
    weights = {}
    last_node_index = 0
    next_node_index = 2
    for layer in range(0, l):
        for i in range(0, 2):
            weights[(last_node_index + i, next_node_index)] = 1
        if layer == l - 1:
            break
        next_node_index += 1
        for i in range(0, 2):
            weights[(last_node_index + i, next_node_index)] = 1
        last_node_index += 2
        next_node_index += 1
    da_boi = len(set([_ for key in weights.keys() for _ in key]))
    activation_functions = [lambda x: math.atan(x) for _ in range(da_boi)]
    activation_function_derivatives = [lambda x: 1 / (1 + x ** 2.0) for _ in range(da_boi)]
    nn1 = NeuralNetwork(weights, activation_functions, activation_function_derivatives, debug = False)
    nn2 = run_neural_network(nn1, 10000)
    dos = time.time()
    print("\n\n", dos - uno, "\n\n")
    return dos - uno

import matplotlib.pyplot as plt

plt.plot(list(range(0,15)), [run_da_ting(i) for i in range(0,15)])
plt.show()
plt.savefig('neural_net.png')