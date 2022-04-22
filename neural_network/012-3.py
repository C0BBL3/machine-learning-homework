import math
import sys
from numpy import random
import matplotlib.pyplot as plt
from generate_weights import generate_weights
from neural_network import NeuralNetwork
import sys
sys.path.append('metaheuristic_algorithm/')
from metaheuristic_algorithm_nn import MetaHeuristicAlgorithm, nn_chromosome
from tic_tac_toe import Game

print( '\nStarting...' )

def calculate_score( fittest_chromosomes, population ):

    num_games = int()

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            #if chromosome_one is chromosome_two: continue
            
            MHA.compete( chromosome_one, chromosome_two )
            chromosome_two[ 'score' ] = 0

            MHA.compete( chromosome_two, chromosome_one )
            chromosome_two[ 'score' ] = 0

            num_games += 2

    score = int()

    for chromosome in fittest_chromosomes:
        score += chromosome[ 'score' ] / num_games
        chromosome[ 'score' ] = 0

    for chromosome in population:
        chromosome[ 'score' ] = 0

    return score

def calculate_score_random( fittest_chromosomes, random_population ):

    num_games = int()

    for chromosome in fittest_chromosomes:
        chromosome[ 'score' ] = 0

    for chromosome_one in fittest_chromosomes:

        for random_function in random_population:

            game = Game( nn_chromosome( chromosome_one ), random_function )
            result = game.play()

            if result[ 1 ] == 1: # chromosome 1 won
                chromosome_one[ 'score' ] += 1
            elif result[ 1 ] == 2: # chromosome 2 won
                chromosome_one[ 'score' ] -= 1
            
            game = Game( random_function, nn_chromosome( chromosome_one ) )
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

    return score

random_average_score = list()
original_average_score = list()
previous_average_score = list()

num_generations = 100

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

random_population = [ random_function ]

print( '\nInitialization Complete! \n\nEvolving...' )

for generation in range( num_generations ):
    
    MHA.determine_fitness( fitness_score = 'blondie24', cutoff_type = 'hard cutoff' )
    MHA.breed( mutation_rate = 0.01, crossover_type = 'evolutionary' )

    random_average_score.append( calculate_score_random( MHA.fittest_chromosomes, random_population ) )
    original_average_score.append( calculate_score( MHA.fittest_chromosomes, MHA.original_population ) )
    previous_average_score.append( calculate_score( MHA.fittest_chromosomes, MHA.previous_population ) )

    plt.plot( list( range( 1, generation + 2 ) ), random_average_score )
    plt.plot( list( range( 1, generation + 2 ) ), original_average_score )
    plt.plot( list( range( 1, generation + 2 ) ), previous_average_score )
    plt.legend( [ 'Random', 'Original', 'Previous' ] )
    plt.savefig( 'images/012-3-1.png' )
    plt.clf()

    if generation < 5 or generation % 10 == 9: 
        print( '\n\tGeneration:', generation + 1, 'Completed!' )

print( '\nEvolution Complete!' )