class Game:
    def __init__(self, strategy_one, strategy_two):
        self.board = [0 for _ in range(9)]
        if isinstance(strategy_one, list): strategy_one = strategy_one[0]
        if isinstance(strategy_two, list): strategy_two = strategy_two[0]

        self.strategies = [strategy_one, strategy_two]

    def play(self):
        current_player = 0
        while not self.game_finished()[0] and self.board.count(0) > 0:
            current_state = self.state()
            if current_state in self.strategies[current_player].keys():
                current_move = self.strategies[current_player][current_state]
            else:
                for i, space in enumerate(self.board):
                    if space == 0:
                        current_move = i
                        self.strategies[current_player][current_state] = current_move
                        break
            self.place(current_player, current_move)
            if current_player == 0: 
                current_player = 1
                continue
            else:
                current_player = 0
                continue

        winner = self.game_finished()

        if winner[1] == None and self.board.count(0) == 0:
            #print("\tDraw")
            #print("\tBoard State", self.state())

            return (False, "Draw", winner[2])

        #print("\tPlayer", winner[1], "Wins")
        #print("\tBoard State", self.state())

        return winner
        
    def place(self, player, index): # 1 or 2 for player, and index is 0-9
        try:
            if self.board[index] == 0: self.board[index] = player + 1
            else: raise ValueError
        except ValueError as va:
            print("Player", player, "tried to cheat by placing a piece on space", index)
            print("Board state", self.state())
            exit()

    def state(self):
        return ''.join([str(space) for space in self.board])

    def game_finished(self):
        for index, space in enumerate(self.board):
            horizontal = index in [0,3,6] and self.board[index] != 0 and self.board[index + 1] == space and self.board[index + 2] == space
            vertical = index in [0,1,2] and self.board[index] != 0 and self.board[index + 3] == space and self.board[index + 6] == space
            forward_diagonal = self.board[index] != 0 and index == 0 and self.board[index + 4] == space and self.board[index + 8] == space
            backward_diagonal = self.board[index] != 0 and index == 2 and self.board[index + 2] == space and self.board[index + 4] == space
            if [horizontal, vertical, forward_diagonal, backward_diagonal].count(True) > 0:
                return (True, space, [horizontal, vertical, forward_diagonal, backward_diagonal])
        return (False, None, None)