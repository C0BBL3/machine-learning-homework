from game import Game

class Minimax:

    def generate_tree( self, game, current_player, root_node = None, current_depth = 0, max_depth = 3 ): # current_player is wack

        if current_depth == 0:
            
            self.initial_player = current_player
            self.nodes = list() # initialize self.nodes list

            for depth in range( max_depth ):

                self.nodes.append( list() )

            self.nodes[0].append( root_node )

        elif 0 < current_depth < max_depth:

            root_nodes = self.nodes[ current_depth ]
            current_nodes = self.nodes[ current_depth + 1 ]
            next_player = game.get_next_player( current_player )

            for root in root_nodes: # generate whole depth layer

                branches = game.get_possible_branches( root.board_state, current_player ) # list of board states
                self.grow_branches( game, root, current_player, current_nodes, branches )
            
            for root in root_nodes: # generate tree from new depth layer
                
                self.generate_tree( game, next_player, current_depth = current_depth + 1 )
            
    def grow_branches( self, game, root, current_nodes, branches ):

        for branch in branches:

            new_index = sum( [ len( nodes ) for nodes in self.nodes ] )
            new_node = Node( board_state = branch, index = new_index )
            current_nodes.append( new_node )
            root += new_node # add new node to current root

        current_nodes.sort( key = lambda node: node.index ) # for sleeping better at night

        for node in current_nodes:

            similar_nodes = list( filter( lambda node: node == new_node, current_nodes ) ) # what the fuck

            if len(similar_nodes) > 0: # if there are similar nodes

                for similar_node in similar_nodes:

                    if root.index in similar_node.parents:
                        
                        root -= similar_node # remove "siblings" of current root

                        similar_node = None # kill

    def evaluate_game_tree( self ):

        current_player = int( self.initial_player )

        for _ in self.nodes:

            current_player = game.get_next_player( current_player )

        for node in self.nodes[ : -1 ]: # leaves of game tree get evaluated

            node.value = game.evaluate( node.board_state, current_player )

        for nodes in self.nodes[ : 0 : -1 ]: # ahhhhhhhh
            # no root node in iteration backwards 

            for node in nodes:

                for parent in node.parents:

                    parent.value += node.value # backtrack up the tree to give the parents value

    def get_best_move( self, root_board_state ):

        best_node = max( self.nodes[ 0 ], key = lambda node: node.value )
        
        for move, i in enumerate( root_board_state ):
            
            j = best_node.board_state[ move ]

            if i != j: return move

class Node:
    def __init__( self, board_state = list(), value = int(), index = int() ):
        self.board_state = board_state
        self.value = value
        self.index = index
        self.parents = []
        self.children = []

    def __eq__(self, node): # if node == node
        return self.board_state == node.board_state

    def __iadd__(self, node): # parent += child
        if node.index not in self.children:
            self.children.append( node.index )
        if self.index not in node.parents:
            node.parents.append( self.index )

    def __isub__(self, node): # parent -= child
        if node.index in self.children:
            self.children.remove( node.index )
        if self.index in node.parents:
            node.parents.remove( self.index )

