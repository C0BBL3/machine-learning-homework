from numpy import random
import numpy as np
import time
import ast
import math
import multiprocessing
from multiprocessing import Pool
from tic_tac_toe import Game
import sys
sys.path.append('neural_network/')
from neural_network import NeuralNetwork
sys.path.pop()
sys.path.append('min_max_algorithm/')
from minimax import Minimax

class MetaHeuristicAlgorithm:
    def __init__( self ):
        self.population = list()

    def determine_fitness( self, fitness_score = 'round robin', cutoff_type = 'hard cutoff', current_bracket = None, round_number = 1, breedable_population_size = int() ):
        
        self.fittest_chromosomes = list()

        if current_bracket is None: 
            current_bracket = self.population

        self.current_bracket = current_bracket
        workers = dict()
        available_thread_count = multiprocessing.cpu_count() - 1
        lock = multiprocessing.Lock()

        matchups = determine_matchups( 
            fitness_score, 
            current_bracket = current_bracket 
        )

        random.shuffle( matchups )

        num_of_matchups_per_core = math.floor( 
            len( matchups) /
            available_thread_count
        )

        return_list = {
            i: multiprocessing.Manager().Value( 'i', 0 )
            for i in range( len( self.current_bracket ) )
        }

        for i in range(0, len( matchups ), num_of_matchups_per_core ):

            matchups_arg = matchups[ i : num_of_matchups_per_core + i ] 
            args = [ 
                fitness_score,
                matchups_arg, 
                return_list, 
                lock
            ]

            worker = multiprocessing.Process( 
                target = self.multi_core_compete, 
                args = args
            )

            worker.start()
            workers[ i ] = worker

        for worker in workers.values():
            worker.join()
            
        for i, worker_return in enumerate( return_list.values() ):

            self.current_bracket[ i ][ 'score' ] = int( worker_return.value )

        if fitness_score == 'bracket' and len( matchups ) > 1:

            next_round_population = list()

            for chromosome in current_bracket:
                if chromosome[ 'score' ] == round_number:
                    next_round_population.append(chromosome)

            self.determine_fitness( 
                fitness_score = fitness_score, 
                current_bracket = next_round_population, 
                round_number = round_number + 1 
            )
        
        if cutoff_type == 'hard cutoff':
            self.fittest_chromosomes = hard_cutoff( 
                self.population,
                self.breedable_population_size
            ) 
        elif cutoff_type == 'stochastic':
            self.fittest_chromosomes = stochastic( 
                self.population,
                self.breedable_population_size
            )
        elif cutoff_type == 'tournament':
            self.fittest_chromosomes = tournament( 
                self.population,
                self.breedable_population_size
            )
            
        temp = int()
        print('\n', len(self.population))
        for chromosome in self.population:
            temp += chromosome[ 'score' ]
            print( chromosome[ 'score' ] )
            chromosome[ 'score' ] = int()

        print('score distribution', temp)

    def multi_core_compete( self, fitness_score, matchups, return_dict, lock ): # nasty
        
        for ( i, j ) in matchups:
            
            result = self.compete( 
                self.population[ i ],
                self.population[ j ]
            )

            if fitness_score == 'bracket':

                if result[ 0 ] is False or result[ 1 ] == 'Draw':
                    self.compete(
                        self.population[ j ],
                        self.population[ i ]
                    ) # reverse matchup and if its still a draw these two dont move on

        lock.acquire()
        temp = int()
        
        for ( i, j ) in matchups:            

            temp += self.population[ i ][ 'score' ]
            temp += self.population[ j ][ 'score' ]
            return_dict[ i ].value += self.population[ i ][ 'score' ]
            return_dict[ j ].value += self.population[ j ][ 'score' ]

        print(temp)
        lock.release()

    def breed( self, mutation_rate = 0.001, crossover_type = 'random', crossover_genes_indices = list() ):

        offspring = list()
        
        if crossover_type == 'evolutionary': # evolutionary breeding (one parent producing one offspring)
            
            for chromosome in self.fittest_chromosomes:
                
                child = {
                    'genes': chromosome[ 'genes' ].mitosis(),
                    'score': int()
                }

                while child in offspring or child in self.population:

                    child = {
                        'genes': chromosome[ 'genes' ].mitosis(),
                        'score': int()
                    }
                
                offspring.append( child )

        else: # genetic breeding (two parents producing two offspring)

            for i, chromosome_one in enumerate( self.fittest_chromosomes ):
                
                for chromosome_two in self.fittest_chromosomes[ i + 1 : ]:

                    crossover_genes_indices = get_crossover_indices( 
                        self.number_of_genes,
                        mutation_rate,
                        crossover_type,
                        crossover_genes_indices
                    )

                    mutated_genes_indices = get_mutated_chromosomes( 
                        self.number_of_genes, 
                        mutation_rate 
                    ) 

                    baby_chromosome_one = dict()
                    baby_chromosome_two = dict()
                    
                    edges = chromosome_one[ 'genes' ].weights.keys()
                    
                    for edge_index, edge in enumerate( edges ):

                        gene = [ 
                            chromosome_one[ 'genes' ].weights[ edge ], 
                            chromosome_two[ 'genes' ].weights[ edge ] 
                        ]
                        
                        gene = [ 
                            check_mutation( gene[ 0 ], edge, mutated_genes_indices[ 0 ] ),
                            check_mutation( gene[ 1 ], edge, mutated_genes_indices[ 1 ] ) 
                        ]
                        
                        if edge_index in crossover_genes_indices:

                            gene = gene[ : : -1 ]

                        baby_chromosome_one[ edge ] = gene[ 0 ]
                        baby_chromosome_two[ edge ] = gene[ 1 ]

                    baby_chromosome_one = {
                        'genes': NeuralNetwork( baby_chromosome_one ), 
                        'score': 0
                    }
                    
                    baby_chromosome_two = {
                        'genes': NeuralNetwork( baby_chromosome_two ), 
                        'score': 0
                    }

                    offspring.append( baby_chromosome_one )
                    offspring.append( baby_chromosome_two )

        self.previous_population = copy_population( self.population )
        self.population = copy_population( self.fittest_chromosomes + offspring ) 

    def compete( self, chromosome_one, chromosome_two ):
        
        game = Game( 
            nn_chromosome( chromosome_one ), 
            nn_chromosome( chromosome_two ) 
        )

        result = game.play()

        if result[ 1 ] == 1: # chromosome 1 won
            chromosome_one[ 'score' ] += 1
            chromosome_two[ 'score' ] -= 1
        elif result[ 1 ] == 2: # chromosome 2 won
            chromosome_one[ 'score' ] -= 1
            chromosome_two[ 'score' ] += 1  

        return result

    def read_chromosomes( self, generate_weights_function, layer_sizes, layers_with_bias_nodes, population_size = 64, breedable_population_size = None, input_size = list(), random_bool = True, random_range = [ -1.0, 1.0 ] ): # the ttc_chromosome_genes_file is a readlines() file

        if breedable_population_size is None:
        
            self.breedable_population_size = math.floor( 
                math.sqrt( 
                    population_size 
                ) 
            )
            
        else:

            self.breedable_population_size = breedable_population_size

        self.population_size = population_size
        input_size_int = input_size[ 0 ] * input_size[ 1 ]
        bias_shift = layers_with_bias_nodes.count( True )

        activation_functions = [ 
            lambda x: x
            for _ in range( input_size_int )
        ] + [ 
            lambda x: tanh(x) 
            for _ in range( sum( layer_sizes ) + bias_shift ) 
        ]

        bias_node_indices = [ 
            9 + sum( layer_sizes[ 0 : i ] ) + i - 1 
            for i in range( 1, len( layer_sizes ) ) 
        ]

        for bias_node_index in bias_node_indices:
            activation_functions[ bias_node_index ] = lambda x: x
        
        for _ in range( self.population_size ):

            genes = generate_weights_function(
                layer_sizes,
                random_bool = random_bool, 
                random_range = random_range,
                layers_with_bias_nodes = layers_with_bias_nodes,
                input_size = input_size
            )

            new_chromosome = {
                'genes': NeuralNetwork( 
                    genes, # weights
                    functions = activation_functions, 
                    alpha = 0.01
                ),
                'score': 0
            }

            self.population.append( new_chromosome )

        self.number_of_genes = len( genes )
        self.original_population = copy_population( self.population ) # create a copy of population for original population

