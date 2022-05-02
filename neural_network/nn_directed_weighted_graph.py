class NNDirectedWeightedGraph:
    def __init__(self, weights, vertex_values):
        self.weights = weights
        self.nodes = [DirectedWeightedNode(index) for index in vertex_values]
        self.make_nodes()

    def make_nodes(self):  # Self explanitory
        for neighbors, weight in self.weights.items():
            current_node, child_node = neighbors
            self.nodes[current_node].set_child(self.nodes[child_node], weight)
        for node in self.nodes:
            node.set_depth(self.get_depth(node.index))

    def set_node_values(self):
        for node in self.nodes:
            node.value = 0
            node.predicted_count = 0

    # Utilizes BacktrackingTM to get the depth recursively
    # For Debugging
    def get_depth(self, index, current_depth = 0):
        if self.nodes[index].parents == list():
            first_child_index = self.nodes[index].children[ 0 ]
            if self.nodes[first_child_index].parents == [index]:
                return current_depth
            temp = 0
            sibling_index = self.nodes[first_child_index].parents[temp]
            if sibling_index == index:
                try:
                    temp += 1
                    sibling_index = self.nodes[first_child_index].parents[temp]
                except:
                    sibling_index = None
            if sibling_index is None or self.nodes[sibling_index].parents == list():
                # If the given node is the input node and has no parents after backtracking, 
                # as well as it's siblings in the same layer dont have parents, return the current depth
                # this is to check for bias node
                return current_depth
            else:
                # continue backtracking with non-bias-node sibling
                index = sibling_index
        # Return the node's first parent's index and increase the current depth count
        first_parent = self.nodes[index].parents[0]
        return self.get_depth(first_parent, current_depth = current_depth + 1)

    def get_every_possible_path_containing_edge(self, current_paths=[]):
        # Start would be the initial edge
        # Edge is a tuple of two node indices, for example Edge 0 -> 2 would be denoted as `(0,2)`
        # Would find every possible path, recursively through each of the start's children to the output node(s)
        is_output = 0
        new_paths = []
        for path in current_paths:
            if len(self.nodes[path[-1]].children) == 0:
                is_output += 1
                continue
            for node_index in self.nodes[path[-1]].children:
                new_paths.append(list(path + [node_index]))
        if is_output == len(current_paths):
            return current_paths
        return self.get_every_possible_path_containing_edge(current_paths=new_paths)

    def get_every_possible_path_containing_index(self, index):
        paths = []
        for child_index in self.nodes[index].children:
            paths += self.get_every_possible_path_containing_edge(current_paths=[[index, child_index]])
        return paths


class DirectedWeightedNode:
    def __init__(self, index):
        self.index = index
        self.input = 0
        self.value = 0
        self.children = []
        self.parents = []
        self.children_weights = {}
        self.parents_weights = {}
        self.predicted_count = 0

    def set_depth(self, depth):
        self.depth = depth

    def set_child(self, child, weight):
        if child.index not in self.children:
            self.children.append(child.index)
        if self.index not in child.parents:
            child.parents.append(self.index)
        self.set_edge_weights(child, weight)

    def set_edge_weights(self, child, weight):
        if child.index not in self.children_weights.keys():
            self.children_weights[child.index] = weight
        if self.index not in child.parents_weights.keys():
            child.parents_weights[self.index] = weight
