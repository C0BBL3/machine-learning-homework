import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph


class NeuralNetwork(NNDirectedWeightedGraph):
    def __init__(self, weights, activation_functions = None, activation_function_derivatives = None, bias = False, data_points={}, alpha=0.001, debug=False):
        # Inhereit from a DirectedWeightedGraph to make the net
        node_indices = sorted(set([_ for key in weights.keys() for _ in key]))
        super().__init__(weights=weights, vertex_values=node_indices) 
        self.bias = bias
        if activation_functions is not None and activation_function_derivatives is not None:
            self.activation_functions = activation_functions
            self.activation_function_derivatives = activation_function_derivatives
        else: # If no Activation Functions given, then linear for all
            self.activation_functions = [lambda x: x for _ in range(0, len(node_indices))]
            self.activation_function_derivatives = [lambda x: 1 for _ in range(0, len(node_indices))]
        self.alpha = alpha
        self.debug = debug
        self.data_points = data_points # Temporary
        self.set_weight_gradients()
        self.set_misclassifications() # Temporary
        self.set_predictions()

    def set_weight_gradients(self):
        self.weight_gradients = {edge: 0.0 for edge in self.weights.keys()}

    def set_misclassifications(self):
        self.misclassifications = {tuple(data_point['input']): False for data_point in self.data_points}

    def set_predictions(self):
        self.predictions = {tuple(data_point['input']): 0.0 for data_point in self.data_points}

    def update_weights(self, print_output=False, iteration=1):
        new_weights = dict(self.weights)
        for edge in self.weights.keys():
            new_weights[edge] -= self.alpha * self.weight_gradients[edge] # Descent `edge`'s Weight
        self.weights = dict(new_weights)
        del new_weights
        if print_output and (iteration < 6 or iteration % 1000 == 0):
            self.print_outputs(iteration) # Self explainitory
        self.set_weight_gradients()
        self.set_misclassifications() # Temporary
        self.set_predictions()

    def update_weight_gradients(self, data_point, edge):
        dE = self.calc_dE(data_point, edge) # Calculate Gradient
        if data_point['output'](self.predictions[tuple(data_point['input'])]) != 0.0:
            self.misclassifications[tuple(data_point['input'])] = True
            self.weight_gradients[edge] += dE # Update Gradient
        if self.debug:
            self.print_debugging_variables(data_point, edge, dE)
        self.set_node_values() # Reset the values, that are used for prediction, of all the nodes

    def calc_dE(self, data_point, edge):
        self.calc_prediction(data_point)
        #print('\n\n[list(edge)]', [list(edge)])
        every_possible_path_containing_edge = self.get_every_possible_path_containing_edge(current_paths=[list(edge)])
        total_weight = 0
        for path in every_possible_path_containing_edge:
            total_weight += math.prod([self.weights[(path[i], path[i + 1])] * self.activation_function_derivatives[path[i]](self.get_node_input(path[i])) for i in range(1, len(path) - 1)])
        #print('\tevery_possible_path_containing_edge', every_possible_path_containing_edge)
        #print("\tdata_point['output'](self.predictions[tuple(data_point['input'])])", data_point['output'](self.predictions[tuple(data_point['input'])]))
        #print('\ttotal_weight', total_weight)
        #print("\tself.activation_function_derivatives[edge[0]](self.get_node_input[edge[0]])", self.activation_function_derivatives[edge[0]](self.get_node_input(edge[0])))
        #print("\tedge[0]", edge[0])
        #print("\tself.nodes[edge[0]].value", self.nodes[edge[0]].value)
        
        return 2 * data_point['output'](self.predictions[tuple(data_point['input'])]) * total_weight * self.activation_function_derivatives[edge[0]](self.get_node_input(edge[0])) * self.nodes[edge[0]].value
        
    def calc_prediction(self, data_point):
        # Start and Depth First Recursion Iteration through input nodes
        # Using recursion, Depth First search through the nodes
        # The output node(s)'s value is be the prediction(s)
        current_depth_nodes = [node.index for node in self.nodes if self.get_depth(node.index) == 0]
        for index, node_index in enumerate(current_depth_nodes):
            if index < len(data_point['input']):
                self.nodes[node_index].value = self.activation_functions[node_index](data_point['input'][index])
            else:
                self.nodes[node_index].value = self.activation_functions[node_index](1)
            #print('\tNode', node_index, 'value', self.nodes[node_index].value)
        self.fortrack_prediction(1)
        self.predictions[tuple(data_point['input'])] = self.nodes[-1].value

    # Backtrack, but forwards | back-wards <-> for-wards = back-track <-> for-track
    def fortrack_prediction(self, depth):
        # Depth First Recursion Iteration through nodes
        # Updating their prediction values along the way
        current_depth_nodes = [node.index for node in self.nodes if self.get_depth(node.index) == depth]
        for node_index in current_depth_nodes:
            self.nodes[node_index].value = self.get_node_input(node_index)
            #print('\tNode', node_index, 'value', self.nodes[node_index].value)
        if len(self.nodes[node_index].children) > 0: # If not output node
            self.fortrack_prediction(depth + 1)

    def get_node_input(self, node_index):
        result = 0
        for parent in self.nodes[node_index].parents:
            result += self.weights[(parent, node_index)] * self.nodes[parent].value
        return self.activation_functions[node_index](result)
        
    def print_outputs(self, iteration):
        print('iteration {}'.format(iteration))
        print('\tgradient: {}'.format(self.weight_gradients))
        print('\tmisclassifications: {}'.format(list(self.misclassifications.values()).count(True)))
        print('\tpredictions: {}'.format(self.predictions))
        print('\tupdated weights: {}'.format(self.weights))

    def print_debugging_variables(self, data_point, edge, dE):
        print('\nedge', edge)
        print('\tdata_point', data_point['input'])
        print('\tdE', dE)
        print('\tmisclassifications', sum([1.0 for classification in self.misclassifications.values() if classification]))
        print('\tself.weight_gradients[edge]', self.weight_gradients[edge])