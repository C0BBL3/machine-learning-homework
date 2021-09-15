from neural_network import NeuralNetwork
import matplotlib.pyplot as plt

weights = {
    (3, 4): -0.1,
    (2, 4): 0.2,
    (1, 3): -0.3,
    (0, 3): 0.4,
    (1, 2): -0.5,
    (0, 2): 0.6
}

data_points = [
    {'input': [1, 4], 'output': lambda pred: 0.0 if pred >= 0 else pred},
    {'input': [1, 2], 'output': lambda pred: 0.0 if pred >= 0 else pred},
    {'input': [2, 2], 'output': lambda pred: 0.0 if pred >= 0 else pred},
    {'input': [2, 1], 'output': lambda pred: 0.0 if pred < 0 else pred},
    {'input': [3, 2], 'output': lambda pred: 0.0 if pred < 0 else pred},
    {'input': [4, 1], 'output': lambda pred: 0.0 if pred < 0 else pred}
]

nn = NeuralNetwork(weights, data_points=data_points, debug = False)

def run_neural_network(nn, iterations = 10 ** 10):
    i = 1
    while True:
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1 or i > iterations:
            break
        nn.update_weights(print_output=False, iteration=i)
        i += 1

    plot_boundry_line(nn)
    return nn

def boundry_line(weights, x):
  return ((weights[(0, 2)] * weights[(2, 4)] + weights[(0, 3)] * weights[(3, 4)]) / (weights[(1, 2)] * weights[(2, 4)] + weights[(1, 3)] * weights[(3, 4)])) * -1 *  x

def plot_boundry_line(nn):
    plt.plot([x / 100 for x in range(1000)], [boundry_line(nn.weights, x / 100) for x in range(1000)])
    
nn1 = run_neural_network(nn, 2373)

plt.scatter([data_point['input'][0] for data_point in data_points], [data_point['input'][1] for data_point in data_points])
plt.axis([0.5, 4.5, 0.5, 4.5])
plt.savefig('neural_net.png')