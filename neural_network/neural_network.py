import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph


class NeuralNetwork(NNDirectedWeightedGraph):
    def __init__(self, weights, functions = None, derivatives = None, data_points={}, alpha=0.001, debug=False):
        # Inhereit from a DirectedWeightedGraph to make the net
        node_indices = sorted(set([_ for key in weights.keys() for _ in key]))
        super().__init__(weights=weights, vertex_values=node_indices) 
        if functions is not None and derivatives is not None:
            self.functions = functions
            self.derivatives = derivatives
        else: # If no Activation Functions given, then linear for all
            self.functions = [lambda x: x for _ in range(0, len(node_indices))]
            self.derivatives = [lambda x: 1 for _ in range(0, len(node_indices))]
        self.alpha = alpha
        self.debug = debug
        self.data_points = data_points # Temporary
        self.set_gradients()
        self.set_misclassifications() # Temporary
        self.set_predictions()

    def set_gradients(self):
        self.weight_gradients = {edge: 0.0 for edge in self.weights.keys()}
        self.neuron_gradients = {node.index: 0.0 for node in self.nodes}
        self.intermediate_neuron_gradients = {edge: None for edge in self.weights.keys()}

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
        self.set_gradients()
        self.set_misclassifications() # Temporary
        self.set_predictions()

    def update_neuron_gradients(self, data_point, node_index):
        self.neuron_gradients[node_index] += 2.0 * data_point['output'](self.predictions[tuple(data_point['input'])])
        total_weight = 0.0
        every_possible_path_containing_edge = self.get_every_possible_path_containing_edge(current_paths=[list([node_index])])
        for path in every_possible_path_containing_edge: # Iterate through every path from the `node_index` to the (or a) output node
            intermediate_neuron_gradients_along_path_temp = 1.0
            for i in range(0, len(path) - 1): # Iterate through the current path
                edge = (path[i], path[i + 1]) # Get Current Edge
                if self.intermediate_neuron_gradients[edge] is None:
                    self.intermediate_neuron_gradients[edge] = self.weights[edge] * self.derivatives[path[i]](self.nodes[path[i+1]].input) # Update Intermediate Neuron Gradients
                    intermediate_neuron_gradients_along_path_temp *= self.intermediate_neuron_gradients[edge]
                else:
                    intermediate_neuron_gradients_along_path_temp *= self.intermediate_neuron_gradients[edge]
            total_weight += intermediate_neuron_gradients_along_path_temp
        self.neuron_gradients[node_index] *= total_weight  # Update Neuron Gradients

    def update_weight_gradients(self, data_point, edge):
        dE = self.calc_dE(data_point, edge) # Calculate Gradient
        if data_point['output'](self.predictions[tuple(data_point['input'])]) != 0.0:
            self.misclassifications[tuple(data_point['input'])] = True
            self.weight_gradients[edge] += dE # Update Gradient
        if self.debug:
            self.print_debugging_variables(data_point, edge, dE)

    def calc_dE(self, data_point, edge):
        return self.neuron_gradients[edge[1]] * self.derivatives[edge[1]](self.nodes[edge[1]].input) * self.nodes[edge[0]].value
        
    def calc_prediction(self, data_point):
        # Start and Depth First Recursion Iteration through input nodes
        # Using recursion, Depth First search through the nodes
        # The output node(s)'s value is be the prediction(s)
        current_depth_nodes = [node.index for node in self.nodes if self.get_depth(node.index) == 0]
        for index, node_index in enumerate(current_depth_nodes):
            if index < len(data_point['input']):
                self.nodes[node_index].input = data_point['input'][index]
                self.nodes[node_index].value = self.functions[node_index](self.nodes[node_index].input)
            else:
                self.nodes[node_index].input = 1
                self.nodes[node_index].value = self.functions[node_index](self.nodes[node_index].input)
        self.fortrack_prediction(1)
        self.predictions[tuple(data_point['input'])] = self.nodes[-1].value

    # Backtrack, but forwards | back-wards <-> for-wards = back-track <-> for-track
    def fortrack_prediction(self, depth):
        # Depth First Recursion Iteration through nodes
        # Updating their prediction values along the way
        current_depth_nodes = [node.index for node in self.nodes if self.get_depth(node.index) == depth]
        for node_index in current_depth_nodes:
            self.nodes[node_index].input = self.get_node_input(node_index)
            self.nodes[node_index].value = self.functions[node_index](self.nodes[node_index].input)
        if len(self.nodes[node_index].children) > 0: # If not output node
            self.fortrack_prediction(depth + 1)

    def get_node_input(self, node_index):
        result = 0
        for parent in self.nodes[node_index].parents:
            result += self.weights[(parent, node_index)] * self.nodes[parent].value
        self.nodes[node_index].input = result
        return result
        
    def print_outputs(self, iteration):
        print('Iteration {}'.format(iteration))
        print('\tWeight Gradients (dE/w_xy): {}'.format(self.weight_gradients))
        print('\tNeuron Gradients (dE/n_x): {}'.format(self.neuron_gradients))
        print('\tIntermediate Neuron Gradients (dn_x/dn_y): {}'.format(self.intermediate_neuron_gradients))
        print('\tMisclassifications: {}'.format(list(self.misclassifications.values()).count(True)))
        print('\tPredictions: {}'.format(self.predictions))
        print('\tUpdated Weights: {}'.format(self.weights))

    def print_debugging_variables(self, data_point, edge, dE):
        print('\nedge', edge)
        print('\tdata_point', data_point['input'])
        print('\tdE', dE)
        print('\tmisclassifications', sum([1.0 for classification in self.misclassifications.values() if classification]))
        print('\tself.weight_gradients[edge]', self.weight_gradients[edge])