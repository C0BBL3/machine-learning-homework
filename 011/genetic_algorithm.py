from numpy import random
from tic_tac_toe import Game
import time
import filecmp


class GeneticAlgorithm:
    def __init__(self, aboard_states, total_amount = 25):
        self.board_states = board_states
        self.population = []
        self.generate_population(total_amount)
        self.original_population = self.copy_population(self.population)
        

    def generate_population(self, total_amount = 25):

        random.seed(int(time.time()))

        for i in range(total_amount):
            
            chromosomes = generate_random_chromosomes() # strategy for cell
            cell = {'chromosomes': chromosomes, 'score': 0} # individual strategy
            self.population.append(cell)
    
    def generate_random_chromosomes(self):

        chromosomes = {}

        for board_state in self.board_states:

            board_state = board_state[:-1] # remove the \n

            list_board_state = [int(space) for space in board_state]

            if list_board_state.count(0) == 0: continue

            move = self.get_random_move(list_board_state)
            chromosomes[board_state] = move

        return chromosomes

    def determine_fitness(self):

        for i, cell_one in enumerate(self.population):

            for cell_two in self.population[:i] + self.population[i + 1:]:

                self.fight(cell_one, cell_two)  

        self.population.sort(key = lambda cell: cell['score'], reverse = True)

    def fight(self, cell_one, cell_two):

        game = Game(cell_one['chromosomes'], cell_two['chromosomes'])
        result = game.play()

        if result[1] == 1: # cell 1 won
            cell_one['score'] += 1
            cell_two['score'] -= 1
        elif result[1] == 2: # cell 2 won
            cell_one['score'] -= 1
            cell_two['score'] += 1  

    def breed(self):

        self.fittest_cells = self.find_fittest_cells(self.population)
        self.offspring = []

        for i, cell_one in enumerate(self.fittest_cells):

            for cell_two in self.fittest_cells[i + 1:]:
        
                baby_cell_one = {'chromosomes': {}, 'score': 0}
                baby_cell_two = {'chromosomes': {}, 'score': 0}

                for key in cell_one['chromosomes'].keys():

                    values = [cell_one['chromosomes'][key], cell_two['chromosomes'][key]]
                    random.shuffle(values)
                    baby_cell_one['chromosomes'][key] = values[0]
                    baby_cell_two['chromosomes'][key] = values[1]

                self.offspring.append(baby_cell_one)
                self.offspring.append(baby_cell_two)

        self.previous_population = self.copy_population(self.population)
        self.population = self.fittest_cells + self.offspring  

    @staticmethod
    def copy_population(population):
        return [{'chromosomes': cell['chromosomes'], 'score': 0} for cell in population] # array of cells w/o scores, [{'00000000': 1, '000000001': 3, ...}, {'00000000': 4, '000000001': 2, ...}, ...]

    @staticmethod
    def get_random_move(board_state):
        return random.choice([j for j in range(9) if board_state[j] == 0])

    @staticmethod
    def find_fittest_cells(population, total_amount = 5, random_selection_size = 3):
        
        fittest_cells = []

        while len(fittest_cells) < total_amount:
            
            random.shuffle(population)
            random_selection = population[:random_selection_size]
            fittest_cell = max(random_selection, key=lambda cell: cell['score'])
            fittest_cell_index = population.index(fittest_cell)
            population.pop(fittest_cell_index)
            fittest_cells.append(fittest_cell)

        return fittest_cells
        
