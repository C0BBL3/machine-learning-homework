import filecmp
from numpy import random
import time

random.seed(int(time.time()))
board_states = [line.strip('\n') for line in open('011/board_states.txt', 'r').readlines()]
ttc_cell_chromosomes_file = open('011/ttc_cell_chromosomes.txt', 'w')

for _ in range(400):

    chromosomes = {}

    for board_state in board_states:

        list_board_state = [int(space) for space in board_state]

        if list_board_state.count(0) == 0: continue

        move = random.choice([j for j in range(9) if list_board_state[j] == 0])
        chromosomes[board_state] = move
        
    string_chromosomes = '{' + ''.join(['"' + str(board_state) + '": ' + str(move) + ', ' for board_state, move in chromosomes.items()]) + '}\n'
    ttc_cell_chromosomes_file.write(str(string_chromosomes))