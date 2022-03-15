from numpy import random
import numpy as np
from tic_tac_toe import Game
import time
import ast


class GeneticAlgorithm:
    def __init__(self, board_states):
        self.board_states = board_states
        self.population = []

    def read_cells(self, ttc_cell_chromosomes_file): # the ttc_cell_chromosomes_file is a readlines() file
        
        for line in ttc_cell_chromosomes_file:

            chromosomes = ast.literal_eval(line)
            new_cell = {'chromosomes': chromosomes, 'score': 0}
            self.population.append(new_cell)
            self.original_population = self.copy_population(self.population)


    def determine_fitness(self, fittest_cells_size = 5, random_selection_size = 3):

        self.fittest_cells = []

        while len(self.fittest_cells) < fittest_cells_size:

            past_matchups = []
            current_heat = self.heat_selection(self.population, random_selection_size = random_selection_size)

            for i, cell_one in enumerate(current_heat):

                for j, cell_two in enumerate(current_heat):

                    if i != j and [i, j] not in past_matchups:
                        
                        past_matchups.append([i, j])
                        self.compete(cell_one, cell_two)
            
            fittest_cell = max(current_heat, key = lambda cell: cell['score'])
            
            for cell in current_heat: cell['score'] = 0

            self.fittest_cells.append(fittest_cell)
            self.population.pop(self.population.index(fittest_cell))
            current_heat.pop(current_heat.index(fittest_cell))

    def compete(self, cell_one, cell_two):

        game = Game(cell_one['chromosomes'], cell_two['chromosomes'])
        result = game.play()

        if result[1] == 1: # cell 1 won
            cell_one['score'] += 1
            cell_two['score'] -= 1
        elif result[1] == 2: # cell 2 won
            cell_one['score'] -= 1
            cell_two['score'] += 1  

    def breed(self):

        #self.population.sorted(key = lambda cell: cell['score'], reverse = True)
        #self.fittest_cells = self.copy_population(self.population[:5])
        offspring = []

        for i, cell_one in enumerate(self.fittest_cells):

            for cell_two in self.fittest_cells[i + 1:]:
        
                baby_cell_one = {'chromosomes': {}, 'score': 0}
                baby_cell_two = {'chromosomes': {}, 'score': 0}

                for key in cell_one['chromosomes'].keys():

                    values = [cell_one['chromosomes'][key], cell_two['chromosomes'][key]]
                    random.shuffle(values)
                    baby_cell_one['chromosomes'][key] = values[0]
                    baby_cell_two['chromosomes'][key] = values[1]

                offspring.append(baby_cell_one)
                offspring.append(baby_cell_two)

        self.previous_population = self.copy_population(self.population)
        self.population = self.fittest_cells + offspring  

    @staticmethod
    def copy_population(population):
        return list(population)

    @staticmethod
    def get_random_move(board_state):
        return random.choice([j for j in range(9) if board_state[j] == 0])

    @staticmethod
    def heat_selection(population, random_selection_size = 3):
        random.shuffle(population)
        return population[:random_selection_size]
        
        
