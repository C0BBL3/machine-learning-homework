import math
import sys
import filecmp
import time
from numpy import random
import multiprocessing
from multiprocessing import Pool
import matplotlib.pyplot as plt

from metaheuristic_algorithm_nn import MetaHeuristicAlgorithm, nn_chromosome
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

def tanh( x ):
    e_x = math.e ** x
    e_neg_x = math.e ** ( - x )
    numerator = e_x - e_neg_x
    denominator = e_x + e_neg_x
    return numerator / denominator

def sech( x ):
    e_x = math.e ** x
    e_neg_x = math.e ** ( - x )
    denominator = e_x + e_neg_x
    return (2 / denominator) ** 2

NN = NeuralNetwork( 
    generate_weights(
        layer_sizes,
        random_bool = False, 
        layers_with_bias_nodes = [ False, False, False, False ],
        input_size = [ 3, 3 ]
    ), 
    functions = [ 
        lambda x: x
        for _ in range( math.prod( input_size ) )
    ] + [ 
        tanh
        for _ in range( sum( layer_sizes ) ) 
    ],

    derivatives = [
        lambda x: 1
        for _ in range( math.prod( input_size ) )
    ] + [ 
        sech
        for _ in range( sum( layer_sizes )) 
    ],
    alpha = 0.01
)

print(NN.calc_prediction( { 'input': [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ] } ) )

print(NN.calc_prediction( { 'input': [ 1, -1, 0, 0, 0, 0, 0, 0, 0 ] } ) )

print(NN.calc_prediction( { 'input': [ 0, 0, 0, -1, 0, 0, 0, 0, 1 ] } ) )

print(NN.calc_prediction( { 'input': [ 1, 0, -1, 0, 1, 0, -1, 0, -1 ] } ) )

def minimax_function( board_state, current_player ):
    minimax = Minimax()

    minimax.generate_tree(
        Game( None, None ), 
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

def minimax_function( board_state, current_player ):
    minimax = Minimax()

    minimax.generate_tree(
        Game( None, None ), 
        current_player, 
        root_board_state = board_state, 
        max_depth = 4
    )

    minimax.evaluate_game_tree(
        Game( None, None ), 
        game.evaluate
    )
    
    return minimax.get_best_move( board_state )

game = Game( minimax_function, minimax_function ) # depth 4
print(game.play())

    
