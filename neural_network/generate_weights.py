from neural_network import NeuralNetwork
import math
import time
import random

def generate_weights(layer_sizes, random_bool = True, random_range = [-1, 1], layers_with_bias_nodes = list(), input_size = [ 0, 0 ] ):

    if input_size[ 0 ] != input_size[ 1 ]:
        print( '\nInput Sizes differ, please make board a square. Input Sizes:', input_size)
        exit()

    shift = math.prod( input_size )

    weights = {}
    
    if shift > 0:

        weights = get_input_weights(
            layer_sizes, 
            input_size, 
            shift, 
            random_bool, 
            random_range
        )
        
    for layer_index, layer_size in enumerate( layer_sizes[ : -1 ] ):

        if layer_index == 0:

            current_layer_iteration_indices = list( 
                range( 
                    0 + shift , 
                    layer_sizes[ 0 ] + shift 
                ) 
            ) 
        
        else:

            current_layer_iteration_indices = list( next_layer_iteration_indices )

        next_layer_iteration_indices = get_iteration_indices(
            layer_sizes,
            layer_index,
            layers_with_bias_nodes,
            layers_with_bias_nodes[ layer_index ],
            shift = shift
        )

        for next_node_index in next_layer_iteration_indices:

            for current_node_index in current_layer_iteration_indices:

                edge = ( 
                    current_node_index, 
                    next_node_index 
                )

                weights[ edge ] = get_random_weight( 
                    random_bool, 
                    random_range 
                )

        if layers_with_bias_nodes[ layer_index ]:

            bias_node_index = current_layer_iteration_indices[ -1 ] + 1
            
            for next_node_index in next_layer_iteration_indices:

                edge = ( 
                    bias_node_index, 
                    next_node_index 
                )
                
                weights[ edge ] = get_random_weight( 
                    random_bool, 
                    random_range 
                )

    return weights



def get_iteration_indices( layer_sizes, layer_index, layers_with_bias_nodes, bias_layer, shift = 0 ):

    bias_node_adder = 0

    if bias_layer:

        temp = layers_with_bias_nodes[ : layer_index + 1 ]
        bias_node_adder += len(temp)

    layer_start_index = sum(
        layer_sizes[ : layer_index + 1 ] 
    ) + bias_node_adder + shift

    layer_end_index = sum(
        layer_sizes[ : layer_index + 2]
    ) + bias_node_adder + shift
    
    return [ 
        i 
        for i in range( 
            layer_start_index, 
            layer_end_index 
        ) 
    ]

def get_input_weights( layer_sizes, input_size, shift, random_bool, random_range, ):

    weights = {}

    layer_sizes[ 0 ] = sum( 
        [ 
            ( input_size[0] - i ) ^ 2 
            for i in range( input_size[ 0 ] )
        ]
    )

    all_possible_quadrants = get_all_possible_quadrant_indices( input_size )

    for input_node_index in range( shift ):

        edges = [ 
            ( # one to one
                input_node_index, 
                input_node_index + shift
            ), 
            ( # one to all
                input_node_index,
                shift + layer_sizes[ 0 ]
            ) 
        ]
        
        quadrant_indices = get_quadrant_indices( 
            input_size, 
            input_node_index 
        )

        for quadrant_index in quadrant_indices: # one to multiple

            edge.append( 
                (
                    input_node_index, 
                    quadrant_index
                )
            )

        for edge in edges: 

            weights[ edge ] = get_random_weight( 
                random_bool, 
                random_range 
            )
            
    return weights

def get_all_possible_quadrant_indices( shift, input_size ):

    all_possible_quadrants = list()

    for size_of_gap in range( 1, input_size[ 0 ] ): # size of gap ( between end of current row and beginning of next row indices )

        size_of_quadrant = input_size[ 0 ] - size_of_gap
        indices = []

        for y_index in range( size_of_quadrant ): # y index
        
            for x_index in range( size_of_quadrant ): # x index

                indices.append( shift + x_index + input_size[ 1 ] * y_index )
            
        for y_shift in range( size_of_gap ): # y shift

            for x_shift in range( size_of_gap ): # x shift
            
                quadrant = list( 
                    map(
                        lambda i: i + x_shift + input_size[ 1 ] * y_shift, 
                        list( indices ) 
                    ) 
                )
                
                all_possible_quadrants.append( quadrant )

    return all_possible_quadrants

def get_quadrant_indices( input_size, input_node_index, all_possible_quadrants ):

    quadrant_indices = list()
    shift = math.prod( input_size )

    for i, quadrant in enumerate( all_possible_quadrants ):

        if input_node_index in quadrant:

            quadrant_indices.append( 2 * shift + i )
    
    return quadrant_indices
    
    
def get_random_weight( random_bool, random_range ):
    if not random_bool: 
        weight = 1
    else:
        temp = random.random() * ( random_range[ 1 ] - random_range[ 0 ] )
        weight = temp - random_range[1]
    return weight