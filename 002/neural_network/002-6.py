from neural_network import NeuralNetwork
import matplotlib.pyplot as plt
import math

weights = {
    (0, 3): -1,
    (1, 3): 1,
    (2, 3): 0
}

activation_functions = [
    lambda x: math.atan(x),
    lambda x: math.atan(x),
    lambda x: math.atan(x),
    lambda x: math.atan(x)
]

data_points = [
    {'input': [0, 3], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [2, 3], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [0, 1], 'output': lambda pred: 0.0 if pred < 0 else pred},
    {'input': [2, 1], 'output': lambda pred: 0.0 if pred < 0 else pred}
]

nn = NeuralNetwork(weights, activation_functions, bias = True, data_points=data_points, debug = True)

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.update_weights(print_output=True, iteration=i)

nn1 = run_neural_network(nn, 1)