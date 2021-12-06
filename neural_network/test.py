from neural_network import NeuralNetwork
import math
import time

def generate_weights(layer_sizes):
    weights = {}
    last_node_index = 0
    for layer_index, layer in enumerate(layer_sizes):
        for next_node_index in range(sum(layer_sizes[:layer_index + 1]), sum(layer_sizes[:layer_index + 2])):
            for i in range(0, layer):
                weights[(last_node_index + i, next_node_index)] = 1
        last_node_index += layer
    return weights

weights = generate_weights([2,3,3,1]) # tall house graph with all weights 1

da_boi = len(set([_ for key in weights.keys() for _ in key]))
activation_functions = [lambda x: x ** 2 for _ in range(da_boi)] 
activation_function_derivatives = [lambda x: 2 * x for _ in range(da_boi)] 

data_points = [
    {'input': [-1, 2], 'output': lambda pred: 0.0 if pred < 0 else pred}, # negative classification
    #{'input': [2, 1], 'output': lambda pred: 0.0 if pred >= 0 else pred}, # positive classification
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
        nn.update_weights(print_output=True, iteration=i)
    return nn

nn1 = NeuralNetwork(weights, activation_functions, activation_function_derivatives, debug = False)
nn2 = run_neural_network(nn1, 1)