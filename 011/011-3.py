from numpy import random
import matplotlib.pyplot as plt
from tic_tac_toe import Game, plots_3_and_4
from genetic_algorithm import GeneticAlgorithm

def calculate_score(fittest_cells, population):

    for cell_one in fittest_cells:

        for cell_two in population:

            GA.compete(cell_one, cell_two)
            cell_two['score'] = 0

            GA.compete(cell_two, cell_one)
            cell_two['score'] = 0

    score = []

    for cell in fittest_cells:
        score.append(cell['score'] / len(fittest_cells))
        cell['score'] = 0

    return sum(score)

original_average_score = []
previous_average_score = []
win_capture_score = []
loss_prevention_score = [] # | || || |_

num_generations = 100

board_states = [line.strip('\n') for line in open('011/board_states.txt', 'r').readlines()]
ttc_cell_chromosomes = [line.strip('\n') for line in open('011/ttc_cell_chromosomes.txt', 'r').readlines()]

GA = GeneticAlgorithm()
GA.read_cells(ttc_cell_chromosomes)

for generation in range(num_generations):
    
    if generation < 5 or generation % 10 == 9: 
        print('\nGeneration:', generation + 1)

    GA.determine_fitness(fittest_cells_size=25, random_selection_size=20)
    GA.breed()

    original_average_score.append(calculate_score(GA.fittest_cells, GA.original_population))
    previous_average_score.append(calculate_score(GA.fittest_cells, GA.previous_population))

    can_win_score = 0
    can_block_score = 0
    will_win_score = 0
    will_block_score = 0

    for cell in GA.fittest_cells:
        for board_state in cell['chromosomes'].keys():
            list_board_state = [int(space) for space in board_state]
            win_capture = plots_3_and_4(list_board_state, 1) # win capture
            if win_capture[0]:
                can_win_score += 1
                if cell['chromosomes'][board_state] in win_capture[1]:
                    will_win_score += 1
            loss_prevention = plots_3_and_4(list_board_state, 2) # loss prevention
            if loss_prevention[0]:
                can_block_score += 1
                if cell['chromosomes'][board_state] in loss_prevention[1]:
                    will_block_score += 1 

    win_capture_score.append(will_win_score / can_win_score)
    loss_prevention_score.append(will_block_score / can_block_score)

plt.plot(list(range(num_generations)), original_average_score)
plt.plot(list(range(num_generations)), previous_average_score)
plt.legend(['Original', 'Previous'])
plt.savefig('images/011-3-1.png')

plt.clf()

plt.plot(list(range(num_generations)), win_capture_score)
plt.plot(list(range(num_generations)), loss_prevention_score)
plt.legend(['Win Capture', 'Loss Prevention'])
plt.savefig('images/011-3-2.png')
