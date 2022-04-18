import filecmp

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
    temp = []
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
                                        temp.append(board)
    return temp

board_states = generate_board_states()

board_states_file = open('metaheuristic_algorithm/board_states.txt', 'w')

for board_state in board_states:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    board_states_file.write(string_board_state)
