from neural_network_old import NeuralNetwork
import matplotlib.pyplot as plt

weights = {
    (0, 2): 1,
    (1, 2): 1
}

data_points = [
    {'input': [2, 3], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [1, 5], 'output': lambda pred: 0.0 if pred > 0 else pred},
    {'input': [0, 1], 'output': lambda pred: 0.0 if pred < 0 else pred}
]

nn = NeuralNetwork(weights, data_points=data_points, debug = True)

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.update_weights(print_output=True, iteration=i, plot=False)

    plot_boundry_line(nn)
    return nn

def boundry_line(weights, x):
  return - ((weights[(0, 2)] * weights[(2, 4)] + weights[(0, 3)] * weights[(3, 4)]) / (weights[(1, 2)] * weights[(2, 4)] + weights[(1, 3)] * weights[(3, 4)])) * x

def plot_boundry_line(nn):
    plt.plot([x / 100 for x in range(1000)], [boundry_line(nn.weights, x / 100) for x in range(1000)])
    
nn1 = run_neural_network(nn, 1)

plt.scatter([data_point['input'][0] for data_point in data_points], [data_point['input'][1] for data_point in data_points])
plt.axis([0.5, 4.5, 0.5, 4.5])
plt.savefig('images/neural_net.png')