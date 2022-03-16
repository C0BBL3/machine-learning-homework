from numpy import random
import numpy as np
from tic_tac_toe import Game
import time
import ast


class GeneticAlgorithm:
    def __init__(self, board_states):
        self.board_states = board_states
        self.population = []

    def determine_fitness(self, fittest_chromosomes_size = 5, random_selection_size = 3):

        self.fittest_chromosomes = []

        while len(self.fittest_chromosomes) < fittest_chromosomes_size:

            past_matchups = []
            current_heat = heat_selection(self.population, random_selection_size = random_selection_size)

            for i, chromosome_one in enumerate(current_heat):

                for j, chromosome_two in enumerate(current_heat):

                    if i != j and [i, j] not in past_matchups:
                        
                        past_matchups.append([i, j])
                        self.compete(chromosome_one, chromosome_two)
            
            fittest_chromosome = max(current_heat, key = lambda chromosome: chromosome['score'])
            
            for chromosome in current_heat: chromosome['score'] = 0

            self.fittest_chromosomes.append(fittest_chromosome)
            self.population.pop(self.population.index(fittest_chromosome))
            current_heat.pop(current_heat.index(fittest_chromosome))

    def breed(self, mutation_rate = 0.01):

        offspring = []

        for i, chromosome_one in enumerate(self.fittest_chromosomes):

            for chromosome_two in self.fittest_chromosomes[i + 1:]:
        
                baby_chromosome_one = {'genes': {}, 'score': 0}
                baby_chromosome_two = {'genes': {}, 'score': 0}

                for key in chromosome_one['genes'].keys():

                    genes = [chromosome_one['genes'][key], chromosome_two['genes'][key]]
                    mutated_genes = [check_mutation(key, gene, mutation_rate = mutation_rate) for gene in genes]
                    random.shuffle(mutated_genes) # shuffle genes
                    baby_chromosome_one['genes'][key] = mutated_genes[0]
                    baby_chromosome_two['genes'][key] = mutated_genes[1]

                offspring.append(baby_chromosome_one)
                offspring.append(baby_chromosome_two)

        self.previous_population = copy_population(self.population)
        self.population = self.fittest_chromosomes + offspring  

    def compete(self, chromosome_one, chromosome_two):

        game = Game(chromosome_one['genes'], chromosome_two['genes'])
        result = game.play()

        if result[1] == 1: # chromosome 1 won
            chromosome_one['score'] += 1
            chromosome_two['score'] -= 1
        elif result[1] == 2: # chromosome 2 won
            chromosome_one['score'] -= 1
            chromosome_two['score'] += 1  

    def read_chromosomes(self, ttc_chromosome_genes_file): # the ttc_chromosome_genes_file is a readlines() file
        
        for line in ttc_chromosome_genes_file:

            genes = ast.literal_eval(line) # parse string dictionary
            new_chromosome = {'genes': genes, 'score': 0}
            self.population.append(new_chromosome)
        
        self.original_population = copy_population(self.population) # create a copy of population for original population

def check_mutation(board_state, gene, mutation_rate = 0.01):
    return random.choice([get_random_move(board_state), gene], p = [mutation_rate, 1 - mutation_rate])

def copy_population(population):
    return list(population)

def get_random_move(board_state):
    return random.choice([j for j in range(9) if int(board_state[j]) == 0])

def heat_selection(population, random_selection_size = 3):
    random.shuffle(population)
    return population[:random_selection_size]
    
        
