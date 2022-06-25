from tic_tac_toe import Game
import sys
sys.path.append('metaheuristic_algorithm/')


class Minimax:

    # current_player is wack
    def generate_tree(self, game, current_player, root_board_state=None, max_depth=9, prune=True):

        self.initial_player = int(current_player)
        self.prune_bool = prune
        self.max_depth = max_depth
        self.edges = list()

        if root_board_state is None:

            root_board_state = game.board

        self.nodes = {
            0: Node(
                root_board_state,
                index=0,
                depth=0,
                player=self.initial_player
            )
        }

        if current_player == 2:
            current_player = game.get_next_player(current_player)

        for current_depth in range(max_depth):

            current_nodes = {
                node_index: node
                for node_index, node in self.nodes.items()
                if node.depth == current_depth
            }

            for current_node_index, current_node in current_nodes.items():  # generate whole depth layer

                if game.game_finished(board_state=current_node.board_state)[0]:
                    continue

                self.grow_branches(
                    game,
                    current_node,
                    current_depth + 1,
                    current_player,
                )

            current_player = game.get_next_player(current_player)

        self.leaf_nodes = {
            node_index: node
            for node_index, node in self.nodes.items()
            if node.children == set()
        }

    def grow_branches(self, game, current_node, current_depth, current_player):

        branches = game.get_possible_branches(  # list of board states
            current_node.board_state,
            current_player
        )

        current_nodes = {
            node_index: node
            for node_index, node in self.nodes.items()
            if node.depth == current_depth
        }

        for branch in branches:

            if not self.prune_bool:

                self.create_children(
                    current_node, branch, current_nodes, current_depth, current_player)

            else:

                similar_nodes = {
                    node_index: node
                    for node_index, node in current_nodes.items()
                    if node.board_state == branch
                }

                if similar_nodes == dict():

                    self.create_children(
                        current_node, branch, current_nodes, current_depth, current_player)

                else:

                    self.prune(similar_nodes, current_node, current_depth)

    def create_children(self, current_node, branch, current_nodes, depth, player):

        new_node_index = len(self.nodes)
        new_node = Node(
            board_state=branch,
            index=new_node_index,
            depth=depth,
            player=player
        )
        self.nodes[new_node_index] = new_node
        self.edges.append([current_node.index, new_node_index])
        current_node.append_child(new_node)

    def prune(self, similar_nodes, current_node, current_depth):

        similar_nodes_parents = dict()

        for similar_node_index, similar_node in similar_nodes.items():

            for parent_index in similar_node.parents:

                parent = self.nodes[parent_index]

                if parent not in similar_nodes_parents.values():

                    similar_nodes_parents[parent_index] = parent

        for parent in similar_nodes_parents.values():

            for child in similar_nodes.values():

                parent.append_child(child)
                current_node.append_child(child)

    def evaluate_game_tree(self, game, evaluation_function):

        for node_index in range(len(self.nodes) - 1, -1, -1):

            node = self.nodes[node_index]

            if node.children == set():

                node.value = evaluation_function(
                    node.board_state,
                    self.initial_player
                )

                continue

            if self.initial_player == 2:

                if node.player != self.initial_player:
                    function = min
                else:
                    function = max

            else:

                if node.player == self.initial_player:
                    function = min
                else:
                    function = max

            best_child_index = function(
                node.children,
                key=lambda child_index: self.nodes[child_index].value
            )

            node.value = self.nodes[best_child_index].value

        self.first_layer_nodes = [
            node
            for node in self.nodes.values()
            if node.depth == 1
        ]

    def get_best_move(self, current_node_board_state):

        best_node = max(self.first_layer_nodes, key=lambda node: node.value)

        for move, i in enumerate(current_node_board_state):

            j = best_node.board_state[move]

            if i != j:
                return move

        return None


class Node:
    def __init__(self, board_state=list(), value=int(), index=int(), depth=int(), player=int()):
        self.board_state = board_state
        self.value = value
        self.index = index
        self.depth = depth
        self.player = player
        self.parents = set()
        self.children = set()

    def __eq__(self, node):  # if node == node
        return self.board_state == node.board_state

    def append_child(self, node):  # parent += child
        if node.index not in self.children:
            self.children.add(node.index)
        if self.index not in node.parents:
            node.parents.add(self.index)

    def kill_child(self, node):  # parent -= child
        if node.index in self.children:
            self.children.remove(node.index)
        if self.index in node.parents:
            node.parents.remove(self.index)
