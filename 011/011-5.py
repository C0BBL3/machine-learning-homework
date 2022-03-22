import random
import matplotlib.pyplot as plt
from tic_tac_toe import Game, plots_3_and_4
from genetic_algorithm import GeneticAlgorithm

def calculate_score( fittest_chromosomes, population ):

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            if chromosome_one in population or chromosome_two in fittest_chromosomes:
                continue

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
win_capture_score = list()
loss_prevention_score = list() # | || || |_

num_generations = 100

ttc_chromosome_genes = [ line.strip( '\n' ) for line in open( '011/ttc_chromosome_genes.txt', 'r' ).readlines() ]
# ^^^^^ tic tac toe chromosome genes

def get_fittest_chromosomes_function_stochastic( population, breedable_population_size ): 
    fittest_chromosomes = []
    
    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.sample( population, math.floor( breedable_poplulation_size / 2 ) )
        fittest_chromosome = max( heat, key = lambda chromosome: chromosome[ 'score' ] )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

    return fittest_chromosomes

def get_fittest_chromosomes_function_tournemant( population, breedable_population_size ): 
    fittest_chromosomes = []
    
    for chromosome in population:
        chromosome[ 'score' ] = 0

    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.sample( population, math.floor( breedable_poplulation_size / 2 ) )

        for i, chromosome_one in enumerate( heat ):
            for j, chromosome_two in enumerate( heat ):
                if i != j:
                    GA.compete( chromosome_one, chromosome_two )
                    
        fittest_chromosome = max( heat, key = lambda chromosome: chromosome[ 'score' ] )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

    return fittest_chromosomes

GA = GeneticAlgorithm()
GA.read_chromosomes( ttc_chromosome_genes, population_size = 64 )

for generation in range( num_generations ):
    
    if generation < 5 or generation % 10 == 9: 
        print( '\nGeneration:', generation + 1 )

    GA.determine_fitness( fitness_score = 'bracket', get_fittest_chromosome_function = get_fittest_chromosomes_function_stochastic )
    GA.breed( mutation_rate = 0.001 )

    original_average_score.append( calculate_score( GA.fittest_chromosomes, GA.original_population ) )
    previous_average_score.append( calculate_score( GA.fittest_chromosomes, GA.previous_population ) )

    can_win_score = 0
    can_block_score = 0
    will_win_score = 0
    will_block_score = 0

    for chromosome in GA.fittest_chromosomes:
        for board_state in chromosome[ 'genes' ].keys():
            list_board_state = [ int( space ) for space in board_state ]
            win_capture = plots_3_and_4( list_board_state, 1 ) # win capture
            if win_capture[ 0 ]:
                can_win_score += 1
                if chromosome[ 'genes' ][ board_state ] in win_capture[ 1 ]:
                    will_win_score += 1
            loss_prevention = plots_3_and_4( list_board_state, 2 ) # loss prevention
            if loss_prevention[ 0 ]:
                can_block_score += 1
                if chromosome[ 'genes' ][ board_state ] in loss_prevention[ 1 ]:
                    will_block_score += 1 

    win_capture_score.append( will_win_score / can_win_score )
    loss_prevention_score.append( will_block_score / can_block_score )

plt.plot( list( range( num_generations ) ), original_average_score )
plt.plot( list( range( num_generations ) ), previous_average_score )
plt.legend( [ 'Original', 'Previous' ] )
plt.savefig( 'images/011-5-1.png' )

plt.clf()

plt.plot( list( range( num_generations ) ), win_capture_score )
plt.plot( list( range( num_generations ) ), loss_prevention_score )
plt.legend( [ 'Win Capture', 'Loss Prevention' ] )
plt.savefig( 'images/011-5-2.png' )
