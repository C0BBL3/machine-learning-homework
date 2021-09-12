from neural_network import NeuralNetwork

weights = {
    (0, 2): 1,
    (1, 2): 1,
    (0, 3): 1,
    (1, 3): 1,
    (2, 4): 1,
    (3, 4): 1
}

data_points = [
    {'input': [1, 4], 'output': lambda pred: pred >= 0},
    {'input': [1, 2], 'output': lambda pred: pred >= 0},
    {'input': [2, 2], 'output': lambda pred: pred >= 0},
    {'input': [2, 1], 'output': lambda pred: pred < 0},
    {'input': [3, 2], 'output': lambda pred: pred < 0},
    {'input': [4, 1], 'output': lambda pred: pred < 0}
]

nn = NeuralNetwork(weights, data_points=data_points, debug=True)

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        nn.update_weights(print_output=False, iteration=i, plot=True)
        if list(nn.misclassifications.values()).count(True) < 1:
            break

run_neural_network(nn, 32)

run_neural_network(nn, 1)

run_neural_network(nn, 1)

run_neural_network(nn, 1)