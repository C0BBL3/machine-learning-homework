from neural_network import NeuralNetwork
import math
import time
import random

def generate_weights(layer_sizes, random_bool = True, random_range = [-1, 1], layers_with_bias_nodes = list() ):

    weights = {}

    for layer_index, layer_size in enumerate( layer_sizes[ : -1 ] ):

        if layer_index == 0:

            current_layer_iteration_indices = list( range( 0, layer_sizes[ 0 ] ) ) 
        
        else:

            current_layer_iteration_indices = list( next_layer_iteration_indices )

        next_layer_iteration_indices = get_iteration_indices(
            layer_sizes,
            layer_index,
            layers_with_bias_nodes,
            layers_with_bias_nodes[ layer_index ]
        )

        for next_node_index in next_layer_iteration_indices:

            for current_node_index in current_layer_iteration_indices:

                edge = ( current_node_index, next_node_index )
                weights[ edge ] = get_random_weight( random_bool, random_range )

        if layers_with_bias_nodes[ layer_index ]:

            bias_node_index = current_layer_iteration_indices[ -1 ] + 1
            
            for next_node_index in next_layer_iteration_indices:

                edge = ( 
                    bias_node_index, 
                    next_node_index 
                )
                
                weights[ edge ] = get_random_weight( random_bool, random_range )

    return weights

def get_random_weight( random_bool, random_range ):
    if not random_bool: 
        weight = 1
    else:
        temp = random.random() * ( random_range[ 1 ] - random_range[ 0 ] )
        weight = temp - random_range[1]
    return weight

def get_iteration_indices(layer_sizes, layer_index, layers_with_bias_nodes, bias_layer):

    bias_node_adder = 0

    if bias_layer:

        temp = layers_with_bias_nodes[ : layer_index + 1 ]
        bias_node_adder += len(temp)

    layer_start_index = sum(
        layer_sizes[ : layer_index + 1 ] 
    ) + bias_node_adder

    layer_end_index = sum(
        layer_sizes[ : layer_index + 2]
    ) + bias_node_adder
    
    return [ 
        i 
        for i in range( 
            layer_start_index, 
            layer_end_index 
        ) 
    ]

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