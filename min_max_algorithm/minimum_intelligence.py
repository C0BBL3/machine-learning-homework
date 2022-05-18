from minimax import Minimax
import time
import sys
sys.path.append('metaheuristic_algorithm/')
from tic_tac_toe import Game

minimax = Minimax()

def minimax_function( board_state, current_player ):
    minimax = Minimax()

    if current_player == 2:
        switcher = { 0: 0, 1: 2, 2: 1 }
        board_state = [ switcher[ space ] for space in board_state ]
        #current_player = 1

    minimax.generate_tree(
        Game( None, None, current_player = current_player ), 
        current_player, 
        root_board_state = board_state, 
        max_depth = 9
    )

    minimax.evaluate_game_tree(
        Game( None, None ), 
        game_1.evaluate
    )
    
    return ( minimax.get_best_move( board_state ), minimax )

def stoopid( board_state, current_player ):
    return board_state.index( 0 )

game_1 = Game( minimax_function, stoopid )

while not game_1.game_finished()[ 0 ] and game_1.board.count( 0 ) > 0:

    current_state = game_1.state( current_player = game_1.current_player )
    current_move = game_1.strategies[ game_1.current_player - 1 ]( game_1.board, game_1.current_player )
    if game_1.current_player == 1:
        game_1.place( game_1.current_player, current_move[ 0 ] )
    else:
        game_1.place( game_1.current_player, current_move )
    game_1.current_player = game_1.get_next_player( game_1.current_player )
    if isinstance(current_move, tuple):
        game_1.logs.append( 
            (
                game_1.state(), [
                    [
                        node.board_state, 
                        node.value
                    ] 
                    for node in current_move[ 1 ].first_layer_nodes
                ]
            )
        )
    else:
        game_1.logs.append(game_1.state())

print(game_1.logs)

game_2 = Game( stoopid, minimax_function )

while not game_2.game_finished()[ 0 ] and game_2.board.count( 0 ) > 0:

    current_state = game_2.state( current_player = game_2.current_player )
    temp = game_2.state()
    current_move = game_2.strategies[ game_2.current_player - 1 ]( game_2.board, game_2.current_player )
    if game_2.current_player == 2:
        game_2.place( game_2.current_player, current_move[ 0 ] )
    else:
        game_2.place( game_2.current_player, current_move )
    game_2.current_player = game_2.get_next_player( game_2.current_player )
    if isinstance(current_move, tuple):
        game_2.logs.append(
            (
                temp, [
                    [
                        node.board_state, 
                        node.value
                    ] 
                    for node in current_move[ 1 ].first_layer_nodes
                ]
            )
        )
    else:
        game_2.logs.append(game_2.state())

print(game_2.logs)