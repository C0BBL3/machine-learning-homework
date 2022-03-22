class Game:
    def __init__(self, strategy_one, strategy_two):
        self.board = [0 for _ in range(9)]

        if isinstance(strategy_one, list): 
            strategy_one = strategy_one[0]

        if isinstance(strategy_two, list): 
            strategy_two = strategy_two[0]

        self.strategies = [strategy_one, strategy_two]

    def play(self):

        current_player = 0
        new_possible_moves = [{}, {}]
        
        while not self.game_finished()[0] and self.board.count(0) > 0:

            current_state = self.state(current_player)
            current_move = self.strategies[current_player][current_state]
            self.place(current_player, current_move)
            
            current_player = 1 if current_player == 0 else 0

        winner = self.game_finished()

        if winner[1] == None: return (False, "Draw")

        return winner
        
    def place(self, player, index): # 1 or 2 for player, and index is 0-9
        try:
            if self.board[index] == 0: 
                self.board[index] = player + 1
            else: 
                raise ValueError
        except ValueError as va:
            print("Player", player, "tried to cheat by placing a piece on space", player)
            print("Board state", self.state())
            exit()

    def state(self, current_player = 1):
        switcher = { 0: 0, 1: 1, 2: 2 }
        if current_player == 2: 
            switcher = { 0: 0, 1: 2, 2: 1 }
        return ''.join([str(switcher[space]) for space in self.board])

    def game_finished(self):

        # horizontal
        if self.board[0] == self.board[1] == self.board[2] != 0: 
            return (True, self.board[0]) 
        if self.board[3] == self.board[4] == self.board[5] != 0: 
            return (True, self.board[3])
        if self.board[6] == self.board[7] == self.board[8] != 0: 
            return (True, self.board[6])

        # vertical
        if self.board[0] == self.board[3] == self.board[6] != 0: 
            return (True, self.board[0])
        if self.board[1] == self.board[4] == self.board[7] != 0: 
            return (True, self.board[1])
        if self.board[2] == self.board[5] == self.board[8] != 0: 
            return (True, self.board[2])

        # diagonal
        if self.board[0] == self.board[4] == self.board[8] != 0: 
            return (True, self.board[0]) 
        
        # backwards diagonal
        if self.board[2] == self.board[4] == self.board[6] != 0: 
            return (True, self.board[2]) 

        if self.board.count(0) == 0:
            return (False, None)

        return (False, None)

def plots_3_and_4(board_state, player):

    moves = []

    #horizontal
    if board_state[1] == board_state[2] == player and board_state[0] == 0: 
        moves.append(0)
    if board_state[0] == board_state[2] == player and board_state[1] == 0: 
        moves.append(1)
    if board_state[0] == board_state[1] == player and board_state[2] == 0: 
        moves.append(2)

    if board_state[4] == board_state[5] == player and board_state[3] == 0: 
        moves.append(3)
    if board_state[3] == board_state[5] == player and board_state[4] == 0: 
        moves.append(4)
    if board_state[3] == board_state[4] == player and board_state[5] == 0: 
        moves.append(5)

    if board_state[7] == board_state[8] == player and board_state[6] == 0: 
        moves.append(6)
    if board_state[6] == board_state[8] == player and board_state[7] == 0: 
        moves.append(7)
    if board_state[6] == board_state[7] == player and board_state[8] == 0: 
        moves.append(8)

    #vertical
    if board_state[3] == board_state[6] == player and board_state[0] == 0: 
        moves.append(0)
    if board_state[4] == board_state[7] == player and board_state[1] == 0: 
        moves.append(1)
    if board_state[5] == board_state[8] == player and board_state[1] == 0: 
        moves.append(2)

    if board_state[0] == board_state[6] == player and board_state[0] == 0: 
        moves.append(3)
    if board_state[1] == board_state[7] == player and board_state[1] == 0: 
        moves.append(4)
    if board_state[2] == board_state[8] == player and board_state[1] == 0: 
        moves.append(5)

    if board_state[0] == board_state[3] == player and board_state[0] == 0: 
        moves.append(6)
    if board_state[1] == board_state[4] == player and board_state[1] == 0: 
        moves.append(7)
    if board_state[2] == board_state[5] == player and board_state[1] == 0: 
        moves.append(8)

    #diagonal
    if board_state[4] == board_state[8] == player and board_state[0] == 0: 
        moves.append(0)
    if board_state[0] == board_state[8] == player and board_state[4] == 0: 
        moves.append(4)
    if board_state[0] == board_state[4] == player and board_state[8] == 0: 
        moves.append(8)

    #backwards diagonal
    if board_state[4] == board_state[6] == player and board_state[2] == 0: 
        moves.append(2)
    if board_state[2] == board_state[6] == player and board_state[4] == 0: 
        moves.append(4)
    if board_state[2] == board_state[4] == player and board_state[6] == 0: 
        moves.append(6)

    return len(moves) > 0, moves