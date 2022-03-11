from numpy import random
import math
from tic_tac_toe import Game

def generate_strategy(num_of_branches = 3, depth = 0, max_depth = 9, strategy = {}, strings = [{'board':[0 for _ in range(9)], 'space': None}]): # depth is also turn number

    if depth == max_depth: return strategy

    player = (depth % 2) + 1
    
    new_strings = build_new_strings(strings, player, num_of_branches)

    random.shuffle(new_strings)
        
    for string in new_strings:
    
        temp = string['board'][:string['space']] + [0] + string['board'][string['space'] + 1:]
        state = ''.join([str(item) for item in temp])

        if state in strategy.keys(): continue
        
        strategy[state] = string['space']

    random.shuffle(new_strings)
    return generate_strategy(num_of_branches, depth = depth + 1, strategy = strategy, strings = new_strings[:num_of_branches])

    # strategy = {}
    
    # for _ in range(100):

    #     string = [0 for _ in range(9)]

    #     for i in range(9):

    #         player = (i % 2) + 1
    #         choices = [i for i in range(9) if string[i] == 0]
    #         space = random.choice(choices)
    #         strategy[''.join([str(item) for item in string])] = space
    #         string[space] = player
            
    # return strategy

def build_new_strings(strings, player, num_of_branches):

    new_strings = []
    
    for string in strings:

        for i in range(num_of_branches):
                            
            choices = [j for j in range(9) if string['board'][j] == 0]
            space = random.choice(choices)
            temp = string['board'][:space] + [player] + string['board'][space + 1:]
            new_strings.append({'board': temp, 'space': space})

    return new_strings

def fight(i, strategy_one, strategy_two, count_score = True):
    game = Game(strategy_one['strategy'], strategy_two['strategy'])
    result = game.play()
    strategy_one['strategy'], strategy_two['strategy'] = result[1][0], result[1][1]

    if not count_score: return strategy_one, strategy_two
    
    if result[0][1] != 'Draw':

        if result[0][1] == 1: # player 1

            strategy_one['score'] += 1
            strategy_two['score'] -= 1

        elif result[0][1] == 2: # player 2

            strategy_one['score'] -= 1
            strategy_two['score'] += 1
        
    # else: # draw

    #     strategy_one['score'] += 1
    #     strategy_two['score'] -= 1            

    return strategy_one, strategy_two

def breed(strategy_one, strategy_two):
    baby_strategy = {'strategy': {}, 'score': 0}

    for (key_1, value_1), (key_2, value_2) in zip(strategy_one['strategy'].items(), strategy_two['strategy'].items()):
        
        if key_1 != key_2:

            baby_strategy['strategy'][key_1] = value_1
            baby_strategy['strategy'][key_2] = value_2

        else:

            baby_strategy['strategy'][key_1] = random.choice([value_1, value_2])

    return baby_strategy

def calculate_score(best_five, strategies):

    for i, strategy_one in enumerate(best_five[:5]):

        for strategy_two in strategies[:5]:

            best_five[i], _ = fight(i, strategy_one, strategy_two, False)

    return sum([strategy['score'] / len(best_five) for strategy in best_five])

strategies = []
original_average_score = []
previous_average_score = []

for i in range(25):
    random.seed(i)
    new_strategy = generate_strategy(num_of_branches=9)
    strategies.append({'strategy': new_strategy, 'score': 0})
    del new_strategy

original_strategies = [strategy for strategy in strategies]
previous_strategies = [strategy for strategy in strategies]

for generation in range(1, 101):

    if generation < 6 or generation % 10 == 0: print('\nGeneration:', generation)

    for i, strategy_one in enumerate(strategies):

        for j, strategy_two in enumerate(strategies[:i] + strategies[i + 1:]):

            strategies[i], strategies[j] = fight(i, strategy_one, strategy_two)

    strategies.sort(key = lambda strategy: strategy['score'], reverse = True)
    print("bad", strategies.count(strategies[-1]))
    best_five = [strategy for strategy in strategies[:5]]

    for strategy in best_five: strategy['score'] = 0

    previous_average_score.append(calculate_score(best_five, previous_strategies))
    original_average_score.append(calculate_score(best_five, original_strategies))
    new_strategies = [strategy for strategy in strategies]

    for i, strategy_one in enumerate(best_five):

        for strategy_two in best_five[:i] + best_five[i + 1:5]:

            new_strategy = breed(strategy_one, strategy_two)
            new_strategies.append(new_strategy)

    previous_strategies = [strategy for strategy in strategies]
    strategies = best_five
    del best_five

import matplotlib.pyplot as plt

plt.plot(list(range(100)), previous_average_score)
plt.plot(list(range(100)), original_average_score)
plt.legend(['Original', 'Previous'])
plt.savefig('images/011-1.png')

print("\nTraining Complete")

print("\nBest Strategy\n\n", strategies[0]['strategy'], "\n\n")