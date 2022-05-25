from numpy import random
import math
import time
import multiprocessing
import matplotlib.pyplot as plt
from metaheuristic_algorithm import nn_chromosome
from tic_tac_toe import Game

def random_function( board_state, current_player ):
    return random.choice( [ 
        i 
        for i in range( 9 ) 
        if int( board_state[ i ] ) == 0 
    ] )

def calculate_score( fittest_chromosomes, population, num_games, return_int, lock, time ):

        result = int()
        random.seed(time)

        fittest_chromosome_indices =  random.randint(
            len( fittest_chromosomes ), 
            size = num_games 
        )

        population_indices = random.randint(
            len( population ), 
            size = num_games 
        )

        temp = 0
        for i in range( num_games ):
            
            chromosome_one = fittest_chromosomes[ fittest_chromosome_indices[ i ] ]
            chromosome_two = population[ population_indices[ i ] ]

            args = [ nn_chromosome( chromosome_one ), nn_chromosome( chromosome_two ) ]

            game = Game( *args )
            if game.play()[ 1 ] == 1: 
                result += 1
                temp += 1

            game = Game( *args[ : : -1 ] )
            if game.play()[ 1 ] == 2: 
                result += 1
            else:
                temp -= 1

        lock.acquire()

        print(temp)
        return_int.value += result / ( 2 * num_games )

        lock.release()
            
def calculate_score_random( fittest_chromosomes, random_function, num_games, return_int, lock, time ):

    result = int()
    random.seed(time)

    fittest_chromosome_indices =  random.randint(
        len( fittest_chromosomes ), 
        size = num_games
    )

    temp = 0
    for i in range( num_games ):

        chromosome_one = fittest_chromosomes[ fittest_chromosome_indices[ i ] ]

        args = [ nn_chromosome( chromosome_one ), random_function ]

        game = Game( *args )
        if game.play()[ 1 ] == 1: 
            result += 1
            temp += 1

        game = Game( *args[ : : -1 ] )
        if game.play()[ 1 ] == 2: 
            result += 1
        else:
            temp -= 1

    lock.acquire()

    return_int.value += result / ( 2 * num_games )
    print(temp)

    lock.release()

def plot_win_loss_tie( MHA, plotted_generation_num, random_average_score, original_average_score, previous_average_score ):

    # stoopid thing to make cleaner code
    random_original_previous_iter = {
        'random': ( 
            random_average_score, 
            calculate_score_random, 
            random_function 
        ), 
        'original': ( 
            original_average_score, 
            calculate_score, 
            MHA.original_population[ : len( MHA.fittest_chromosomes ) ] 
        ), 
        'previous': ( 
            previous_average_score, 
            calculate_score, 
            MHA.previous_population[ : len( MHA.fittest_chromosomes ) ] 
        ) 
    }

    return_dict = {
        'random': multiprocessing.Manager().Value( 'd', 0 ), # d for 'double' (double precision float)
        'original': multiprocessing.Manager().Value( 'd', 0 ),
        'previous': multiprocessing.Manager().Value( 'd', 0 )
    }
    
    workers = list()
    lock = multiprocessing.Lock()

    for i, (name, ( _, function, enemys ) ) in enumerate(random_original_previous_iter.items()): # cringe

        worker_group = list()

        available_thread_count = math.floor(
            ( multiprocessing.cpu_count() - 1 ) / 3
        )

        num_of_matchups_per_core = math.floor( 
            50 / available_thread_count
        )
        
        for j in range( 0, available_thread_count ):
            
            args = [ 
                MHA.fittest_chromosomes, 
                enemys, 
                num_of_matchups_per_core, 
                return_dict[ name ],
                lock,
                int(time.time() + 100*j*math.sin(i) + 350*i*math.cos(j*j) + 100*j + 4500*i) # random expression cause random is cringe
            ]

            worker = multiprocessing.Process( 
                target = function, 
                args = args
            )

            worker.start()
            worker_group.append( worker )
        
        workers.append( worker_group )

    for worker_group in workers:
        for worker in worker_group:
            worker.join()

    for name, ( plot, _, _ ) in random_original_previous_iter.items():
        print( return_dict[ name ].value / 5 )
        plot.append( return_dict[ name ].value / 5 )
    
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), random_average_score )
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), original_average_score )
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), previous_average_score )
    plt.legend( [ 'Random', 'Original', 'Previous' ] )
    plt.savefig( 'images/012-3-1.png' )
    plt.clf()

