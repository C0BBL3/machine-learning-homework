from numpy import random
from minimax import Minimax
import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game


new_possible_moves = {}

order = 0

def print_board(board):
    print('\nCurrent Board\n')
    for i in range(3):
        print('\t' + ''.join([str(space) + ' | ' if j < 2 else str(space) for j, space in enumerate(board[3 * i:3 * (i + 1)])]))
        if i < 2:
            print('\t---------')

game = Game(None, None)

for game in range(5):

    print('\nGame:', game + 1)

    board = [i for i in range(9)]

    try:

        for turn in range(9):

            if turn != 0: print_board(board)

            if (turn % 2) == order:

                current_state = ''

                minimax = Minimax()
                minimax.generate_tree(game, turn % 2, root_node = board, prune = True, max_depth = 3)
                minimax.evaluate_game_tree(game)
                minimax.get_best_move(board)

                if isinstance(board[current_move], int): board[current_move] = 'O'
                
                print('\nThe Minimax strategy placed an O on space', current_move)

            else:

                print('\nWhat is your next move?\n')
                current_move = input()
                
                if current_move == '': 
                    choices = [i for i in board if isinstance(i, int)]
                    current_move = random.choice(choices)
                else:
                    current_move = int(current_move)
                
                if isinstance(board[current_move], int): board[current_move] = 'X'
                print('\nYou placed an X on space', current_move)

            # horizontal
            if board[0] == board[1] == board[2] != 0: 
                horizontal = True
                space = board[0] 
            if board[3] == board[4] == board[5] != 0: 
                horizontal = True
                space = board[3] 
            if board[6] == board[7] == board[8] != 0: 
                horizontal = True
                space = board[6] 
            # vertical
            if board[0] == board[3] == board[6] != 0: 
                vertical = True
                space = board[0] 
            if board[1] == board[4] == board[7] != 0: 
                vertical = True
                space = board[1] 
            if board[2] == board[5] == board[8] != 0: 
                vertical = True
                space = board[2] 
            # diagonal
            if board[0] == board[4] == board[8] != 0: 
                diagonal = True
                space = board[0] 
            # backwards diagonal
            if board[2] == board[4] == board[6] != 0: 
                backward_diagonal = True
                space = board[2] 
                
            if [horizontal, vertical, forward_diagonal, backward_diagonal].count(True) > 0:
                if space == 'O':
                    print('\nThe Best Strategy Won!')
                    for state, move in new_possible_moves.items():
                        best_strategy[state] = move
                    print_board(board)
                    order = 0
                elif space == 'X':
                    print('\nYou won!')
                    print_board(board)
                    order = 1
                    best_strategy[current_state] = current_move
                raise Exception('win')

        raise Exception('draw')

    except Exception as exc:
        if exc.args[0] == 'draw':
            print('\nGame Finished: Draw')
            best_strategy[current_state] = current_move
            for state, move in new_possible_moves.items():
                best_strategy[state] = move
            print_board(board)
        continue

print("\n\nNew Strategy\n\n", best_strategy)
    

