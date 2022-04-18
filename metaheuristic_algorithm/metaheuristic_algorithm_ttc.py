import random
import numpy as np
import time
import ast
import math
from tic_tac_toe import Game

class MetaHeuristicAlgorithm:
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


    def breed( self, mutation_rate = 0.001 ):

        offspring = list()

        for i, chromosome_one in enumerate( self.fittest_chromosomes ):
            for chromosome_two in self.fittest_chromosomes[ i + 1 : ]:

                mutated_genes_indices = get_mutated_chromosomes( 
                    self.number_of_genes, 
                    mutation_rate 
                ) 

                baby_chromosome_one = {'genes': {}, 'score': 0}
                baby_chromosome_two = {'genes': {}, 'score': 0}
                
                for gene_index, board_state in enumerate( chromosome_one[ 'genes' ].keys() ):

                    genes = [ 
                        chromosome_one[ 'genes' ][ board_state ], 
                        chromosome_two[ 'genes' ][ board_state ] 
                    ]
                    mutated_genes = [ 
                        check_mutation( board_state, genes[0], gene_index, mutated_genes_indices[0] ),
                        check_mutation( board_state, genes[1], gene_index, mutated_genes_indices[1] ) 
                    ]
                    
                    random.shuffle( mutated_genes ) # shuffle genes
                    baby_chromosome_one[ 'genes' ][ board_state ] = mutated_genes[ 0 ]
                    baby_chromosome_two[ 'genes' ][ board_state ] = mutated_genes[ 1 ]

                offspring.append( baby_chromosome_one )
                offspring.append( baby_chromosome_two )

        self.previous_population = copy_population( self.population )
        self.population = self.fittest_chromosomes + offspring  

    def compete( self, chromosome_one, chromosome_two ):

        lambda_chromosome_one = lambda board_state, _: chromosome_one[ 'genes' ][ board_state ] 
        lambda_chromosome_two = lambda board_state, _: chromosome_two[ 'genes' ][ board_state ] 
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

            genes = ast.literal_eval( line ) # parse string dictionary
            new_chromosome = {'genes': genes, 'score': 0}
            self.population.append( new_chromosome )

        self.number_of_genes = len( genes )
        self.original_population = copy_population( self.population ) # create a copy of population for original population

def hard_cutoff( population, breedable_population_size ):
    population.sort( key = lambda chromosome: chromosome[ 'score' ], reverse = True )
    return population[ : breedable_population_size ]

def stochastic( population, breedable_population_size ): 
    fittest_chromosomes = []
    
    while len( fittest_chromosomes ) < breedable_population_size:
        
        heat = random.sample( population, math.floor( breedable_population_size / 2 ) )
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
        
        heat = random.sample( population, math.floor( breedable_population_size / 2 ) )

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

def check_mutation( board_state, gene, gene_index, mutated_genes ):
    return get_random_move( board_state ) if gene_index in mutated_genes else gene

def get_valid_move( board_state ):
    return [ i for i in range( 9 ) if board_state[ i ] in [ '0', 0 ] ]

def get_random_move( board_state ):
    return random.choices( get_valid_move( board_state ) )[0]

def copy_population( population ):
    return list( population )
    
def get_mutated_chromosomes( number_of_genes, mutation_rate ):
    number_of_mutated_genes = math.ceil( number_of_genes * mutation_rate )
    chromosome_one_mutated_genes = random.sample( range( number_of_genes ), number_of_mutated_genes )
    chromosome_two_mutated_genes = random.sample( range( number_of_genes ), number_of_mutated_genes )
    return [ chromosome_one_mutated_genes, chromosome_two_mutated_genes ]
