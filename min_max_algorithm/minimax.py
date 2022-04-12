import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game

class Minimax:

    def generate_tree( self, game, current_player, root_node = None, max_depth = 9, prune = True ): # current_player is wack

        self.initial_player = current_player
        self.nodes = list() # initialize self.nodes list

        for depth in range( max_depth + 1 ):

            self.nodes.append( list() )

        if root_node is None:

            root_node = Node( game.board, index = 0 )

        self.nodes[0].append( root_node )
        
        for current_depth in range(1, max_depth + 1):

            print('bop')
        
            root_nodes = self.nodes[ current_depth - 1]

            for root in root_nodes: # generate whole depth layer

                if game.game_finished(board_state = root.board_state)[0]: continue 
                branches = game.get_possible_branches( root.board_state, current_player ) # list of board states
                self.grow_branches( game, root, current_depth, branches, prune = prune )
            
            current_player = game.get_next_player( current_player )
            print(len(self.nodes[current_depth]))

    def grow_branches( self, game, root, current_depth, branches, prune = True ):

        current_nodes = self.nodes[ current_depth ]

        for branch in branches:

            new_index = sum( [ len( nodes ) for nodes in self.nodes ] )
            new_node = Node( board_state = branch, index = new_index )
            similar_nodes = list( filter( lambda node: node == new_node, current_nodes ) )

            if len( similar_nodes ) == 0 or not prune:

                current_nodes.append( new_node )
                root.append_child( new_node )
                # add new node to current root

            else:

                similar_nodes_parents = list()

                for similar_node in similar_nodes:
                
                    for parent_index in similar_node.parents:

                        parent = self.get_node( current_depth - 1, parent_index)
                        if parent not in similar_nodes_parents:
                            similar_nodes_parents.append( parent )

                for parent in similar_nodes_parents:

                    for child in similar_nodes:

                        if child.index not in parent.children:

                            parent.append_child( child )

                        if child.index not in root.children:

                            root.append_child( child )

                        
                

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
                    parent_depth = len( self.nodes ) - i - 2
                    parent = self.get_node(parent_depth, parent_index)
                    parent.value += node.value 

    def get_best_move( self, root_board_state ):

        best_node = max( self.nodes[ 1 ], key = lambda node: node.value )
        
        for move, i in enumerate( root_board_state ):
            
            j = best_node.board_state[ move ]

            if i != j: return move

        return None

    def get_node(self, depth, index):
        parent = list( filter( lambda node: node.index == index, self.nodes[ depth ] ) )[0]
        return parent

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

