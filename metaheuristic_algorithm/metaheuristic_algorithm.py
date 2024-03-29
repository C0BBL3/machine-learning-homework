from minimax import Minimax
from neural_network import NeuralNetwork
from numpy import random
import numpy as np
import time
import ast
import math
import multiprocessing
from tic_tac_toe import Game
import sys
sys.path.append('neural_network/')
sys.path.pop()
sys.path.append('min_max_algorithm/')


class MetaHeuristicAlgorithm:
    def __init__(self):
        self.population = list()

    def pre_train_state(self, iterations=50, board_states_path='ttt_board_states', print_progress=False):

        file_path = 'metaheuristic_algorithm/' + board_states_path

        files = {
            result: open(file_path + '/' + result + '_board_states.txt', 'r')
            for result in ['winning', 'losing', 'tieing']
        }

        board_states = {
            result: [line.strip('\n') for line in files[result]]
            for result in ['winning', 'losing', 'tieing']
        }

        results = {
            'winning': 1,
            'losing': 0,
            'tieing': -1
        }

        # score will be rss for each chromosome

        for generation in range(iterations):

            if print_progress and (generation < 5 or generation % 5 == 4):

                print('\n\tPre-Evolving Generation: {}...'.format(generation + 1))

            for chromosome in self.population:

                for result, board_states_list in board_states.items():

                    for board_state in board_states_list:

                        temp = [
                            float(space)
                            for space in board_state
                        ]

                        chromosome['score'] += (results[result] - chromosome['genes'].calc_prediction(
                            {
                                'input': temp
                            }
                        )) ** 2

            self.population = sorted(
                copy_population(self.population),
                key=lambda chromosome: chromosome['score'],
                reverse=True
            )[: len(self.population) // 2]

            self.population += [
                {
                    'genes': chromosome['genes'].mitosis(),
                    'score': 0
                }
                for chromosome in self.population
            ]

            if print_progress and (generation < 5 or generation % 5 == 4):
                print(
                    '\n\tGeneration: {} Pre-Evolution Completed!'.format(generation + 1))

    def determine_fitness(self, fitness_score='round robin', cutoff_type='hard cutoff', current_bracket=None, round_number=1, breedable_population_size=int()):

        self.fitness_score = fitness_score
        self.cutoff_type = cutoff_type
        self.fittest_chromosomes = list()

        if current_bracket is None:
            current_bracket = self.population

        self.current_bracket = current_bracket
        workers = dict()
        available_thread_count = multiprocessing.cpu_count() - 1
        lock = multiprocessing.Lock()

        matchups = self.determine_matchups()

        random.shuffle(matchups)

        num_of_matchups_per_core = math.floor(
            len(matchups) /
            available_thread_count
        )

        return_list = {
            i: multiprocessing.Manager().Value('i', 0)
            for i in range(len(self.current_bracket))
        }

        for i in range(0, len(matchups), num_of_matchups_per_core):

            matchups_arg = matchups[i: num_of_matchups_per_core + i]
            args = [
                fitness_score,
                matchups_arg,
                return_list,
                lock
            ]

            worker = multiprocessing.Process(
                target=self.multi_core_compete,
                args=args
            )

            worker.start()
            workers[i] = worker

        for worker in workers.values():
            worker.join()

        for i, worker_return in enumerate(return_list.values()):

            self.current_bracket[i]['score'] = int(worker_return.value)

        if fitness_score == 'bracket' and len(matchups) > 1:

            next_round_population = list()

            for chromosome in current_bracket:
                if chromosome['score'] == round_number:
                    next_round_population.append(chromosome)

            self.determine_fitness(
                fitness_score=fitness_score,
                current_bracket=next_round_population,
                round_number=round_number + 1
            )

        if cutoff_type == 'stochastic':
            cutoff_function = stochastic
        elif cutoff_type == 'tournament':
            cutoff_function = tournament
        else:
            cutoff_function = hard_cutoff

        self.fittest_chromosomes = cutoff_function(
            self.population,
            self.breedable_population_size
        )

    def breed(self, mutation_rate=0.001, crossover_type='random', crossover_genes_indices=list()):

        offspring = list()

        # evolutionary breeding (one parent producing one offspring)
        if crossover_type == 'evolutionary':

            for chromosome in self.fittest_chromosomes:

                child = {
                    'genes': chromosome['genes'].mitosis(),
                    'score': int()
                }

                while child in offspring or child in self.population:

                    child = {
                        'genes': chromosome['genes'].mitosis(),
                        'score': int()
                    }

                offspring.append(child)

        else:  # genetic breeding (two parents producing two offspring)

            for i, chromosome_one in enumerate(self.fittest_chromosomes):

                for chromosome_two in self.fittest_chromosomes[i + 1:]:

                    crossover_genes_indices = get_crossover_indices(
                        self.number_of_genes,
                        mutation_rate,
                        crossover_type,
                        crossover_genes_indices
                    )

                    mutated_genes_indices = get_mutated_chromosomes(
                        self.number_of_genes,
                        mutation_rate
                    )

                    baby_chromosome_one = dict()
                    baby_chromosome_two = dict()

                    edges = chromosome_one['genes'].weights.keys()

                    for edge_index, edge in enumerate(edges):

                        gene = [
                            chromosome_one['genes'].weights[edge],
                            chromosome_two['genes'].weights[edge]
                        ]

                        gene = [
                            check_mutation(
                                gene[0], edge, mutated_genes_indices[0]),
                            check_mutation(
                                gene[1], edge, mutated_genes_indices[1])
                        ]

                        if edge_index in crossover_genes_indices:

                            gene = gene[:: -1]

                        baby_chromosome_one[edge] = gene[0]
                        baby_chromosome_two[edge] = gene[1]

                    baby_chromosome_one = {
                        'genes': NeuralNetwork(baby_chromosome_one),
                        'score': 0
                    }

                    baby_chromosome_two = {
                        'genes': NeuralNetwork(baby_chromosome_two),
                        'score': 0
                    }

                    offspring.append(baby_chromosome_one)
                    offspring.append(baby_chromosome_two)

        self.previous_population = copy_population(self.population)
        self.population = copy_population(self.fittest_chromosomes + offspring)

    def compete(self, chromosome_one, chromosome_two):

        game = Game(
            nn_chromosome(chromosome_one),
            nn_chromosome(chromosome_two)
        )

        result = game.play()

        if result[1] == 1:  # chromosome 1 won
            chromosome_one['score'] += 1
            chromosome_two['score'] -= 1
        elif result[1] == 2:  # chromosome 2 won
            chromosome_one['score'] -= 1
            chromosome_two['score'] += 1

        return result

    def multi_core_compete(self, fitness_score, matchups, return_dict, lock):  # nasty

        for (i, j) in matchups:

            result = self.compete(
                self.population[i],
                self.population[j]
            )

            if fitness_score == 'bracket':

                if result[0] is False or result[1] == 'Draw':
                    self.compete(
                        self.population[j],
                        self.population[i]
                    )  # reverse matchup and if its still a draw these two dont move on

        lock.acquire()

        for (i, j) in matchups:

            return_dict[i].value += self.population[i]['score']
            return_dict[j].value += self.population[j]['score']

        lock.release()

    # the ttc_chromosome_genes_file is a readlines() file
    def read_chromosomes(self, generate_weights_function, layer_sizes, layers_with_bias_nodes, population_size=64, breedable_population_size=None, input_size=list(), random_bool=True, random_range=[-1.0, 1.0]):

        if breedable_population_size is None:

            self.breedable_population_size = math.floor(
                math.sqrt(
                    population_size
                )
            )

        else:

            self.breedable_population_size = breedable_population_size

        self.population_size = population_size
        input_size_int = input_size[0] * input_size[1]
        bias_shift = layers_with_bias_nodes.count(True)

        activation_functions = [
            lambda x: x
            for _ in range(input_size_int)
        ] + [
            lambda x: math.tanh(x)
            for _ in range(sum(layer_sizes) + bias_shift)
        ]

        bias_node_indices = [
            9 + sum(layer_sizes[0: i]) + i - 1
            for i in range(1, len(layer_sizes))
        ]

        for bias_node_index in bias_node_indices:
            activation_functions[bias_node_index] = lambda x: x

        for _ in range(self.population_size):

            genes = generate_weights_function(
                layer_sizes,
                random_bool=random_bool,
                random_range=random_range,
                layers_with_bias_nodes=layers_with_bias_nodes,
                input_size=input_size
            )

            new_chromosome = {
                'genes': NeuralNetwork(
                    genes,  # weights
                    functions=activation_functions,
                    alpha=0.01
                ),
                'score': 0
            }

            self.population.append(new_chromosome)

        self.number_of_genes = len(genes)
        # create a copy of population for original population
        self.original_population = copy_population(self.population)

    def determine_matchups(self):

        matchups = list()

        if self.fitness_score == 'round robin':

            for i in range(len(self.current_bracket)):

                for j in range(len(self.current_bracket)):

                    if i != j and [i, j] not in matchups:

                        matchups.append([i, j])

        elif self.fitness_score == 'bracket':

            for i in range(0,  len(self.current_bracket) - 1, 2):

                matchups.append([i, i + 1])

        elif self.fitness_score == 'blondie24':

            for i in range(len(self.current_bracket)):

                for _ in range(5):

                    j = random.choice(list(range(len(self.current_bracket))))

                    while [i, j] in matchups and [j, i] in matchups:

                        # re-roll j so we dont have two of the same games
                        # with the same players (order doesnt matter)

                        j = random.choice(
                            list(range(len(self.current_bracket))))

                    matchups.append([i, j])

        return matchups


def nn_chromosome(chromosome):

    def evaluation_function(board_state, current_player): return chromosome['genes'].calc_prediction(
        {
            'input': [
                {0: 0, 1: -1, 2: 1}[space]  # double checking if
                if current_player == 2 else   # board state  is in
                {0: 0, 1: 1, 2: -1}[space]  # current player format
                for space in board_state
            ]
        }
    )

    return lambda board_state, current_player: minimax_function(
        board_state,
        evaluation_function,
        current_player
    )


def minimax_function(board_state, evaluation_function, current_player):
    minimax = Minimax()

    minimax.generate_tree(
        Game(None, None, current_player=current_player),
        current_player,
        root_board_state=board_state,
        max_depth=5
    )

    minimax.evaluate_game_tree(
        Game(None, None),
        evaluation_function
    )

    return minimax.get_best_move(board_state)


def get_crossover_indices(number_of_genes, mutation_rate, crossover_type='random', crossover_genes_indices=list()):

    if crossover_type == 'random':

        # random indices for crossover
        crossover_genes_indices = random.choice(
            range(number_of_genes),
            round(number_of_genes * mutation_rate),
            replace=False
        )

    else:

        half_of_number_of_genes = math.ceil(number_of_genes / 2)
        first_half_of_genes_indices = list(range(half_of_number_of_genes))

        if crossover_type == 'alternating':

            # every even is crossovered
            crossover_genes_indices = list(map(
                lambda x: 2 * x,
                first_half_of_genes_indices
            ))

        elif crossover_type == 'fiftyfifty':

            # first half is crossovered
            crossover_genes_indices = first_half_of_genes_indices

    return crossover_genes_indices


def hard_cutoff(population, breedable_population_size, key=lambda chromosome: chromosome['score']):

    population.sort(
        key=key,
        reverse=True
    )

    return population[: breedable_population_size]


def stochastic(population, breedable_population_size):

    fittest_chromosomes = []

    while len(fittest_chromosomes) < breedable_population_size:

        heat = random.choice(
            population,
            math.floor(
                breedable_population_size / 2
            ),
            replace=False
        )
        fittest_chromosome = max(
            heat,
            key=lambda chromosome: chromosome['score']
        )
        fittest_chromosomes.append(fittest_chromosome)
        fittest_chromosome_index = population.index(fittest_chromosome)
        population.pop(fittest_chromosome_index)

    return fittest_chromosomes


def tournament(population, breedable_population_size):

    fittest_chromosomes = []

    for chromosome in population:
        chromosome['score'] = 0

    while len(fittest_chromosomes) < breedable_population_size:

        heat = random.choice(
            population,
            math.floor(breedable_population_size / 2),
            replace=False
        )

        for i, chromosome_one in enumerate(heat):

            for j, chromosome_two in enumerate(heat):

                if i != j:

                    game = Game(
                        chromosome_one['genes'],
                        chromosome_two['genes']
                    )
                    result = game.play()

                    if result[1] == 1:  # chromosome 1 won
                        chromosome_one['score'] += 1
                        chromosome_two['score'] -= 1

                    elif result[1] == 2:  # chromosome 2 won
                        chromosome_one['score'] -= 1
                        chromosome_two['score'] += 1

        fittest_chromosome = max(
            heat,
            key=lambda chromosome: chromosome['score']
        )
        fittest_chromosomes.append(fittest_chromosome)
        fittest_chromosome_index = population.index(fittest_chromosome)
        population.pop(fittest_chromosome_index)

        for chromosome in heat:
            chromosome['score'] = 0

    return fittest_chromosomes


def check_mutation(gene, gene_index, mutated_genes):
    return calculate_mutation() if gene_index in mutated_genes else gene


def calculate_mutation():
    gaussian_random_numbers = np.random.normal(0, 1, 1000)
    np.random.shuffle(
        gaussian_random_numbers
    )
    return gaussian_random_numbers[0]


def copy_population(population):

    copy_population_list = list()

    for chromosome in population:

        copy_chromosome = {
            'genes': NeuralNetwork(
                weights=dict(chromosome['genes'].weights),
                functions=list(chromosome['genes'].functions),
                alpha=float(chromosome['genes'].alpha)
            ),
            'score': int()
        }

        copy_population_list.append(copy_chromosome)

    return copy_population_list


def get_mutated_chromosomes(number_of_genes, mutation_rate):

    number_of_mutated_genes = math.ceil(
        number_of_genes * mutation_rate
    )
    chromosome_one_mutated_genes = random.choice(
        range(number_of_genes),
        number_of_mutated_genes,
        replace=False)
    chromosome_two_mutated_genes = random.choice(
        range(number_of_genes),
        number_of_mutated_genes,
        replace=False)
    return [
        chromosome_one_mutated_genes,
        chromosome_two_mutated_genes
    ]
