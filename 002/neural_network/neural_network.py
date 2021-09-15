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
        self.set_predictions()

    def set_weight_gradients(self):
        self.weight_gradients = {edge: 0.0 for edge in self.weights.keys()}

    def set_misclassifications(self):
        self.misclassifications = {tuple(data_point['input']): False for data_point in self.data_points}

    def set_predictions(self):
        self.predictions = {tuple(data_point['input']): 0.0 for data_point in self.data_points}

    def update_weights(self, print_output=False, iteration=1):
        for edge in self.weights.keys():
            self.weights[edge] -= self.alpha * self.weight_gradients[edge] # Descent `edge`'s Weight
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
        return 2 * data_point['output'](self.predictions[tuple(data_point['input'])]) * self.nodes[edge[0]].value
        
    def calc_prediction(self, data_point):
        # Start and Iterate through input nodes
        # Using recursion, iterate through the input nodes' children and the children's children
        # The output node(s)'s value should be the prediction if Python isn't bad
        for index, value in enumerate(data_point['input']):
            self.nodes[index].value = value
            self.fortrack_prediction(index, value)
        self.predictions[tuple(data_point['input'])] = self.nodes[-1].value

    # Backtrack, but forwards | back-wards <-> for-wards = back-track <-> for-track
    def fortrack_prediction(self, index, value): 
        # Recursive iteration through the nodes
        # Updating their predictionvalues along the way
        if len(self.nodes[index].children) > 0: # If not output node
            for child_index in self.nodes[index].children:
                self.nodes[child_index].value += value * self.weights[(index, child_index)]
                self.nodes[child_index].predicted_count += 1
            for child_index in self.nodes[index].children:
                if self.nodes[child_index].predicted_count == len(self.nodes[child_index].parents):
                    self.fortrack_prediction(child_index, self.nodes[child_index].value)

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