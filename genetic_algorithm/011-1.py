from numpy import random
from tic_tac_toe import Game
import time
import matplotlib.pyplot as plt
import filecmp

all_possible_board_states = open('genetic_algorithm/board_states.txt', 'r').readlines()

def get_random_move(board_state):
    return random.choice([j for j in range(9) if board_state[j] == 0])

def generate_strategy(all_possible_board_states):

    strategy = {}

    for board_state in all_possible_board_states:

        list_board_state = [int(space) for space in board_state[:-1]]

        if list_board_state.count(0) == 0: continue

        move = get_random_move(list_board_state)
        strategy[board_state[:-1]] = move

    return strategy

def fight(strategy_one, strategy_two, count_score = True):
    lambda_strategy_one = lambda board_state: strategy_one['strategy'][board_state]
    lambda_strategy_two = lambda board_state: strategy_two['strategy'][board_state]
    game = Game(lambda_strategy_one, lambda_strategy_two)
    result = game.play()
    if not count_score: return strategy_one, strategy_two
    
    if result[1] != 'Draw':

        if result[1] == 1: # player 1

            strategy_one['score'] += 1
            strategy_two['score'] -= 1

        elif result[1] == 2: # player 2

            strategy_one['score'] -= 1
            strategy_two['score'] += 1         

    return strategy_one, strategy_two

def breed(strategy_one, strategy_two):
    baby_strategy_one = {'strategy': {}, 'score': 0}
    baby_strategy_two = {'strategy': {}, 'score': 0}

    for key in strategy_one['strategy'].keys():

        values = [strategy_one['strategy'][key], strategy_two['strategy'][key]]
        random.shuffle(values)

        baby_strategy_one['strategy'][key] = values[0]
        baby_strategy_two['strategy'][key] = values[1]

    return baby_strategy_one, baby_strategy_two

def calculate_score(best_five, population):

    for i, strategy_one in enumerate(best_five):

        for strategy_two in population:

            best_five[i], _ = fight(strategy_one, strategy_two)
            _, best_five[i] = fight(strategy_two, strategy_one)

    return sum([strategy['score'] / len(best_five) for strategy in best_five])

def plots_3_and_4(board_state, player):

    moves = []

    #horizontal
    if board_state[1] == board_state[2] == player and board_state[0] == 0: moves.append(0)
    if board_state[0] == board_state[2] == player and board_state[1] == 0: moves.append(1)
    if board_state[0] == board_state[1] == player and board_state[2] == 0: moves.append(2)

    if board_state[4] == board_state[5] == player and board_state[3] == 0: moves.append(3)
    if board_state[3] == board_state[5] == player and board_state[4] == 0: moves.append(4)
    if board_state[3] == board_state[4] == player and board_state[5] == 0: moves.append(5)

    if board_state[7] == board_state[8] == player and board_state[6] == 0: moves.append(6)
    if board_state[6] == board_state[8] == player and board_state[7] == 0: moves.append(7)
    if board_state[6] == board_state[7] == player and board_state[8] == 0: moves.append(8)

    #vertical
    if board_state[3] == board_state[6] == player and board_state[0] == 0: moves.append(0)
    if board_state[4] == board_state[7] == player and board_state[1] == 0: moves.append(1)
    if board_state[5] == board_state[8] == player and board_state[1] == 0: moves.append(2)

    if board_state[0] == board_state[6] == player and board_state[0] == 0: moves.append(3)
    if board_state[1] == board_state[7] == player and board_state[1] == 0: moves.append(4)
    if board_state[2] == board_state[8] == player and board_state[1] == 0: moves.append(5)

    if board_state[0] == board_state[3] == player and board_state[0] == 0: moves.append(6)
    if board_state[1] == board_state[4] == player and board_state[1] == 0: moves.append(7)
    if board_state[2] == board_state[5] == player and board_state[1] == 0: moves.append(8)

    #diagonal
    if board_state[4] == board_state[8] == player and board_state[0] == 0: moves.append(0)
    if board_state[0] == board_state[8] == player and board_state[4] == 0: moves.append(4)
    if board_state[0] == board_state[4] == player and board_state[8] == 0: moves.append(8)

    #backwards diagonal
    if board_state[4] == board_state[6] == player and board_state[2] == 0: moves.append(2)
    if board_state[2] == board_state[6] == player and board_state[4] == 0: moves.append(4)
    if board_state[2] == board_state[4] == player and board_state[6] == 0: moves.append(6)

    return len(moves) > 0, moves
    

population = []

random.seed(int(time.time()))
for i in range(25):
    strategy = generate_strategy(all_possible_board_states)
    population.append({'strategy': strategy, 'score': 0})

original_average_score = []
previous_average_score = []
win_capture_score = []
loss_prevention_score = [] # | || || |_

original_population = [{key: value for key, value in strategy.items()} for strategy in population]
previous_population = [{key: value for key, value in strategy.items()} for strategy in population]

num_generations = 100

for generation in range(1, num_generations + 1):

    if generation < 6 or generation % 10 == 0: print('\nGeneration:', generation)

    for i, strategy_one in enumerate(population):

        for j, strategy_two in enumerate(population[i + 1:]):

            strategy_one, strategy_two = fight(strategy_one, strategy_two)

    population.sort(key = lambda strategy: strategy['score'], reverse = True)
    best_five = [strategy for strategy in population[:5]]

    for strategy in best_five: strategy['score'] = 0

    previous_population_score = calculate_score(best_five, previous_population)

    for strategy in previous_population: strategy['score'] = 0
    for strategy in best_five: strategy['score'] = 0

    original_population_score = calculate_score(best_five, original_population)

    for strategy in original_population: strategy['score'] = 0
    for strategy in best_five: strategy['score'] = 0

    previous_average_score.append(previous_population_score)
    original_average_score.append(original_population_score)

    can_win_score = 0
    can_block_score = 0
    will_win_score = 0
    will_block_score = 0

    for strategy in best_five:
        for board_state in strategy['strategy']:
            temp = [int(space) for space in board_state]
            win_capture = plots_3_and_4(temp, 1) # win capture
            if win_capture[0]:
                can_win_score += 1
                if strategy['strategy'][board_state] in win_capture[1]:
                    will_win_score += 1
            loss_prevention = plots_3_and_4(temp, 2) # loss prevention
            if loss_prevention[0]:
                can_block_score += 1
                if strategy['strategy'][board_state] in loss_prevention[1]:
                    will_block_score += 1 

    win_capture_score.append(will_win_score / can_win_score)
    loss_prevention_score.append(will_block_score / can_block_score)

    new_population = [strategy for strategy in best_five]

    for i, strategy_one in enumerate(best_five):

        for j, strategy_two in enumerate(best_five[i + 1:]):

            baby_strategy_one, baby_strategy_two = breed(strategy_one, strategy_two)
            new_population.append(baby_strategy_one)
            new_population.append(baby_strategy_two)

    previous_population = [strategy for strategy in population]
    population = new_population
    del best_five

plt.plot(list(range(num_generations)), original_average_score)
plt.plot(list(range(num_generations)), previous_average_score)
plt.legend(['Original', 'Previous'])
plt.savefig('images/011-1-1.png')

plt.clf()

plt.plot(list(range(num_generations)), win_capture_score)
plt.plot(list(range(num_generations)), loss_prevention_score)
plt.legend(['Win Capture', 'Loss Prevention'])
plt.savefig('images/011-1-2.png')

print("\nTraining Complete")

print("\nBest Strategy\n\n", population[0]['strategy'], "\n\n")
