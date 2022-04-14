import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game

class Minimax:

    def generate_tree( self, game, current_player, root_board_state = None, max_depth = 9, prune = True ): # current_player is wack

        self.leaf_node_count = int()
        self.initial_player = current_player
        self.nodes = list() # initialize self.nodes list

        for depth in range( max_depth + 1 ):

            self.nodes.append( list() )

        if root_board_state is None:

            root_node = Node( game.board, index = 0 )

        self.nodes[0].append( root_node )
        
        for current_depth in range(1, max_depth + 1):
        
            root_nodes = self.nodes[ current_depth - 1]

            for root in root_nodes: # generate whole depth layer

                if game.game_finished(board_state = root.board_state)[0]: continue
                branches = game.get_possible_branches( root.board_state, current_player ) # list of board states
                self.grow_branches( game, root, current_depth, branches, prune = prune )
            
            current_player = game.get_next_player( current_player )

        for nodes in self.nodes:

            for node in nodes:

                if node.children == []:
                    
                    self.leaf_node_count += 1

    def grow_branches( self, game, root, current_depth, branches, prune = True ):

        current_nodes = self.nodes[ current_depth ]

        for branch in branches:

            if not prune:

                self.create_children( root, branch, current_nodes )

            else:

                similar_node = next( current_nodes, lambda node: node.board_state == branch )
  
                if similar_node is None:

                    self.create_children( root, branch, current_nodes )

                else:

                    self.prune( similar_node, root, current_depth)

    def create_children( self, root, branch, current_nodes ):

        new_index = sum( [ len( nodes ) for nodes in self.nodes ] )
        new_node = Node( board_state = branch, index = new_index )
        current_nodes.append( new_node )
        root.append_child( new_node )

    def prune( self, similar_node, root, current_depth ):
        
        similar_nodes_parents = list()

        while similar_node is not None:
        
            for parent_index in similar_node.parents:

                parent = self.get_node(parent_index, current_depth - 1)
                if parent not in similar_nodes_parents:
                    similar_nodes_parents.append( parent )

            similar_node = next( current_nodes, lambda node: node.board_state == branch )

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
                    parent = self.get_node(parent_index)
                    parent.value += node.value 

    def get_best_move( self, root_board_state ):

        best_node = max( self.nodes[ 1 ], key = lambda node: node.value )
        
        for move, i in enumerate( root_board_state ):
            
            j = best_node.board_state[ move ]

            if i != j: return move

        return None

    def get_node(self, index, depth = int()):

        if depth == int():

            for nodes in self.nodes:

                if len(nodes) > index:

                    depth -= 1
                    break

                else: depth += 1

        parent = next( self.nodes[ depth ], lambda node: node.index == index )
        
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

