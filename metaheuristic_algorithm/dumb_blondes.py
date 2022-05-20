import math
import sys
import filecmp
import time
from pyvis.network import Network
from numpy import random
import multiprocessing
import matplotlib.pyplot as plt

from metaheuristic_algorithm import MetaHeuristicAlgorithm, nn_chromosome
from tic_tac_toe import Game, plots_3_and_4

import sys
sys.path.append('neural_network/')
from generate_weights import generate_weights
from neural_network import NeuralNetwork

sys.path.pop()
sys.path.append('min_max_algorithm/')
from minimax import Minimax

layer_sizes = [ 14, 8, 4, 1 ]
input_size = [ 3, 3 ]

weights = generate_weights(
        layer_sizes,
        random_bool = False, 
        layers_with_bias_nodes = [ True, True, True ],
        input_size = [ 3, 3 ]
    )

bias_shift = [ True, True, True ].count( True )

activation_functions = [ 
    lambda x: x
    for _ in range( 9 )
] + [ 
    lambda x: math.tanh(x) 
    for _ in range( sum( layer_sizes ) + bias_shift ) 
]

bias_node_indices = [ 
    9 + sum( layer_sizes[ 0 : i ] ) + i - 1 
    for i in range( 1, len( layer_sizes ) ) 
]

for bias_node_index in bias_node_indices:
    activation_functions[ bias_node_index ] = lambda x: x

NN = NeuralNetwork( 
    weights, 
    functions = activation_functions,
    alpha = 0.01
)

print(NN.calc_prediction( { 'input': [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ] } ) )

print(NN.calc_prediction( { 'input': [ -1, -1, -1, -1, -1, -1, -1, -1, -1 ] } ) )

print(NN.calc_prediction( { 'input': [ 1, 1, 1, 1, 1, 1, 1, 1, 1 ] } ) )

print(NN.calc_prediction( { 'input': [ +1, +1, +1, -1, -1, -1, 0, 0, 0 ] } ) )

net = Network( '1500px', '1500px' )

for node in NN.nodes:

    net.add_node( node.index, label = 'Index: {}, Value: {}'.format( node.index, node.value ) )

for edge in NN.weights.keys():

    net.add_edge( edge[ 0 ], edge[ 1 ] )
    
net.show_buttons( filter_ = True )
net.show( 'nodes.html' )

def minimax_function( board_state, current_player ):
    minimax = Minimax()

    minimax.generate_tree(
        Game( None, None, current_player = current_player ), 
        current_player, 
        root_board_state = board_state, 
        max_depth = 9
    )

    minimax.evaluate_game_tree(
        Game( None, None ), 
        game.evaluate
    )
    
    return minimax.get_best_move( board_state )

game = Game( minimax_function, minimax_function ) # depth 9
print(game.play())

    
