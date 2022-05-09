import math

class Game:
    
    def __init__( self, strategy_one, strategy_two, current_player = 1 ):

        self.board = [ 0 for _ in range( 9 ) ]
        self.strategies = [ strategy_one, strategy_two ] 
        # ^^^^^^ [ function, function]
        self.state()
        self.current_player = current_player

    def play( self ):

        while not self.game_finished()[ 0 ] and self.board.count( 0 ) > 0:

            current_state = self.state( current_player = self.current_player )
            current_move = self.strategies[ self.current_player - 1 ]( self.board, self.current_player )
            self.place( self.current_player, current_move )
            self.current_player = self.get_next_player( self.current_player )

        winner = self.game_finished()

        if winner[ 1 ] == None: return ( False, "Draw" )

        return winner
        
    def place( self, player, index ): # 1 or 2 for player, and index is 0-9
        try:

            if self.board[ index ] == 0: 

                self.board[ index ] = player

            else: 

                raise ValueError

        except ValueError as va:

            print( "Player", player, "tried to cheat by placing a piece on space", player )
            print( "Board state", self.state() )
            exit()

    def state( self, current_player = 1 ):
        switcher = { 0: 0, 1: 1, 2: 2 }
        if current_player == 2: 
            switcher = { 0: 0, 1: 2, 2: 1 }
        return ''.join( [ str( switcher[ space ] ) for space in self.board ] )

    def get_next_player( self, current_player ):
        return 2 if current_player == 1 else 1
    
    def get_possible_branches( self, board_state, current_player ):
        
        possible_branches = [ i for i in range( 9 ) if int( board_state[ i ] ) == 0 ]

        return [ 
            board_state[ : i ] + [ current_player ] + board_state[ i + 1 : ] 
            for i in possible_branches
        ]
            

    def game_finished( self, board_state = None ):

        if board_state is None:
            board_state = self.board

        # horizontal
        if board_state[ 0 ] == board_state[ 1 ] == board_state[ 2 ] != 0: 
            return ( True, board_state[ 0 ] ) 
        if board_state[ 3 ] == board_state[ 4 ] == board_state[ 5 ] != 0: 
            return ( True, board_state[ 3 ] )
        if board_state[ 6 ] == board_state[ 7 ] == board_state[ 8 ] != 0: 
            return ( True, board_state[ 6 ] )

        # vertical
        if board_state[ 0 ] == board_state[ 3 ] == board_state[ 6 ] != 0: 
            return ( True, board_state[ 0 ] )
        if board_state[ 1 ] == board_state[ 4 ] == board_state[ 7 ] != 0: 
            return ( True, board_state[ 1 ] )
        if board_state[ 2 ] == board_state[ 5 ] == board_state[ 8 ] != 0: 
            return ( True, board_state[ 2 ] )

        # diagonal
        if board_state[ 0 ] == board_state[ 4 ] == board_state[ 8 ] != 0: 
            return ( True, board_state[ 0 ] ) 
        
        # backwards diagonal
        if board_state[ 2 ] == board_state[ 4 ] == board_state[ 6 ] != 0: 
            return ( True, board_state[ 2 ] ) 

        if board_state.count( 0 ) == 0:
            return ( False, None )

        return ( False, None )

    def evaluate( self, board_state, player ):

        win = num_wins( board_state, player )
        lose = num_wins( board_state, self.get_next_player( player ) )

        # total possible wins - total possible losses
        return win - lose

