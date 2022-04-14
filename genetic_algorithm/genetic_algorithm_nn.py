from numpy import random
import numpy as np
import time
import ast
import math
from tic_tac_toe import Game
import sys
sys.path.append('neural_network')
from neural_network import NeuralNetwork

class GeneticAlgorithm:
    def __init__( self ):
        self.population = list()

    def determine_fitness( self, fitness_score = 'round robin', cutoff_type = 'hard cutoff', current_bracket = None, round_number = 1 ):

        self.fittest_chromosomes = list()

        if current_bracket is None: 
            current_bracket = self.population

        matchups = self.determine_matchups( fitness_score, current_bracket = current_bracket )

        for ( i, j ) in matchups: 
            
            result = self.compete( 
                current_bracket[ i ],
                current_bracket[ j ] 
            )

            if fitness_score == 'bracket':

                if result[0] is False or result[1] == 'Draw':
                    self.compete( 
                        current_bracket[ j ], 
                        current_bracket[ i ] 
                    ) # reverse matchup and if its still a draw these two dont move on

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
        
    def determine_matchups(self, fitness_score, current_bracket = None):

        matchups = list()

        if fitness_score == 'round robin':

            for i in range( len( current_bracket ) ):

                for j in range( len( current_bracket ) ):

                    if i != j and [ i, j ] not in matchups:

                        matchups.append( [ i, j ] )

            return matchups

        elif fitness_score == 'bracket':

            for i in range( 0,  len( current_bracket ) - 1, 2 ):

                matchups.append( [ i, i + 1 ] )

            return matchups


    def breed( self, mutation_rate = 0.001, crossover_type = str(), crossover_genes_indices = list() ):

        offspring = list()

        for i, chromosome_one in enumerate( self.fittest_chromosomes ):
            
            for chromosome_two in self.fittest_chromosomes[ i + 1 : ]:

                crossover_genes_indices = get_crossover_indices( 
                    self.number_of_genes,
                    crossover_type,
                    crossover_genes_indices
                )

                mutated_genes_indices = get_mutated_chromosomes( 
                    self.number_of_genes, 
                    mutation_rate 
                ) 

                baby_chromosome_one = {'genes': NeuralNetwork( dict() ), 'score': 0}
                baby_chromosome_two = {'genes': NeuralNetwork( dict() ), 'score': 0}
                
                for edge, weight in chromosome_one[ 'genes' ].weights.keys():

                    genes = [ 
                        chromosome_one[ 'genes' ].weights[ edge ], 
                        chromosome_two[ 'genes' ].weights[ edge ] 
                    ]
                    
                    mutated_genes = [ 
                        check_mutation( genes[0], edge, mutated_genes_indices[0] ),
                        check_mutation( genes[1], edge, mutated_genes_indices[1] ) 
                    ]
                    
                    if edge in crossover_genes_indices:

                        mutated_genes = mutated_genes[ : : -1 ]

                    baby_chromosome_one[ 'genes' ].weights[ edge ] = mutated_genes[ 0 ]
                    baby_chromosome_two[ 'genes' ].weights[ edge ] = mutated_genes[ 1 ]

                offspring.append( baby_chromosome_one )
                offspring.append( baby_chromosome_two )

        self.previous_population = copy_population( self.population )
        self.population = self.fittest_chromosomes + offspring  

    def compete( self, chromosome_one, chromosome_two ):

        lambda_chromosome_one = lambda board_state, _: chromosome_one[ 'genes' ].calc_prediction( {'input': board_state} )
        lambda_chromosome_two = lambda board_state, _: chromosome_two[ 'genes' ].calc_prediction( {'input': board_state} )
        game = Game( lambda_chromosome_one, lambda_chromosome_two )
        result = game.play()

        if result[ 1 ] == 1: # chromosome 1 won
            chromosome_one[ 'score' ] += 1
            chromosome_two[ 'score' ] -= 1
        elif result[ 1 ] == 2: # chromosome 2 won
            chromosome_one[ 'score' ] -= 1
            chromosome_two[ 'score' ] += 1  

        return result

    def read_chromosomes( self, ttc_chromosome_genes_file, population_size = 64 ): # the ttc_chromosome_genes_file is a readlines() file
        
        if population_size % 2 != 0: # adjust so population size is even
            population_size = int( 2 ** ( math.floor( math.log( population_size, 2 ) ) ) )

        self.breedable_population_size = math.floor( math.sqrt( population_size ) )
        self.population_size = math.floor( self.breedable_population_size ** 2 )
        random.shuffle( ttc_chromosome_genes_file )
        
        for line in ttc_chromosome_genes_file[ : self.population_size ]:

            weights = ast.literal_eval( line ) # parse string dictionary
            new_chromosome = {'genes': NeuralNetwork( weights ), 'score': 0}
            self.population.append( new_chromosome )

        self.number_of_genes = len( genes )
        self.original_population = copy_population( self.population ) # create a copy of population for original population

