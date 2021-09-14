import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph


class NeuralNetwork(NNDirectedWeightedGraph):
    def __init__(self, weights, data_points={}, alpha=0.001, debug=False):
        # Inhereit from a DirectedWeightedGraph to make the net
        super().__init__(weights=weights, vertex_values=sorted(set([_ for key in weights.keys() for _ in key]))) 
        self.alpha = alpha
        self.debug = debug
        self.data_points = data_points # Temporary
        self.set_weight_gradients()
        self.set_misclassifications() # Temporary
        self.set_predictions() # Temporary

    def set_weight_gradients(self):
        self.weight_gradients = {edge: 0.0 for edge in self.weights.keys()}

    def set_misclassifications(self):
        self.misclassifications = {tuple(data_point['input']): False for data_point in self.data_points}

    def set_predictions(self):
        self.predictions = {tuple(data_point['input']): 0.0 for data_point in self.data_points}

    def update_weights(self, print_output=False ,iteration=1, plot=False):
        for edge in self.weights.keys():
            alpha_times_delta_e = self.alpha * self.weight_gradients[edge] # Temporary
            self.weights[edge] -= alpha_times_delta_e # Descent `edge`'s Weight
        if print_output and (iteration < 6 or iteration % 100 == 0):
            self.print_outputs(iteration) # Self explainitory
        if not plot:
            self.set_weight_gradients()
            self.set_misclassifications() # Temporary
            self.set_predictions() # Temporary

    def compute_predictions(self, data_point):
        if not hasattr(self, 'paths'):
            self.paths = {index: self.get_every_possible_path_containing_index(index) for index in range(len(data_point['input']))}
        for input_index, value in enumerate(data_point['input']):
            if isinstance(self.paths[input_index], list):
                total_weight = 0
                for path in self.paths[input_index]:
                    total_weight += math.prod([self.weights[(path[i], path[i + 1])] for i in range(0, len(path) - 1)])
                self.paths[input_index] = float(total_weight)
                del total_weight
            self.predictions[tuple(data_point['input'])] += data_point['input'][input_index] * self.paths[input_index]
        if not data_point['output'](self.predictions[tuple(data_point['input'])]):
            self.predictions[tuple(data_point['input'])] = 0.0

    def update_weight_gradients(self, data_point, edge):
        dE = self.calc_dE(data_point, edge) # Calculate Gradient
        self.weight_gradients[edge] += dE # Update Gradient
        if self.predictions[tuple(data_point['input'])] != 0.0:
            self.misclassifications[tuple(data_point['input'])] = True
        if self.debug:
            self.print_debugging_variables(data_point, edge, pred, dE)
        self.set_node_values() # Reset the values, that are used for prediction, of all the nodes

    def calc_dE(self, data_point, edge):
        every_possible_path_containing_edge = self.get_every_possible_path_containing_edge(current_paths=[list(edge)])
        total_weight = 0
        for path in every_possible_path_containing_edge:
            total_weight += math.prod([self.weights[(path[i], path[i + 1])] for i in range(1, len(path) - 1)])
        return 2 * self.predictions[tuple(data_point['input'])] * total_weight * self.nodes[edge[0]].value
        
    def print_outputs(self, iteration):
        print('iteration {}'.format(iteration))
        print('\tgradient: {}'.format(self.weight_gradients))
        print('\tmisclassifications: {}'.format(list(self.misclassifications.values()).count(True)))
        print('\tpredictions: {}'.format(self.predictions))
        print('\tupdated weights: {}'.format(self.weights))

    def print_debugging_variables(self, data_point, edge, pred, dE):
        print('\nedge', edge)
        print('\tdata_point', data_point['input'])
        print('\tpred', pred)
        print('\t2 * pred', 2 * pred)
        print('\tself.nodes[edge[0]].value', self.nodes[edge[0]].value)
        print('\tdE', dE)
        print('\tmisclassifications', sum([1.0 for classification in self.misclassifications.values() if classification]))
        print('\tself.weight_gradients[edge]', self.weight_gradients[edge])