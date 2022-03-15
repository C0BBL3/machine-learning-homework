from numpy import random
import matplotlib.pyplot as plt
from tic_tac_toe import Game
from genetic_algorithm import GeneticAlgorithm

board_states = open('011/board_states.txt', 'r').readlines()

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

GA = GeneticAlgorithm(board_states)

for generation in range(num_generations):
    
    if generation < 5 or generation % 10 == 9: 
        print('\nGeneration:', generation + 1)

    GA.determine_fitness()
    GA.breed()

    original_average_score.append(calculate_score(GA.fittest_cells, GA.original_population))
    previous_average_score.append(calculate_score(GA.fittest_cells, GA.previous_population))


plt.plot(list(range(num_generations)), original_average_score)
plt.plot(list(range(num_generations)), previous_average_score)
plt.legend(['Original', 'Previous'])
plt.savefig('images/011-3.png')
