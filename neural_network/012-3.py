import math
import sys
import filecmp
from numpy import random
import matplotlib.pyplot as plt
from generate_weights import generate_weights
from neural_network import NeuralNetwork
import sys
sys.path.append('metaheuristic_algorithm/')
from metaheuristic_algorithm_nn import MetaHeuristicAlgorithm, nn_chromosome
from tic_tac_toe import Game, plots_3_and_4

print( '\nStarting...' )

def calculate_score( fittest_chromosomes, population ):

    num_games = int()

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            game = Game( nn_chromosome( chromosome_one ), nn_chromosome( chromosome_two ) )
            result = game.play()

            if result[ 1 ] == 1: # chromosome 1 won
                chromosome_one[ 'score' ] += 1
            elif result[ 1 ] == 2: # chromosome 2 won
                chromosome_one[ 'score' ] -= 1
            
            game = Game( nn_chromosome( chromosome_two ), nn_chromosome( chromosome_one ) )
            result = game.play()

            if result[ 1 ] == 1: # chromosome 1 won
                chromosome_one[ 'score' ] += 1
            elif result[ 1 ] == 2: # chromosome 2 won
                chromosome_one[ 'score' ] -= 1

            num_games += 2

    score = int()

    for chromosome in fittest_chromosomes:
        score += chromosome[ 'score' ] / num_games
        chromosome[ 'score' ] = 0

    for chromosome in population:
        chromosome[ 'score' ] = 0

    return score

def calculate_score_random( fittest_chromosomes, random_function ):

    num_games = int()

    for chromosome in fittest_chromosomes:
        chromosome[ 'score' ] = 0

    for chromosome_one in fittest_chromosomes:

        game = Game( nn_chromosome( chromosome_one ), random_function )
        result = game.play()

        if result[ 1 ] == 1: # chromosome 1 won
            chromosome_one[ 'score' ] += 1
        elif result[ 1 ] == 2: # random won
            chromosome_one[ 'score' ] -= 1
        
        game = Game( random_function, nn_chromosome( chromosome_one ) )
        result = game.play()

        if result[ 1 ] == 1: # chromosome 1 won
            chromosome_one[ 'score' ] += 1
        elif result[ 1 ] == 2: # random won
            chromosome_one[ 'score' ] -= 1

        num_games += 2

    score = int()

    for chromosome in fittest_chromosomes:
        score += chromosome[ 'score' ] / num_games
        chromosome[ 'score' ] = 0

    return score

random_average_score = list()
original_average_score = list()
previous_average_score = list()

win_prediction_score = list()
lose_prediction_score = list()
tie_prediction_score = list()

win_capture_score = list()
loss_prevention_score = list()

num_generations = 250

print( '\nInitializing Meta-Heuristic Algorithm...' )

MHA = MetaHeuristicAlgorithm() 
MHA.read_chromosomes( 
    generate_weights, 
    [14, 9, 6, 1],
    population_size = 30, # instead of 20 cause im lazy
    breedable_population_size = 15,
    layers_with_bias_nodes = [ False, False, False, False ],
    input_size = [ 3, 3 ] # must be square
)

def random_function( board_state, current_player ):
    return random.choice( [ 
        i 
        for i in range( 9 ) 
        if int( board_state[ i ] ) == 0 
    ] )

plotted_generations = 0
winnable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/winnable_board_states.txt', 'r' ).readlines() ]
losable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/losable_board_states.txt', 'r' ).readlines() ]
winning_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/winning_board_states.txt', 'r' ).readlines() ]
losing_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/losing_board_states.txt', 'r' ).readlines() ]
tieing_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/tieing_board_states.txt', 'r' ).readlines() ]
game = Game( None, None )

print( '\nInitialization Complete! \n\nEvolving...' )

