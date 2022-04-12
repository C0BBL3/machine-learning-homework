import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game

class Minimax:

    def generate_tree( self, game, current_player, root_node = None, max_depth = 9 ): # current_player is wack

        for current_depth in range(max_depth - 1):
        
            if current_depth == 0:
                
                self.initial_player = current_player
                self.nodes = list() # initialize self.nodes list

                for depth in range( max_depth + 1 ):

                    self.nodes.append( list() )

                if root_node is None:

                    root_node = Node( game.board, index = 0 )

                self.nodes[0].append( root_node )
                current_player = game.get_next_player( current_player )

            else:

                root_nodes = self.nodes[ current_depth - 1]
                current_nodes = self.nodes[ current_depth ]

                for root in root_nodes: # generate whole depth layer

                    branches = game.get_possible_branches( root.board_state, current_player ) # list of board states
                    self.grow_branches( game, root, current_nodes, branches )
                
                current_player = game.get_next_player( current_player )

    def grow_branches( self, game, root, current_nodes, branches ):

        for branch in branches:

            new_index = sum( [ len( nodes ) for nodes in self.nodes ] )
            new_node = Node( board_state = branch, index = new_index )
            if sum(node == new_node for node in current_nodes) == 0:
                current_nodes.append( new_node )
                root.append_child( new_node ) # add new node to current root

    def evaluate_game_tree( self, game ):

        current_player = int( self.initial_player )

        for _ in self.nodes:

            current_player = game.get_next_player( current_player )

        for nodes in self.nodes[ : -1 ]: # leaves of game tree get evaluated

            for node in nodes:

                node.value = game.evaluate( node.board_state, current_player )

        for i, nodes in enumerate( self.nodes[ : 0 : -1 ] ): # ahhhhhhhh
            # no root node in iteration backwards 

            for node in nodes:

                for parent_index in node.parents:

                    # backtrack up the tree to give the parents value
                    parent_depth = len(self.nodes) - i - 2
                    parent = list( filter( lambda node: node.index == parent_index, self.nodes[ parent_depth ] ) )[0]
                    parent.value += node.value 

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

    def append_child(self, node): # parent += child
        if node.index not in self.children:
            self.children.append( node.index )
        if self.index not in node.parents:
            node.parents.append( self.index )

    def kill_child(self, node): # parent -= child
        if node.index in self.children:
            self.children.remove( node.index )
        if self.index in node.parents:
            node.parents.remove( self.index )

