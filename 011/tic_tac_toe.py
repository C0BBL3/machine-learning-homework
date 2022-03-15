from numpy import random

class Game:
    def __init__(self, strategy_one, strategy_two):
        self.board = [0 for _ in range(9)]

        if isinstance(strategy_one, list): strategy_one = strategy_one[0]

        if isinstance(strategy_two, list): strategy_two = strategy_two[0]

        self.strategies = [strategy_one, strategy_two]

    def play(self):
        current_player = 0
        new_possible_moves = [{}, {}]
        while not self.game_finished()[0] and self.board.count(0) > 0:
            current_state = self.state(current_player)
            if current_state in self.strategies[current_player].keys():
                current_move = self.strategies[current_player][current_state]
            else:
                current_move = random.choice([i for i in range(9) if self.board[i] == 0]) # random open spot if key bad
                new_possible_moves[current_player][current_state] = current_move
            self.place(current_player, current_move)
            
            current_player = 1 if current_player == 0 else 0

        winner = self.game_finished()

        if winner[0]:
            self.strategies[winner[1] - 1] = {**self.strategies[winner[1] - 1], **new_possible_moves[winner[1] - 1]}

        if winner[1] == None and self.board.count(0) == 0:
            #print("\tDraw")
            #print("\tBoard State", self.state())

            return (False, "Draw")

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

    def state(self, current_player):
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