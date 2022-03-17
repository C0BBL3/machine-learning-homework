import filecmp
from numpy import random
import time

random.seed(int(time.time()))
board_states = [line.strip('\n') for line in open('011/board_states.txt', 'r').readlines()]
ttc_chromosome_genes_file = open('011/ttc_chromosome_genes.txt', 'w')

for _ in range(40):

    genes = {}

    for board_state in board_states:


        if board_state.count('0') == 0: continue

        move = random.choice([j for j in range(9) if int(board_state[j]) == 0])
        genes[board_state] = move
        
    string_genes = '{' + ''.join(['"' + str(board_state) + '": ' + str(move) + ', ' for board_state, move in genes.items()]) + '}\n'
    ttc_chromosome_genes_file.write(str(string_genes))