for generation in range( num_generations ):

    if generation < 5 or generation % 5 == 4: 
        print( '\n\tEvolving Generation: {}...'.format( generation + 1 ) )
    
    MHA.determine_fitness( fitness_score = 'blondie24', cutoff_type = 'hard cutoff' )
    MHA.breed( mutation_rate = 0.01, crossover_type = 'evolutionary' )

    if generation < 5 or generation % 5 == 4: 
        print( '\n\tGeneration: {} Evolution Completed!'.format( generation + 1 ) )

    if generation == 0 or generation % 5 == 4:

        print( '\n\tPlotting Generation: {}...'.format( generation + 1 ) )

        random_average_score.append( 
            calculate_score_random( 
                MHA.fittest_chromosomes, 
                random_function 
            ) 
        )
        
        original_average_score.append( 
            calculate_score( 
                MHA.fittest_chromosomes, 
                MHA.original_population 
            ) 
        )

        previous_average_score.append( 
            calculate_score( 
                MHA.fittest_chromosomes, 
                MHA.previous_population
            ) 
        )
        
        plt.plot( list( range( 1, plotted_generations + 2 ) ), random_average_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), original_average_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), previous_average_score )
        plt.legend( [ 'Random', 'Original', 'Previous' ] )
        plt.savefig( 'images/012-3-1.png' )
        plt.clf()

        print ('\n\t\tWin-Lose-Tie Plotting Completed!' )

        win_predictions = int() 
        num_win_predictions = int() 

        lose_predictions = int()
        num_lose_predictions = int() 

        tie_predictions = int()
        num_tie_predictions = int()

        for chromosome in MHA.fittest_chromosomes:

            for board_state in winning_board_states:

                temp = [int(space) for space in board_state]
                num_win_predictions += 1
                win_predictions = chromosome['genes'].calc_prediction(
                    {
                        'input': temp
                    }
                )
                           
            for board_state in losing_board_states:

                temp = [int(space) for space in board_state]
                num_lose_predictions += 1
                lose_predictions = chromosome['genes'].calc_prediction(
                    {
                        'input': temp
                    }
                )

            for board_state in tieing_board_states:

                temp = [int(space) for space in board_state]
                num_tie_predictions += 1
                tie_predictions = chromosome['genes'].calc_prediction(
                    {
                        'input': temp
                    }
                )

        win_prediction_score.append( win_predictions / num_win_predictions )
        lose_prediction_score.append( lose_predictions / num_lose_predictions )
        tie_prediction_score.append( tie_predictions / num_tie_predictions )

        plt.plot( list( range( 1, plotted_generations + 2 ) ), win_prediction_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), lose_prediction_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), tie_prediction_score )

        plt.legend( [ 'Win', 'Lose', 'Tie' ] )
        plt.savefig( 'images/012-3-2.png' )
        plt.clf()

        plotted_generations += 1

        print( '\t\tState Value Plotting Completed!' )

        for chromosome in MHA.fittest_chromosomes:

            for board_state in winnable_board_states:

                temp = [int(space) for space in board_state]

                win_capture = plots_3_and_4( temp, 1 ) # win capture
                
                can_win_score += 1

                current_move = nn_chromosome( chromosome )( temp, 1 )
                
                if current_move in win_capture[ 1 ]:
                    
                    will_win_score += 1

            
            for board_state in losable_board_states:

                temp = [int(space) for space in board_state]

                loss_prevention = plots_3_and_4(temp, 2) # loss prevention
                    
                can_block_score += 1

                current_move = nn_chromosome( chromosome )( temp, 1 )
                
                if current_move in loss_prevention[ 1 ]:
                    
                    will_block_score -= 1

        win_capture_score.append( will_win_score / can_win_score )
        loss_prevention_score.append( will_block_score / can_block_score )

        plt.plot( list( range( 1, plotted_generations + 2 ) ), win_capture_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), loss_prevention_score )
        plt.legend( [ 'Win Rate', 'Lose Rate' ] )
        plt.savefig( 'images/012-3-3.png' )
        plt.clf()

        print( '\t\tStrategy Effectiveness Plotting Completed!' )

        print( '\n\tPlotting Generation: {} Completed'.format( generation + 1) )

print( '\nEvolution Complete!' )

print('\n\tSaving Best Neural Network')
neural_network_file = open('metaheuristic_algorithm/ttt_board_states/best_neural_network.txt', 'w')
neural_network_file.write('{')

for edge, weight in MMA.fittest_chromosomes[ 0 ].weights.items():
    string = '\n{}: {}'.format(edge, weight)
    neural_network_file.write(string)

neural_network_file.write('\n}')

print( '\n\tSaved Best Neural Network!' )

print('\nFinished!')