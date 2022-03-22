from numpy import random
import numpy as np
import time
import ast
import math
from tic_tac_toe import Game

class GeneticAlgorithm:
    def __init__( self ):
        self.population = list()

    def determine_fitness( self, fitness_score = 'round robin' ):

        self.fittest_chromosomes = list()

        if fitness_score == 'round robin': # n ^ 2 matchups more accurate

            matchups = self.determine_matchups( fitness_score )

            for ( i, j ) in matchups: 
                
                self.compete( self.population[ i ], self.population[ j ] )
            
        elif fitness_score == 'bracket': # n/2 + n/4 + n/8 = 7n/8 total matchups less accurate but faster

            round_population = self.population # initial population
            matchups = self.determine_matchups( fitness_score, round_population )
            round_ = 1

            while matchups is not []:

                for ( i, j ) in matchups: 

                    result = self.compete( self.population[ i ], self.population[ j ] )
                    
                    if result[1] is False:
                        _ = self.compete( self.population[ j ], self.population[ i ] ) # reverse matchup and if its still a draw these two dont move on

                round_population = [ chromosome for chromosome in round_population if chromosome[ 'score' ] == round_ ]
                matchups = self.determine_matchups( fitness_score, round_population )
                round_ += 1

        self.population.sort( key = lambda chromosome: chromosome[ 'score' ], reverse = True )
        self.fittest_chromosomes = self.population[ : self.breedable_population_size ]

    def determine_matchups(self, fitness_score, current_bracket = None):

        matchups = list()

        if fitness_score == 'round robin':

            for i in range( self.population_size ):

                for j in range( self.population_size ):

                    if i != j and [ i, j ] not in matchups:

                        matchups.append( [ i, j ] )

            return matchups

        elif fitness_score == 'bracket':

            if current_bracket is None: current_bracket = copy_population( self.population )

            for i in range( 0,  len( current_bracket ) - 1, 2 ):

                matchups.append( [ i, i + 1 ] )

            return matchups


    def breed( self, mutation_rate = 0.001 ):

        number_of_mutated_genes = int( 1 / mutation_rate ) if mutation_rate != 0 else 0
        offspring = list()

        for i, chromosome_one in enumerate( self.fittest_chromosomes ):

            chromosome_one_mutated_genes = random.randint( self.number_of_genes, size = number_of_mutated_genes ).tolist()

            for chromosome_two in self.fittest_chromosomes[ i + 1 : ]:

                chromosome_two_mutated_genes = random.randint( self.number_of_genes, size = number_of_mutated_genes ).tolist()
                temp = [ chromosome_one_mutated_genes, chromosome_two_mutated_genes ] # for iterating over

                baby_chromosome_one = {'genes': {}, 'score': 0}
                baby_chromosome_two = {'genes': {}, 'score': 0}
                
                for gene_index, board_state in enumerate( chromosome_one[ 'genes' ].keys() ):

                    genes = [ chromosome_one[ 'genes' ][ board_state ], chromosome_two[ 'genes' ][ board_state ] ]
                    mutated_genes = [ check_mutation( board_state, gene, gene_index, mutated_genes ) for gene, mutated_genes in zip( genes, temp ) ]
                    random.shuffle( mutated_genes ) # shuffle genes
                    baby_chromosome_one[ 'genes' ][ board_state ] = mutated_genes[ 0 ]
                    baby_chromosome_two[ 'genes' ][ board_state ] = mutated_genes[ 1 ]

                offspring.append( baby_chromosome_one )
                offspring.append( baby_chromosome_two )

        self.previous_population = copy_population( self.population )
        self.population = self.fittest_chromosomes + offspring  

    def compete( self, chromosome_one, chromosome_two ):

        game = Game( chromosome_one[ 'genes' ], chromosome_two[ 'genes' ] )
        result = game.play()

        if result[ 1 ] == 1: # chromosome 1 won
            chromosome_one[ 'score' ] += 1
            chromosome_two[ 'score' ] -= 1
        elif result[ 1 ] == 2: # chromosome 2 won
            chromosome_one[ 'score' ] -= 1
            chromosome_two[ 'score' ] += 1  

        return result

    def read_chromosomes( self, ttc_chromosome_genes_file, population_size = 64 ): # the ttc_chromosome_genes_file is a readlines() file
        
        random.shuffle( ttc_chromosome_genes_file )

        self.population_size = int( 2 ** ( math.floor( math.log( population_size, 2 ) ) ) ) # what the fuck
        self.breedable_population_size = int( math.sqrt( self.population_size ) )

        for line in ttc_chromosome_genes_file[ : self.population_size ]:

            genes = ast.literal_eval( line ) # parse string dictionary
            new_chromosome = {'genes': genes, 'score': 0}
            self.population.append( new_chromosome )

        self.number_of_genes = len( genes )
        self.original_population = copy_population( self.population ) # create a copy of population for original population

def check_mutation( board_state, gene, gene_index, mutated_genes ):
    return get_random_move( board_state ) if gene_index in mutated_genes else gene

def get_valid_move( board_state ):
    return [ i for i in range( 9 ) if board_state[ i ] in [ '0', 0 ] ]

def get_random_move( board_state ):
    return random.choice( get_valid_move( board_state ) )

def copy_population( population ):
    return list( population )
    
        
