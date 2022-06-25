from neural_network import NeuralNetwork
from generate_weights import generate_weights
from tic_tac_toe import Game
from minimax import Minimax
import time
import sys
import math
sys.path.append('metaheuristic_algorithm/')

sys.path.pop()
sys.path.append('neural_network/')

layer_sizes = [14, 8, 4, 1]
input_size = [3, 3]

bias_shift = [True, True, True].count(True)

activation_functions = [
    lambda x: x
    for _ in range(9)
] + [
    lambda x: math.tanh(x)
    for _ in range(sum(layer_sizes) + bias_shift)
]

bias_node_indices = [
    9 + sum(layer_sizes[0: i]) + i - 1
    for i in range(1, len(layer_sizes))
]

for bias_node_index in bias_node_indices:
    activation_functions[bias_node_index] = lambda x: x

game = Game(None, None)
temp = [0 for i in range(21)]

weights = generate_weights(
    layer_sizes,
    random_bool=False,
    #random_range = [ -0.2, 0.2 ],
    layers_with_bias_nodes=[True, True, True],
    input_size=[3, 3]
)

NN = NeuralNetwork(
    weights,
    functions=activation_functions,
    alpha=0.01
)


def evaluation_function(board_state, current_player): return NN.calc_prediction(
    {
        'input': [
            {0: 0, 1: -1, 2: 1}[space]  # double checking if
            if current_player == 2 else   # board state  is in
            {0: 0, 1: 1, 2: -1}[space]  # current player format
            for space in board_state
        ]
    }
)


minimax = Minimax()
minimax.generate_tree(game, game.current_player)
minimax.evaluate_game_tree(game, evaluation_function)
for node in minimax.nodes.values():
    node.value = round(node.value, 1)
for node in minimax.nodes.values():
    for j, num in enumerate(range(-10, 11)):
        if node.value == (num / 10):
            temp[j] += 1

print(temp)

game = Game(None, None)
temp = [0 for i in range(21)]
for i in range(20):

    weights = generate_weights(
        layer_sizes,
        random_bool=True,
        random_range=[-0.2, 0.2],
        layers_with_bias_nodes=[True, True, True],
        input_size=[3, 3]
    )

    NN = NeuralNetwork(
        weights,
        functions=activation_functions,
        alpha=0.01
    )

    def evaluation_function(board_state, current_player): return NN.calc_prediction(
        {
            'input': [
                {0: 0, 1: -1, 2: 1}[space]  # double checking if
                if current_player == 2 else   # board state  is in
                {0: 0, 1: 1, 2: -1}[space]  # current player format
                for space in board_state
            ]
        }
    )

    minimax = Minimax()
    minimax.generate_tree(game, game.current_player)
    minimax.evaluate_game_tree(game, evaluation_function)
    for node in minimax.nodes.values():
        node.value = round(node.value, 1)
    for node in minimax.nodes.values():
        for j, num in enumerate(range(-10, 11)):
            if node.value == (num / 10):
                temp[j] += 1 / 20


print(temp)