def plot_state_value( MHA, plotted_generation_num, win_prediction_score, lose_prediction_score, tie_prediction_score ):

    file_path = 'metaheuristic_algorithm/ttt_board_states'

    files = {
        result: open( file_path + '/' + result + '_board_states.txt', 'r' )
        for result in [ 'winning', 'losing', 'tieing' ]
    }

    board_states = {
        result: [ line.strip( '\n' ) for line in files[ result ] ]
        for result in [ 'winning', 'losing', 'tieing' ]
    }

    win_predictions = int() 
    num_win_predictions = len( board_states[ 'winning' ] ) * len( MHA.fittest_chromosomes ) 

    lose_predictions = int()
    num_lose_predictions = len( board_states[ 'losing' ] ) * len( MHA.fittest_chromosomes )

    tie_predictions = int()
    num_tie_predictions = len( board_states[ 'losing' ] ) * len( MHA.fittest_chromosomes )

    for chromosome in MHA.fittest_chromosomes:

        for board_state in board_states[ 'winning' ]:

            temp = [int(space) for space in board_state]
            win_predictions += chromosome['genes'].calc_prediction(
                {
                    'input': temp
                }
            )
                        
        for board_state in board_states[ 'losing' ]:

            temp = [int(space) for space in board_state]
            lose_predictions += chromosome['genes'].calc_prediction(
                {
                    'input': temp
                }
            )

        for board_state in board_states[ 'losing' ]:

            temp = [int(space) for space in board_state]
            tie_predictions += chromosome['genes'].calc_prediction(
                {
                    'input': temp
                }
            )

    win_prediction_score.append( win_predictions / num_win_predictions )
    lose_prediction_score.append( lose_predictions / num_lose_predictions )
    tie_prediction_score.append( tie_predictions / num_tie_predictions )

    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), win_prediction_score )
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), lose_prediction_score )
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), tie_prediction_score )

    plt.legend( [ 'Win', 'Lose', 'Tie' ] )
    plt.savefig( 'images/012-3-2.png' )
    plt.clf()

def plot_strategy_effectiveness( MHA, plotted_generation_num, win_capture_score, loss_prevention_score ):

    winnable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/winnable_board_states.txt', 'r' ).readlines() ]
    losable_board_states = [ line.strip( '\n' ) for line in open( 'metaheuristic_algorithm/ttt_board_states/losable_board_states.txt', 'r' ).readlines() ]

    will_win_score = int()
    can_win_score = len( winnable_board_states ) * len( MHA.fittest_chromosomes )

    will_block_score = int()
    can_block_score = len( losable_board_states ) * len( MHA.fittest_chromosomes )

    for board_state in winnable_board_states:

        temp = [int(space) for space in board_state]

        win_capture = plots_3_and_4( temp, 1 ) # win capture

        for chromosome in MHA.fittest_chromosomes:

            current_move = nn_chromosome( chromosome )( temp, 1 )
            
            if current_move in win_capture[ 1 ]:
                
                will_win_score += 1
        
    for board_state in losable_board_states:

        temp = [int(space) for space in board_state]

        loss_prevention = plots_3_and_4(temp, 2) # loss prevention

        for chromosome in MHA.fittest_chromosomes:
                
            current_move = nn_chromosome( chromosome )( temp, 1 )
            
            if current_move in loss_prevention[ 1 ]:
                
                will_block_score -= 1

    win_capture_score.append( will_win_score / can_win_score )
    loss_prevention_score.append( will_block_score / can_block_score )

    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), win_capture_score )
    plt.plot( list( range( 1, plotted_generation_num + 2 ) ), loss_prevention_score )
    plt.legend( [ 'Win Rate', 'Lose Rate' ] )
    plt.savefig( 'images/012-3-3.png' )
    plt.clf()