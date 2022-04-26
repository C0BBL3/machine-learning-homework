import random
import matplotlib.pyplot as plt
from tic_tac_toe import Game, plots_3_and_4
from metaheuristic_algorithm import MetaHeuristicAlgorithm

def calculate_score( fittest_chromosomes, population ):

    for chromosome_one in fittest_chromosomes:

        for chromosome_two in population:

            if chromosome_one in population or chromosome_two in fittest_chromosomes:
                continue

            lambda_chromosome_one = lambda board_state, _: chromosome_one[ 'genes' ][ board_state ] 
            lambda_chromosome_two = lambda board_state, _: chromosome_two[ 'genes' ][ board_state ]
            
            MHA.compete( lambda_chromosome_one, lambda_chromosome_two )
            chromosome_two[ 'score' ] = 0

            MHA.compete( lambda_chromosome_two, lambda_chromosome_one )
            chromosome_two[ 'score' ] = 0

    score = list()

    for chromosome in fittest_chromosomes:
        score.append( chromosome[ 'score' ] / len( fittest_chromosomes ) )
        chromosome[ 'score' ] = 0

    return sum( score )

original_average_score = [ [], [], [], [], [], [], [] ]
previous_average_score = [ [], [], [], [], [], [], [] ]
win_capture_score = [ [], [], [], [], [], [], [] ]
loss_prevention_score = [ [], [], [], [], [], [], [] ] # | || || |_

num_generations = 50

ttc_chromosome_genes = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/ttc_chromosome_genes.txt', 'r' ).readlines() ]
# ^^^^^ tic tac toe chromosome genes

metaheuristic_algorithms = list()
sizes = [ 64, 64, 256, 256, 1024, 1024 ]
mutation_rates = [ 0.01, 0.001, 0.01, 0.001, 0.01, 0.001 ] 

for i in range(6):
    MHA = MetaHeuristicAlgorithm()
    MHA.read_chromosomes( ttc_chromosome_genes, population_size = sizes[ i ] )
    metaheuristic_algorithms.append(MHA)
    del MHA

for generation in range( num_generations ):
    
    if generation < 5 or generation % 10 == 9 or generation == num_generations - 1: 
        print( '\nGeneration:', generation + 1 )

    for i, MHA in enumerate( metaheuristic_algorithms ):

        MHA.determine_fitness( fitness_score = 'bracket', cutoff_type = 'stochastic' )
        MHA.breed( mutation_rate = 0.01 )

        original_average_score[ i ].append( calculate_score( MHA.fittest_chromosomes, MHA.original_population ) )
        previous_average_score[ i ].append( calculate_score( MHA.fittest_chromosomes, MHA.previous_population ) )

        can_win_score = 0
        can_block_score = 0
        will_win_score = 0
        will_block_score = 0

        for chromosome in MHA.fittest_chromosomes:
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

        win_capture_score[ i ].append( will_win_score / ( can_win_score + 1) )
        loss_prevention_score[ i ].append( will_block_score / ( can_block_score + 1) )

plt.plot( list( range( num_generations ) ), original_average_score[ 0 ] )
plt.plot( list( range( num_generations ) ), original_average_score[ 1 ] )
plt.plot( list( range( num_generations ) ), original_average_score[ 2 ] )
plt.plot( list( range( num_generations ) ), original_average_score[ 3 ] )
plt.plot( list( range( num_generations ) ), original_average_score[ 4 ] )
plt.plot( list( range( num_generations ) ), original_average_score[ 5 ] )
plt.legend( [ '64-0.01', '64-0.001', '256-0.01', '256-0.001', '1024-0.01', '1024-0.001' ] )
plt.savefig( 'images/011-6-1.png' )

plt.clf()

plt.plot( list( range( num_generations ) ), previous_average_score[ 0 ] )
plt.plot( list( range( num_generations ) ), previous_average_score[ 1 ] )
plt.plot( list( range( num_generations ) ), previous_average_score[ 2 ] )
plt.plot( list( range( num_generations ) ), previous_average_score[ 3 ] )
plt.plot( list( range( num_generations ) ), previous_average_score[ 4 ] )
plt.plot( list( range( num_generations ) ), previous_average_score[ 5 ] )
plt.legend( [ '64-0.01', '64-0.001', '256-0.01', '256-0.001', '1024-0.01', '1024-0.001' ] )
plt.savefig( 'images/011-6-2.png' )

plt.clf()

plt.plot( list( range( num_generations ) ), win_capture_score[ 0 ] )
plt.plot( list( range( num_generations ) ), win_capture_score[ 1 ] )
plt.plot( list( range( num_generations ) ), win_capture_score[ 2 ] )
plt.plot( list( range( num_generations ) ), win_capture_score[ 3 ] )
plt.plot( list( range( num_generations ) ), win_capture_score[ 4 ] )
plt.plot( list( range( num_generations ) ), win_capture_score[ 5 ] )
plt.legend( [ '64-0.01', '64-0.001', '256-0.01', '256-0.001', '1024-0.01', '1024-0.001' ] )
plt.savefig( 'images/011-6-3.png' )

plt.clf()

plt.plot( list( range( num_generations ) ), loss_prevention_score[ 0 ] )
plt.plot( list( range( num_generations ) ), loss_prevention_score[ 1 ] )
plt.plot( list( range( num_generations ) ), loss_prevention_score[ 2 ] )
plt.plot( list( range( num_generations ) ), loss_prevention_score[ 3 ] )
plt.plot( list( range( num_generations ) ), loss_prevention_score[ 4 ] )
plt.plot( list( range( num_generations ) ), loss_prevention_score[ 5 ] )
plt.legend( [ '64-0.01', '64-0.001', '256-0.01', '256-0.001', '1024-0.01', '1024-0.001' ] )
plt.savefig( 'images/011-6-4.png' )