def determine_matchups(fitness_score, current_bracket = None):

    matchups = list()

    if fitness_score == 'round robin':

        for i in range( len( current_bracket ) ):

            for j in range( len( current_bracket ) ):

                if i != j and [ i, j ] not in matchups:

                    matchups.append( [ i, j ] )

    elif fitness_score == 'bracket':

        for i in range( 0,  len( current_bracket ) - 1, 2 ):

            matchups.append( [ i, i + 1 ] )

    elif fitness_score == 'blondie24':

        for i in range( len( current_bracket ) ):

            for _ in range( 5 ):
            
                j = random.choice( list( range( len( current_bracket ) ) ) )

                while [i, j] in matchups and [j, i] in matchups: 

                    # re-roll j so we dont have two of the same games 
                    # with the same players (order doesnt matter)

                    j = random.choice( list( range( len( current_bracket ) ) ) )

                matchups.append( [i, j] )

    return matchups

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
    return 2 / denominator

def nn_chromosome(chromosome):

    evaluation_function = lambda board_state, current_player: chromosome['genes'].calc_prediction(
        {
            'input': [ 
                { 0: 0, 1: -1, 2: 1 }[ space ] # double checking if 
                if current_player == 2 else   # board state  is in 
                { 0: 0, 1: 1, 2: -1 }[ space ] # current player format
                for space in board_state
            ]
        }
    )

    return lambda board_state, current_player: minimax_function(
        board_state, 
        evaluation_function, 
        current_player
    )

