import math
import sys
from generate_weights import generate_weights
from neural_network import NeuralNetwork
import sys
sys.path.append('genetic_algorithm/')
from genetic_algorithm_nn import GeneticAlgorithm, nn_chromosome
from tic_tac_toe import Game

def calculate_score( fittest_chromosomes, population ):

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            if chromosome_one in population or chromosome_two in fittest_chromosomes:
                continue

            lambda_chromosome_one = lambda board_state, _: chromosome_one[ 'genes' ][ board_state ] 
            lambda_chromosome_two = lambda board_state, _: chromosome_two[ 'genes' ][ board_state ]
            
            GA.compete( chromosome_one, chromosome_two )
            chromosome_two[ 'score' ] = 0

            GA.compete( chromosome_two, chromosome_one )
            chromosome_two[ 'score' ] = 0

    score = list()

    for chromosome in fittest_chromosomes:
        score.append( chromosome[ 'score' ] / len( fittest_chromosomes ) )
        chromosome[ 'score' ] = 0

    return sum( score )

original_average_score = list()
previous_average_score = list()

num_generations = 100

GA = GeneticAlgorithm()
GA.read_chromosomes( 
    generate_weights, 
    [14, 9, 6, 1], 
    population_size = 30, # instead of 30 cause im lazy
    breedable_population_size = 15,
    layers_with_bias_nodes = [ False, False, False, False ] # nothing
    #[ # everything but output
        #True if i < len(layer_sizes) - 1 
        #else False 
        #for i in range( len( layer_sizes ) ) 
    #]
)

for generation in range( num_generations ):
    
    if generation < 5 or generation % 10 == 9: 
        print( '\nGeneration:', generation + 1 )

    GA.determine_fitness( fitness_score = 'blondie24', cutoff_type = 'hard cutoff' )
    GA.breed( mutation_rate = 0.01, crossover_type = 'none' )

    original_average_score.append( calculate_score( GA.fittest_chromosomes, GA.original_population ) )
    previous_average_score.append( calculate_score( GA.fittest_chromosomes, GA.previous_population ) )

import matplotlib.pyplot as plt

plt.plot( list( range( num_generations ) ), original_average_score )
plt.plot( list( range( num_generations ) ), previous_average_score )
plt.legend( [ 'Original', 'Previous' ] )
plt.savefig( 'images/012-3.png' )