import filecmp
from tic_tac_toe import Game, plots_3_and_4

game = Game( None, None )

def detect_tie( board ):

    if board.count( 0 ) == 0:

        return True

    elif board.count( 0 ) >= 1:

        return False

    else:

        if board.count( 1 ) > board.count( 2 ):
            current_player = 2
        else:
            current_player = 1
        
        possible_branches = game.get_possible_branches(board, current_player)

        for branch in possible_branches:

            if evaluate_board( branch )[ 0 ] and branch.count( 0 ) > 0:

                return False

        return True

def validate_board( board ):

    if board.count( 1 ) > board.count( 2 ) + 1: 
        return False
    elif board.count( 2 ) > board.count( 1 ) + 1:
        return False
    else:
        return True

def evaluate_board( board ):
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

    if detect_tie( board ): 
        return (False, 'Tie')

    return (False, None)

def generate_board_states():
    board_states = list()
    winnable_board_states = list()
    losable_board_states = list() # should be inverse of winnable
    winning_board_states = list()
    losing_board_states = list() # should be inverse of winning
    tieing_board_states = list()

    for a in [0, 1, 2]: # 
        for b in [0, 1, 2]:
            for c in [0, 1, 2]:
                for d in [0, 1, 2]:
                    for e in [0, 1, 2]: # 
                        for f in [0, 1, 2]:
                            for g in [0, 1, 2]:
                                for h in [0, 1, 2]:
                                    for i in [0, 1, 2]:

                                        board = [ a, b, c, d, e, f, g, h, i ]

                                        board_validation = validate_board( board )

                                        if not board_validation: continue

                                        board_evaluation = evaluate_board( board )

                                        if not board_evaluation[0] and board_evaluation[1] != 'Tie': 

                                            board_states.append( board )
                                        
                                        elif board_evaluation[ 0 ] and board_evaluation[ 1 ] == 1:

                                            winning_board_states.append( board )

                                        elif board_evaluation[ 0 ] and board_evaluation[ 1 ] == 2:

                                            losing_board_states.append( board )

                                        elif board_evaluation[ 1 ] == 'Tie':

                                            tieing_board_states.append( board )

                                        win = plots_3_and_4(board, 1)

                                        if win[ 0 ] and not board_evaluation[ 0 ]:
                                            winnable_board_states.append( board )

                                        loss = plots_3_and_4(board, 2)

                                        if loss[ 0 ] and not board_evaluation[ 0 ]:
                                            losable_board_states.append( board )

    return board_states, winnable_board_states, losable_board_states, winning_board_states, losing_board_states, tieing_board_states

board_states, winnable_board_states, losable_board_states, winning_board_states, losing_board_states, tieing_board_states = generate_board_states()

board_states_file = open('metaheuristic_algorithm/ttt_board_states/board_states.txt', 'w')

for board_state in board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    board_states_file.write(string_board_state)

winnable_board_states_file = open('metaheuristic_algorithm/ttt_board_states/winnable_board_states.txt', 'w')

for board_state in winnable_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    winnable_board_states_file.write(string_board_state)

losable_board_states_file = open('metaheuristic_algorithm/ttt_board_states/losable_board_states.txt', 'w')

for board_state in losable_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    losable_board_states_file.write(string_board_state)


winning_board_states_file = open('metaheuristic_algorithm/ttt_board_states/winning_board_states.txt', 'w')

for board_state in winning_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    winning_board_states_file.write(string_board_state)

losing_board_states_file = open('metaheuristic_algorithm/ttt_board_states/losing_board_states.txt', 'w')

for board_state in losing_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    losing_board_states_file.write(string_board_state)


tieing_board_states_file = open('metaheuristic_algorithm/ttt_board_states/tieing_board_states.txt', 'w')

for board_state in tieing_board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    tieing_board_states_file.write(string_board_state)