def get_crossover_indices( number_of_genes, crossover_type = str(), crossover_genes_indices = list() ):

    if crossover_type == str() and crossover_genes_indices == list(): 
        
        # random indices
        crossover_genes_indices = random.choice( range( number_of_genes ), number_of_genes, replace = False )
    
    else:
    
        half_of_number_of_genes = math.ceil( len( number_of_genes ) / 2 )
        first_half_of_genes_indices = list( range( number_of_genes [ half_of_number_of_genes : ] ) )
        
        if crossover_type == 'alternating':

            crossover_genes_indices = map( lambda x: 2 * x, first_half_of_genes_indices )

        elif crossover_type == 'fiftyfifty':

            crossover_genes_indices = first_half_of_genes_indices

    return crossover_genes_indices

def hard_cutoff( population, breedable_population_size ):

    population.sort( key = lambda chromosome: chromosome[ 'score' ], reverse = True )

    return population[ : breedable_population_size ]

def stochastic( population, breedable_population_size ): 

    fittest_chromosomes = []
    
    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.choice( population, math.floor( breedable_population_size / 2 ), replace = False )
        fittest_chromosome = max( heat, key = lambda chromosome: chromosome[ 'score' ] )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

    return fittest_chromosomes

def tournament( population, breedable_population_size ): 

    fittest_chromosomes = []
    
    for chromosome in population:
        chromosome[ 'score' ] = 0

    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.choice( population, math.floor( breedable_population_size / 2 ), replace = False )

        for i, chromosome_one in enumerate( heat ):

            for j, chromosome_two in enumerate( heat ):

                if i != j:

                    game = Game( chromosome_one[ 'genes' ], chromosome_two[ 'genes' ] )
                    result = game.play()

                    if result[ 1 ] == 1: # chromosome 1 won
                        chromosome_one[ 'score' ] += 1
                        chromosome_two[ 'score' ] -= 1

                    elif result[ 1 ] == 2: # chromosome 2 won
                        chromosome_one[ 'score' ] -= 1
                        chromosome_two[ 'score' ] += 1  
                    
        fittest_chromosome = max( heat, key = lambda chromosome: chromosome[ 'score' ] )
        fittest_chromosomes.append( fittest_chromosome )
        fittest_chromosome_index = population.index( fittest_chromosome )
        population.pop( fittest_chromosome_index )

        for chromosome in heat:
            chromosome[ 'score' ] = 0

    return fittest_chromosomes

def check_mutation( gene, gene_index, mutated_genes ):
    return get_random_move() if gene_index in mutated_genes else gene

def get_random_move():
    gaussian_random_numbers = np.random.normal( 0, 3, 1000 )
    np.random.shuffle( gaussian_random_numbers )
    return gaussian_random_numbers[0]

def copy_population( population ):
    return list( population )
    
def get_mutated_chromosomes( number_of_genes, mutation_rate ):

    number_of_mutated_genes = math.ceil( number_of_genes * mutation_rate )
    chromosome_one_mutated_genes = random.choice( range( number_of_genes ), number_of_mutated_genes, replace = False )
    chromosome_two_mutated_genes = random.choice( range( number_of_genes ), number_of_mutated_genes, replace = False  )
    return [ chromosome_one_mutated_genes, chromosome_two_mutated_genes ]
