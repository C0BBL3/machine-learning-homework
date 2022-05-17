import math

class Game:
    
    def __init__( self, strategy_one, strategy_two, current_player = 1 ):

        self.board = [ 0 for _ in range( 9 ) ]
        self.strategies = [ strategy_one, strategy_two ] 
        # ^^^^^^          [   function  ,   function   ]
        self.state()
        self.current_player = current_player
        self.logs = list()
        self.all_possible_winning_combinations = [
            [ 0, 1, 2 ], 
            [ 3, 4, 5 ], 
            [ 6, 7, 8 ], 
            [ 0, 3, 6 ], 
            [ 1, 4, 7 ],
            [ 2, 5, 8 ],
            [ 0, 4, 8 ],
            [ 2, 4, 6 ]
        ]
        
        self.winning_board_states = { 
            line.strip( '\n' ) 
            for line in open( 'metaheuristic_algorithm/ttt_board_states/winning_board_states.txt', 'r' ).readlines() 
        } # make set for fast

        self.losing_board_states = { 
            line.strip( '\n' ) 
            for line in open( 'metaheuristic_algorithm/ttt_board_states/losing_board_states.txt', 'r' ).readlines() 
        }

        self.tieing_board_states = { 
            line.strip( '\n' ) 
            for line in open( 'metaheuristic_algorithm/ttt_board_states/tieing_board_states.txt', 'r' ).readlines() 
        }

    def play( self ):

        while not self.game_finished()[ 0 ]:

            current_state = self.state( current_player = self.current_player )
            current_move = self.strategies[ self.current_player - 1 ]( self.board, self.current_player )
            self.place( self.current_player, current_move )
            self.current_player = self.get_next_player( self.current_player )
            self.logs.append( self.state() )

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

    def get_possible_branches( self, board_state, current_player ):
        
        possible_branches = [ i for i in range( 9 ) if int( board_state[ i ] ) == 0 ]

        return [ 
            board_state[ : i ] + [ current_player ] + board_state[ i + 1 : ] 
            for i in possible_branches
        ]
            

    def game_finished( self, board_state = None ):

        if board_state is None:
            board_state = self.board
        
        string_board_state = ''.join( 
            [ 
                str( space ) 
                for space in board_state 
            ]
        )

        if string_board_state in self.winning_board_states:
            return ( 
                True, 
                self.current_player 
            )
        elif string_board_state in self.losing_board_states:
            return ( 
                True, 
                self.get_next_player( self.current_player ) 
            )
        elif string_board_state in self.tieing_board_states:
            return (
                True,
                'Draw'
            )
        else:
            return ( False, True )

    def evaluate( self, board_state, player ):

        temp = self.game_finished( board_state = board_state )
        next_player = self.get_next_player( player )

        if temp[ 0 ] and temp[ 1 ] == player:
            
            return 1

        elif temp[ 0 ] and temp[ 1 ] == next_player:

            return -1

        elif temp[ 0 ] and temp[ 1 ] == 'Draw':
 
            return 0

    def get_next_player( self, current_player ):
            return { 1 : 2, 2 : 1 }[ current_player ]

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

