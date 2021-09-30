from neural_network import NeuralNetwork

weights = {
    (3, 4): -0.1,
    (2, 4): 0.2,
    (1, 3): -0.3,
    (0, 3): 0.4,
    (1, 2): -0.5,
    (0, 2): 0.6
}

data_points = [
    {'input': [1, 4], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [1, 2], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [2, 2], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [2, 1], 'output': lambda pred: 0.0 if pred < 0 else pred},
    {'input': [3, 2], 'output': lambda pred: 0.0 if pred < 0 else pred},
    {'input': [4, 1], 'output': lambda pred: 0.0 if pred < 0 else pred}
]

nn = NeuralNetwork(weights, data_points=data_points, debug = False)

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.update_weights(print_output=True, iteration=i)

nn1 = run_neural_network(nn, 3)