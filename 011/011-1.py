import random
from tic_tac_toe import Game

def generate_strategy(seed):
    random.seed(seed)
    strategy = {}

    for _ in range(25):

        string = [0 for _ in range(9)]

        for i in range(9):

            player = (i % 2) + 1
            choices = [i for i in range(9) if string[i] == 0]
            space = random.choices(choices)[0]
            strategy[''.join([str(item) for item in string])] = space
            string[space] = player
            
    return strategy

def fight(i, strategy_one, strategy_two):
    random.seed(i)
    game = Game(strategy_one['strategy'], strategy_two['strategy'])
    result = game.play()
    strategy_one['strategy'], strategy_two['strategy'] = result[1][0], result[1][1]

    if result[0][1] != 'Draw':

        if result[0][1] == 1:

            strategy_one['score'] += 1
            strategy_two['score'] -= 1

        elif result[0][1] == 2:

            strategy_one['score'] -= 1
            strategy_two['score'] += 1

    return strategy_one, strategy_two

def breed(strategy_one, strategy_two):
    baby_strategy = {'strategy': {}, 'score': 0}

    for (key_1, value_1), (key_2, value_2) in zip(strategy_one['strategy'].items(), strategy_two['strategy'].items()):
        
        if key_1 != key_2:

            baby_strategy['strategy'][key_1] = value_1
            baby_strategy['strategy'][key_2] = value_2

        else:

            baby_strategy['strategy'][key_1] = random.choices([value_1, value_2])[0]

    return baby_strategy

strategies = []
average_score = []

for i in range(25):
    strategies.append({'strategy': generate_strategy(i), 'score': 0})

previous_strategies = [strategy for strategy in strategies]

for generation in range(1, 101):

    if generation < 6 or generation % 10 == 0: print('\nGeneration:', generation)

    for i, strategy_one in enumerate(strategies):

        for j, strategy_two in enumerate(strategies[:i] + strategies[i + 1:]):

            strategies[i], strategies[j] = fight(i, strategy_one, strategy_two)

    strategies.sort(key = lambda strategy: strategy['score'], reverse = True)
    temp_1 = strategies[:5]
    previous_strategies = [strategy for strategy in strategies]
    del strategies

    for strategy in temp_1: strategy['score'] = 0

    for i, strategy_one in enumerate(temp_1):

        for strategy_two in previous_strategies:

            temp_1[i], _ = fight(i, strategy_one, strategy_two)

    average_score.append(sum([strategy['score'] / len(temp_1) for strategy in temp_1]) )
    temp_2 = []

    for strategy in temp_1: strategy['score'] = 0

    for i, strategy_one in enumerate(temp_1):

        for strategy_two in temp_1[:i] + temp_1[i + 1:]:

            new_strategy = breed(strategy_one, strategy_two)
            temp_2.append(new_strategy)

    strategies = temp_2
    

import matplotlib.pyplot as plt

plt.plot(list(range(100)), average_score)
plt.savefig('images/011-1.png')

print("\nTraining Complete")

print("\nBest Strategy\n\n", strategies[0], "\n\n")