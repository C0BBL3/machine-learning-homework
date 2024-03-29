from neural_network_old import NeuralNetwork
import math
import time

weights = {
    (0, 2): 1,
    (1, 2): 1,
    (0, 3): 1,
    (1, 3): 1,
    (2, 4): 1,
    (3, 4): 1,
}

activation_functions = [
    lambda x: x ** 2,
    lambda x: x ** 2,
    lambda x: x ** 2,
    lambda x: x ** 2,
    lambda x: x ** 2,
]

activation_function_derivatives = [
    lambda x: 2 * x,
    lambda x: 2 * x,
    lambda x: 2 * x,
    lambda x: 2 * x,
    lambda x: 2 * x,
]

data_points = [
    {'input': [1, 2], 'output': lambda pred: 0.0 if pred < 0 else pred},
]


def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for data_point in data_points:
            nn.calc_prediction(data_point)
            for node in nn.nodes[::-1]:
                nn.update_neuron_gradients(data_point, node.index)
            for edge in weights.keys():
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.update_weights(print_output=False, iteration=i)

def run_neural_network_old(nn, iterations):
    for i in range(1, iterations + 1):
        for data_point in data_points:
            nn.calc_prediction(data_point)
            for edge in weights.keys():
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.update_weights(print_output=False, iteration=i)

first = time.time()

nn1 = NeuralNetwork(weights, activation_functions, activation_function_derivatives, debug = False)
nn2 = run_neural_network(nn1, 1)

second = time.time()
print("total time new", second - first)

from neural_network_old import NeuralNetwork

third = time.time()

nn3 = NeuralNetwork(weights, activation_functions, activation_function_derivatives, bias = False, debug = False)
nn4 = run_neural_network_old(nn3, 1)

fourth = time.time()
print("total time old", fourth - third)