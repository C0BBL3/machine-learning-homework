from numpy import random

class Game:
    def __init__(self, strategy_one, strategy_two):
        self.board = [0 for _ in range(9)]

        if isinstance(strategy_one, list): strategy_one = strategy_one[0]

        if isinstance(strategy_two, list): strategy_two = strategy_two[0]

        self.strategies = [strategy_one, strategy_two]

    def play(self):
        current_player = 0
        #new_possible_moves = [{}, {}]
        while not self.game_finished()[0] and self.board.count(0) > 0:
            current_state = self.state()
            if current_state in self.strategies[current_player].keys():
                current_move = self.strategies[current_player][current_state]
            else:
                choices = [i for i in range(9) if self.board[i] == 0]
                current_move = random.choice(choices)
                #new_possible_moves[current_player][current_state] = current_move
            self.place(current_player, current_move)
            
            current_player = 1 if current_player == 0 else 0

        winner = self.game_finished()

        # new_possible_moves[current_player - 1][current_state] = current_move # next time dont let player win using same move

        # for current_player, new_moves in enumerate(new_possible_moves):
        #     if current_player + 1 == winner[1] or not winner[0]:
        #         for state, move in new_moves.items():
        #             self.strategies[current_player][state] = move

        if winner[1] == None and self.board.count(0) == 0:
            #print("\tDraw")
            #print("\tBoard State", self.state())

            return ((False, "Draw", winner[2]), self.strategies)

        #print("\tPlayer", winner[1], "Wins")
        #print("\tBoard State", self.state())

        return (winner, self.strategies)
        
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
        if self.board.count(0) > 4: return (False, None, None)
        for index, space in enumerate(self.board):

            horizontal = index in [0, 3, 6] and not self.board[index] != 0 and self.board[index + 1] == space and self.board[index + 2] == space
            vertical = index in [0, 1, 2] and not self.board[index] != 0 and self.board[index + 3] == space and self.board[index + 6] == space
            forward_diagonal = index in [0, 4, 8] and not self.board[index] != 0 and self.board[0] == space and self.board[4] == space and self.board[8] == space
            backward_diagonal = index in [2, 4, 6] and not self.board[index] != 0 and self.board[2] == space and self.board[4] == space and self.board[6] == space
            
            connected = [horizontal, vertical, forward_diagonal, backward_diagonal]

            if connected.count(True) > 0: return (True, space, connected)

        return (False, None, None)