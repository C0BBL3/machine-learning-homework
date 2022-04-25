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

win_capture_score = list()
tie_score_list = list()
loss_prevention_score = list()

random_average_score = list()
original_average_score = list()
previous_average_score = list()

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
winnable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/winnable_board_states.txt', 'r' ).readlines() ]
losable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/losable_board_states.txt', 'r' ).readlines() ]
game = Game( None, None )

print( '\nInitialization Complete! \n\nEvolving...' )

for generation in range( num_generations ):
    
    MHA.determine_fitness( fitness_score = 'blondie24', cutoff_type = 'hard cutoff' )
    MHA.breed( mutation_rate = 0.01, crossover_type = 'evolutionary' )

    if generation == 0 or generation % 5 == 4:

        random_average_score.append( 
            calculate_score_random( 
                MHA.fittest_chromosomes, 
                random_function 
            ) 
        )
        
        original_average_score.append( 
            calculate_score( 
                MHA.fittest_chromosomes, 
                MHA.original_population[ : MHA.breedable_population_size ] 
            ) 
        )

        previous_average_score.append( 
            calculate_score( 
                MHA.fittest_chromosomes, 
                MHA.previous_population[ : MHA.breedable_population_size ] 
            ) 
        )
        
        plt.plot( list( range( 1, plotted_generations + 2 ) ), random_average_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), original_average_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), previous_average_score )
        plt.legend( [ 'Random', 'Original', 'Previous' ] )
        plt.savefig( 'images/012-3-1.png' )
        plt.clf()

        can_win_score = int()
        can_block_score = int()
        can_tie_score = int()
        will_tie_score = int()
        will_win_score = int()
        will_block_score = int()

        for chromosome in MHA.fittest_chromosomes:

            for board_state in winnable_board_states:

                temp = [int(space) for space in board_state]

                win_capture = plots_3_and_4( temp, 1 ) # win capture
                
                can_win_score += 1
                can_tie_score += 1

                current_move = nn_chromosome( chromosome )( temp, 1 )
                
                if current_move in win_capture[ 1 ]:
                    
                    will_win_score += 1

                else:

                    temp_2 = temp[ : current_move ] + [ 1 ] + temp[ current_move + 1 : ]

                    if not game.game_finished( temp_2 )[ 0 ]:
                        
                        will_tie_score += 1
            
            for board_state in losable_board_states:

                temp = [int(space) for space in board_state]

                loss_prevention = plots_3_and_4(temp, 2) # loss prevention
                    
                can_block_score += 1
                can_tie_score += 1

                current_move = nn_chromosome( chromosome )( temp, 1 )
                
                if current_move in loss_prevention[ 1 ]:
                    
                    will_block_score -= 1

                else:

                    temp_2 = temp[ : current_move ] + [ 2 ] + temp[ current_move + 1 : ]

                    if not game.game_finished( temp_2 )[ 0 ]:
                        
                        will_tie_score += 1

        win_capture_score.append( will_win_score / can_win_score )
        loss_prevention_score.append( will_block_score / can_block_score )
        tie_score_list.append( will_tie_score / can_tie_score )

        plt.plot( list( range( 1, plotted_generations + 2 ) ), win_capture_score )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), tie_score_list )
        plt.plot( list( range( 1, plotted_generations + 2 ) ), loss_prevention_score )
        plt.legend( [ 'Win', 'Tie', 'Loss' ] )
        plt.savefig( 'images/012-3-2.png' )
        plt.clf()

        plotted_generations += 1

    if generation < 5 or generation % 5 == 4: 
        print( '\n\tGeneration:', generation + 1, 'Completed!' )

print( '\nEvolution Complete!' )

neural_network_file = open('metaheuristic_algorithm/best_neural_network.txt', 'w')
neural_network_file.write('{')

for edge, weight in MMA.fittest_chromosomes[ 0 ].weights.items():
    string = '\n{}: {}'.format(edge, weight)
    neural_network_file.write(string)

neural_network_file.write('\n}')

print( '\nSaved Best Neural Network!' )