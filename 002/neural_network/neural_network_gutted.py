import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph


class NeuralNetwork(NNDirectedWeightedGraph):
    def __init__(self, weights, alpha=0.001):
        super().__init__(weights=weights, vertex_values=sorted(set([_ for key in weights.keys() for _ in key])))
        self.alpha = alpha
        self.set_weight_gradients()

    def set_weight_gradients(self):
        self.weight_gradients = {edge: 0.0 for edge in self.weights.keys()}

    def update_weights(self):
        for edge in self.weights.keys():
            self.weights[edge] -= self.alpha * self.weight_gradients[edge]  # Descend `edge`'s Weight

    def update_weight_gradients(self, data_point, edge):
        dE = self.calc_dE(data_point, edge)
        self.weight_gradients[edge] += dE
        self.set_node_values()

    def calc_dE(self, data_point, edge):
        every_possible_path_containing_edge = self.get_every_possible_path_containing_edge(current_paths=[list(edge)])
        total_weight = 0
        for path in every_possible_path_containing_edge:
            total_weight += math.prod([self.weights[(path[i], path[i + 1])] for i in range(1, len(path) - 1)])
        return 2 * self.calc_prediction(data_point) * total_weight * self.nodes[edge[0]].value

    def calc_prediction(self, data_point):
        for index, value in enumerate(data_point['input']):
            self.nodes[index].value = value
            self.fortrack_prediction(index, value)
        return self.classify(data_point)

    def fortrack_prediction(self, index, value):
        current_node_children = self.nodes[index].children
        if len(current_node_children) > 0.0:
            for child_index in current_node_children:
                self.nodes[child_index].value += value * self.weights[(index, child_index)]
                self.fortrack_prediction(child_index, value)

    def classify(self, data_point):
        pred = float(self.nodes[-1].value)
        self.nodes[-1].value = 0.0
        if data_point['output'](pred):
            self.nodes[-1].value = 0.0
            return 0.0
        else:
            return float(pred)
