import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph


class NeuralNetwork(NNDirectedWeightedGraph):
    def __init__(self, weights, alpha=0.001, debug=False):
        self.alpha = alpha
        self.debug = debug
        super().__init__(weights=weights, vertex_values=sorted(set([_ for key in weights.keys() for _ in key])))
        self.set_weight_gradients()
        
    def set_weight_gradients(self):
        self.weight_gradients = {edge: 0 for edge in self.weights.keys()}

    def update_weights(self):
        for edge in self.weights.keys():
            self.weights[edge] -= self.alpha * self.weight_gradients[edge]
        #self.set_weight_gradients()

    def update_weight_gradients(self, data_point, edge):
        dE, pred = self.calc_dE(data_point, edge)
        self.weight_gradients[edge] += dE
        if self.debug:
            print('\nedge', edge)
            print('\tdata_point', data_point['input'])
            print('\tpred', pred)
            print('\tdE', dE) 
            print('\tself.weight_gradients[edge]', self.weight_gradients[edge])
        self.set_node_values()

    def calc_dE(self, data_point, edge):
        pred = self.calc_prediction(data_point)
        return 2 * pred * self.nodes[edge[0]].value, pred

    def calc_prediction(self, data_point):
        for index, value in enumerate(data_point['input']):
            self.nodes[index].value = value
            self.fortrack_prediction(index, value)
        # Hopefully should be the output's prediction
        pred = self.nodes[-1].value
        if data_point['output'](pred): return 0
        else: return pred

    def fortrack_prediction(self, index, value):
        current_node_children = self.nodes[index].children
        if len(current_node_children) > 0:
            for child_index in current_node_children:
                self.nodes[child_index].value += value * self.weights[(index, child_index)]
                self.fortrack_prediction(child_index, value)

    def get_node_input(self, index):
        return [parent_index for parent_index in self.nodes[index].parents]