def plots_3_and_4( board_state, player ): # cringe

    moves = list()

    #horizontal
    if board_state[ 0 ] == board_state[ 1 ] == player and board_state[ 0 ] == 0: 
        moves.append( 0 )
    if board_state[ 0 ] == board_state[ 2 ] == player and board_state[ 1 ] == 0: 
        moves.append( 1 )
    if board_state[ 0 ] == board_state[ 1 ] == player and board_state[ 2 ] == 0: 
        moves.append( 2 )

    if board_state[ 4 ] == board_state[ 5 ] == player and board_state[ 3 ] == 0: 
        moves.append( 3 )
    if board_state[ 3 ] == board_state[ 5 ] == player and board_state[ 4 ] == 0: 
        moves.append( 4 )
    if board_state[ 3 ] == board_state[ 4 ] == player and board_state[ 5 ] == 0: 
        moves.append( 5 )

    if board_state[ 7 ] == board_state[ 8 ] == player and board_state[ 6 ] == 0: 
        moves.append( 6 )
    if board_state[ 6 ] == board_state[ 8 ] == player and board_state[ 7 ] == 0: 
        moves.append( 7 )
    if board_state[ 6 ] == board_state[ 7 ] == player and board_state[ 8 ] == 0: 
        moves.append( 8 )

    #vertical
    if board_state[ 3 ] == board_state[ 6 ] == player and board_state[ 0 ] == 0: 
        moves.append( 0 )
    if board_state[ 4 ] == board_state[ 7 ] == player and board_state[ 1 ] == 0: 
        moves.append( 1 )
    if board_state[ 5 ] == board_state[ 8 ] == player and board_state[ 1 ] == 0: 
        moves.append( 2 )

    if board_state[ 0 ] == board_state[ 6 ] == player and board_state[ 0 ] == 0: 
        moves.append( 3 )
    if board_state[ 1 ] == board_state[ 7 ] == player and board_state[ 1 ] == 0: 
        moves.append( 4 )
    if board_state[ 2 ] == board_state[ 8 ] == player and board_state[ 2 ] == 0: 
        moves.append( 5 )

    if board_state[ 0 ] == board_state[ 3 ] == player and board_state[ 0 ] == 0: 
        moves.append( 6 )
    if board_state[ 1 ] == board_state[ 4 ] == player and board_state[ 1 ] == 0: 
        moves.append( 7 )
    if board_state[ 2 ] == board_state[ 5 ] == player and board_state[ 1 ] == 0: 
        moves.append( 8 )

    #diagonal
    if board_state[ 4 ] == board_state[ 8 ] == player and board_state[ 0 ] == 0: 
        moves.append( 0 )
    if board_state[ 0 ] == board_state[ 8 ] == player and board_state[ 4 ] == 0: 
        moves.append( 4 )
    if board_state[ 0 ] == board_state[ 4 ] == player and board_state[ 8 ] == 0: 
        moves.append( 8 )

    #backwards diagonal
    if board_state[ 4 ] == board_state[ 6 ] == player and board_state[ 2 ] == 0: 
        moves.append( 2 )
    if board_state[ 2 ] == board_state[ 6 ] == player and board_state[ 4 ] == 0: 
        moves.append( 4 )
    if board_state[ 2 ] == board_state[ 4 ] == player and board_state[ 6 ] == 0: 
        moves.append( 6 )

    return len( moves ) > 0, moves

def num_wins( board_state, player ): # cringe

    wins = int()

    #horizontal
    if board_state[ 0 ] == board_state[ 1 ] == board_state[ 2 ] == player: 
        wins += 1
    if board_state[ 3 ] == board_state[ 4 ] == board_state[ 5 ] == player: 
        wins += 1
    if board_state[ 6 ] == board_state[ 7 ] == board_state[ 8 ] == player: 
        wins += 1

    #vertical
    if board_state[ 0 ] == board_state[ 3 ] == board_state[ 6 ] == player: 
        wins += 1
    if board_state[ 1 ] == board_state[ 4 ] == board_state[ 7 ] == player: 
        wins += 1
    if board_state[ 2 ] == board_state[ 5 ] == board_state[ 8 ] == player:
        wins += 1

    #diagonal
    if board_state[ 0 ] == board_state[ 4 ] == board_state[ 8 ] == player: 
        wins += 1

    #backwards diagonal
    if board_state[ 2 ] == board_state[ 4 ] == board_state[ 6 ] == player: 
        wins += 1

    return wins