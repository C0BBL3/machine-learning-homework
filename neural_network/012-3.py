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

def calculate_score( fittest_chromosomes, population ):

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            if chromosome_one in population or chromosome_two in fittest_chromosomes:
                continue

            
            MHA.compete( chromosome_one, chromosome_two )
            chromosome_two[ 'score' ] = 0

            MHA.compete( chromosome_two, chromosome_one )
            chromosome_two[ 'score' ] = 0

    score = list()

    for chromosome in fittest_chromosomes:
        score.append( chromosome[ 'score' ] / len( fittest_chromosomes ) )
        chromosome[ 'score' ] = 0

    return sum( score )

def calculate_score_random( fittest_chromosomes, random_population ):

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

    score = list()

    for chromosome in fittest_chromosomes:
        score.append( chromosome[ 'score' ] / len( fittest_chromosomes ) )
        chromosome[ 'score' ] = 0

    return sum( score )

random_average_score = list()
original_average_score = list()
previous_average_score = list()

num_generations = 100

MHA = MetaHeuristicAlgorithm()
MHA.read_chromosomes( 
    generate_weights, 
    [14, 9, 6, 1],
    population_size = 30, # instead of 30 cause im lazy
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

random_population = [ 
    random_function
    for _ in range(30)
]

for generation in range( num_generations ):
    
    if generation < 5 or generation % 10 == 9: 
        print( '\nGeneration:', generation + 1 )

    MHA.determine_fitness( fitness_score = 'blondie24', cutoff_type = 'hard cutoff' )
    MHA.breed( mutation_rate = 0.01, crossover_type = 'evolutionary' )

    random_average_score.append( calculate_score_random( MHA.fittest_chromosomes, random_population ) )
    original_average_score.append( calculate_score( MHA.fittest_chromosomes, MHA.original_population ) )
    previous_average_score.append( calculate_score( MHA.fittest_chromosomes, MHA.previous_population ) )

    plt.plot( list( range( generation ) ), random_average_score )
    plt.plot( list( range( generation ) ), original_average_score )
    plt.plot( list( range( generation ) ), previous_average_score )
    plt.legend( [ 'Random', 'Original', 'Previous' ] )
    plt.savefig( 'images/012-3-1.png' )
    plt.clf()