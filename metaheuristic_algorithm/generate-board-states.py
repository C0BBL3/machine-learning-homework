import filecmp
from tic_tac_toe import plots_3_and_4

def evaluate_board(board):
    # horizontal
    if board[0] == board[1] == board[2] != 0: 
        return (True, board[0]) 
    if board[3] == board[4] == board[5] != 0: 
        return (True, board[3])
    if board[6] == board[7] == board[8] != 0: 
        return (True, board[6])
    # vertical
    if board[0] == board[3] == board[6] != 0: 
        return (True, board[0])
    if board[1] == board[4] == board[7] != 0: 
        return (True, board[1])
    if board[2] == board[5] == board[8] != 0: 
        return (True, board[2])
    # diagonal
    if board[0] == board[4] == board[8] != 0: 
        return (True, board[0]) 
    # backwards diagonal
    if board[2] == board[4] == board[6] != 0: 
        return (True, board[2]) 

    if board.count(0) == 0: 
        return (False, None)

    return (False, None)

def generate_board_states():
    board_states = list()
    winnable_board_states = list()
    losable_board_states = list() # should be reverse of winnable

    for a in [0, 1, 2]: # 
        for b in [0, 1, 2]:
            for c in [0, 1, 2]:
                for d in [0, 1, 2]:
                    for e in [0, 1, 2]: # 
                        for f in [0, 1, 2]:
                            for g in [0, 1, 2]:
                                for h in [0, 1, 2]:
                                    for i in [0, 1, 2]:

                                        board = [a, b, c, d, e, f, g, h, i]

                                        if evaluate_board(board)[0]: continue

                                        board_states.append( board )

                                        win = plots_3_and_4(board, 1)

                                        if win[ 0 ]:
                                            winnable_board_states.append( board )

                                        loss = plots_3_and_4(board, 2)

                                        if loss[ 0 ]:
                                            losable_board_states.append( board )

    return board_states, winnable_board_states, losable_board_states

board_states, winnable_board_states, losable_board_states = generate_board_states()

board_states_file = open('metaheuristic_algorithm/board_states.txt', 'w')

for board_state in board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    board_states_file.write(string_board_state)

winnable_board_states_file = open('metaheuristic_algorithm/winnable_board_states.txt', 'w')

for board_state in winnable_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    winnable_board_states_file.write(string_board_state)

losable_board_states_file = open('metaheuristic_algorithm/losable_board_states.txt', 'w')

for board_state in losable_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    losable_board_states_file.write(string_board_state)
