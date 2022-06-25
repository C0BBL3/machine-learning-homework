from neural_network import NeuralNetwork
from generate_weights import generate_weights
import math
import sys
import filecmp
import time
from numpy import random
import multiprocessing
import matplotlib.pyplot as plt
from plot_metaheuristic_algorithm import plot_win_loss_tie, plot_state_value, plot_strategy_effectiveness
from metaheuristic_algorithm import MetaHeuristicAlgorithm
from tic_tac_toe import Game, plots_3_and_4

import sys
sys.path.append('neural_network/')

if __name__ == '__main__':

    print('\nStarting...\n\nInitializing Meta-Heuristic Algorithm...')

    scores = [
        list(),  # random average
        list(),  # original average
        list(),  # previous average
        list(),  # win prediction
        list(),  # loss prediction
        list(),  # tie prediction
    ]

    num_generations = 250

    MHA = MetaHeuristicAlgorithm()
    MHA.read_chromosomes(
        generate_weights,
        [14, 8, 4, 1],
        population_size=30,  # instead of 20 cause im lazy
        breedable_population_size=15,
        layers_with_bias_nodes=[True, True, True],
        input_size=[3, 3],  # must be square
        random_range=[-0.1, 0.1]
    )

    num_of_plotted_generations = 0
    game = Game(None, None)

    print('\nInitialization Complete!')

    #print( '\nPre-Evolving...')

    #MHA.pre_train_state( iterations = 10, print_progress = True )

    #print( '\nPre-Evolution Complete!')

    print('\nEvolving...')

    for generation in range(num_generations):

        if generation < 5 or generation % 5 == 4:
            print('\n\tEvolving Generation: {}...'.format(generation + 1))

        MHA.determine_fitness(
            fitness_score='blondie24',
            cutoff_type='hard cutoff',
        )

        MHA.breed(
            mutation_rate=0.01,
            crossover_type='evolutionary'
        )

        if generation < 5 or generation % 5 == 4:
            print('\n\tGeneration: {} Evolution Completed!'.format(generation + 1))

        if generation == 0 or generation % 5 == 4 or True:

            print('\n\tPlotting Generation: {}...'.format(generation + 1))

            plot_win_loss_tie(
                MHA,
                num_of_plotted_generations,
                scores[0],
                scores[1],
                scores[2]
            )

            print('\n\t\tWin-Lose-Tie Plotting Completed!')

            plot_state_value(
                MHA,
                num_of_plotted_generations,
                scores[3],
                scores[4],
                scores[5]
            )

            print('\t\tState Value Plotting Completed!')

            # this plot isn't needed but
            # provides some decent info

            # plot_strategy_effectiveness(
            #   MHA,
            #   num_of_plotted_generations,
            #   win_capture_score,
            #   loss_prevention_score
            # )

            #print( '\t\tStrategy Effectiveness Plotting Completed!' )

            print('\n\tPlotting Generation: {} Completed'.format(generation + 1))

            num_of_plotted_generations += 1

    print('\nEvolution Complete!')

    print('\n\tSaving Best Neural Network')
    neural_network_file = open(
        'metaheuristic_algorithm/ttt_board_states/best_neural_network.txt', 'w')
    neural_network_file.write('{')

    for edge, weight in MMA.fittest_chromosomes[0].weights.items():
        string = '\n{}: {}'.format(edge, weight)
        neural_network_file.write(string)

    neural_network_file.write('\n}')

    print('\n\tSaved Best Neural Network!')

    print('\nFinished!')