def minimax_function( board_state, evaluation_function, current_player ):
    minimax = Minimax()
    
    minimax.generate_tree(
        Game( None, None, current_player = current_player ), 
        current_player, 
        root_board_state = board_state, 
        max_depth = 5
    )

    minimax.evaluate_game_tree(
        Game( None, None ), 
        evaluation_function
    )
    
    return minimax.get_best_move( board_state )

def get_crossover_indices( number_of_genes, mutation_rate, crossover_type = 'random', crossover_genes_indices = list() ):

    if crossover_type == 'random': 
        
        # random indices
        crossover_genes_indices = random.choice( 
            range( number_of_genes ), 
            round( number_of_genes * mutation_rate ), 
            replace = False
        )
    
    else:
    
        half_of_number_of_genes = math.ceil( number_of_genes / 2 )
        first_half_of_genes_indices = list( range( half_of_number_of_genes ) )
        
        if crossover_type == 'alternating': 

            # every even is a crossover
            crossover_genes_indices = list ( map( 
                lambda x: 2 * x, 
                first_half_of_genes_indices 
            ) )

        elif crossover_type == 'fiftyfifty':

            # first half is a crossover
            crossover_genes_indices = first_half_of_genes_indices

    return crossover_genes_indices

def hard_cutoff( population, breedable_population_size ):

    population.sort( 
        key = lambda chromosome: chromosome[ 'score' ], 
        reverse = True 
    )

    return population[ : breedable_population_size ]

def stochastic( population, breedable_population_size ): 

    fittest_chromosomes = []
    
    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.choice( 
            population, 
            math.floor( 
                breedable_population_size / 2 
            ), 
            replace = False
        )
        fittest_chromosome = max(
            heat, 
            key = lambda chromosome: chromosome[ 'score' ]
        )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

    return fittest_chromosomes

def tournament( population, breedable_population_size ): 

    fittest_chromosomes = []
    
    for chromosome in population:
        chromosome[ 'score' ] = 0

    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.choice( 
            population, 
            math.floor( breedable_population_size / 2 ), 
            replace = False
        )

        for i, chromosome_one in enumerate( heat ):

            for j, chromosome_two in enumerate( heat ):

                if i != j:

                    game = Game( 
                        chromosome_one[ 'genes' ], 
                        chromosome_two[ 'genes' ] 
                    )
                    result = game.play()

                    if result[ 1 ] == 1: # chromosome 1 won
                        chromosome_one[ 'score' ] += 1
                        chromosome_two[ 'score' ] -= 1

                    elif result[ 1 ] == 2: # chromosome 2 won
                        chromosome_one[ 'score' ] -= 1
                        chromosome_two[ 'score' ] += 1  
                    
        fittest_chromosome = max( 
            heat,
            key = lambda chromosome: chromosome[ 'score' ]
        )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

        for chromosome in heat:
            chromosome[ 'score' ] = 0

    return fittest_chromosomes

def check_mutation( gene, gene_index, mutated_genes ):
    return calculate_mutation() if gene_index in mutated_genes else gene

def calculate_mutation():
    gaussian_random_numbers = np.random.normal( 0, 1, 1000 )
    np.random.shuffle( 
        gaussian_random_numbers
    )
    return gaussian_random_numbers[0]

def copy_population( population ):

    copy_population_list = list()

    for chromosome in population:

        copy_chromosome = {
            'genes': NeuralNetwork( 
                chromosome[ 'genes' ].weights,
                data_type = chromosome[ 'genes' ].data_type,
                functions = chromosome[ 'genes' ].functions,
                derivatives = chromosome[ 'genes' ].derivatives,
                alpha = chromosome[ 'genes' ].alpha

            ),
            'score': int()
        }

        copy_population_list.append( copy_chromosome )
    
    return copy_population_list
    
def get_mutated_chromosomes( number_of_genes, mutation_rate ):

    number_of_mutated_genes = math.ceil( 
        number_of_genes * mutation_rate
    )
    chromosome_one_mutated_genes = random.choice( 
        range( number_of_genes ), 
        number_of_mutated_genes, 
        replace = False )
    chromosome_two_mutated_genes = random.choice( 
        range( number_of_genes ), 
        number_of_mutated_genes, 
        replace = False  )
    return [ 
        chromosome_one_mutated_genes, 
        chromosome_two_mutated_genes 
    ]
