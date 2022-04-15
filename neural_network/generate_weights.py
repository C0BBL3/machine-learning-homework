from neural_network import NeuralNetwork
import math
import time
import random

def generate_weights(layer_sizes, random_bool = True, random_range = [-1, 1], layers_with_bias_nodes = list() ):
    weights = {}
    last_node_index = 0
    for layer_index, layer in enumerate(layer_sizes):

        layer_start_index, layer_end_index = get_iteration_indices(
            layer_sizes,
            layer_index,
            layers_with_bias_nodes
        )

        for next_node_index in range(layer_start_index, layer_end_index):
            for i in range(0, layer):
                edge = (last_node_index + i, next_node_index)
                weights[ edge ] = get_random_weight(random_bool, random_range)

        if layer_index in layers_with_bias_nodes:
            for next_node_index in range(layer_start_index, layer_end_index):
                edge = (layer_start_index - 1, next_node_index)
                weights[ edge ] = get_random_weight(random_bool, random_range)
            layer += 1

        last_node_index += layer
    return weights

def get_random_weight(random_bool, random_range):
    if not random_bool: 
        weight = 1
    else:
        temp = random.random() * ( random_range[ 1 ] - random_range[ 0 ] )
        weight = temp - random_range[1]
    return weight

def get_iteration_indices(layer_sizes, layer_index, layers_with_bias_nodes):
    bias_node_adder = 0
    if layer_index in layers_with_bias_nodes:
        temp = layers_with_bias_nodes[:layer_index + 1]
        bias_node_adder += len(temp)
    layer_start_index = sum(layer_sizes[:layer_index + 1]) + bias_node_adder
    layer_end_index = sum(layer_sizes[:layer_index + 2]) + bias_node_adder
    return layer_start_index, layer_end_index

# weights = generate_weights([2,3,3,1]) # tall house graph with all weights 1

# node_indices = len(set([_ for key in weights.keys() for _ in key]))
# activation_functions = [lambda x: x ** 2 for _ in range(node_indices)] 
# activation_function_derivatives = [lambda x: 2 * x for _ in range(node_indices)] 

# data_points = [
#     {'input': [-1, 2], 'output': lambda pred: 0.0 if pred < 0 else pred}, # negative classification
#     #{'input': [2, 1], 'output': lambda pred: 0.0 if pred >= 0 else pred}, # positive classification
# ]


# def run_neural_network(nn, iterations):
#     for i in range(1, iterations + 1):
#         for data_point in data_points:
#             nn.calc_prediction(data_point)
#             for node in nn.nodes[::-1]:
#                 nn.update_neuron_gradients(data_point, node.index)
#             for edge in weights.keys():
#                 nn.update_weight_gradients(data_point, edge)
#         if list(nn.misclassifications.values()).count(True) < 1:
#             break
#         nn.update_weights(print_output=True, iteration=i)
#     return nn

# nn1 = NeuralNetwork(weights, activation_functions, activation_function_derivatives, debug = False)
# nn2 = run_neural_network(nn1, 1)