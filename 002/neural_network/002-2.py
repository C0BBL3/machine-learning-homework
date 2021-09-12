from neural_network import NeuralNetwork
import matplotlib.pyplot as plt

weights = {
  (0,2): 1, 
  (1,2): 1
}

data_points = [
    {'input': [1, 4], 'output': lambda pred: pred >= 0},
    {'input': [1, 2], 'output': lambda pred: pred >= 0},
    {'input': [2, 2], 'output': lambda pred: pred >= 0},
    {'input': [2, 1], 'output': lambda pred: pred < 0},
    {'input': [3, 2], 'output': lambda pred: pred < 0},
    {'input': [4, 1], 'output': lambda pred: pred < 0}
]

nn = NeuralNetwork(weights, data_points=data_points, debug = False)

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for edge in weights.keys():
            for data_point in data_points:
                nn.update_weight_gradients(data_point, edge)
        nn.update_weights(print_output=False, iteration=i, plot=True)
        if list(nn.misclassifications.values()).count(True) < 1:
            break
        nn.set_misclassifications()
        nn.set_weight_gradients()
        nn.set_predictions()

    plot_boundry_line(nn)
    return nn

def boundry_line(weights, x):
  return -(weights[(0, 2)] / weights[(1, 2)]) * x

def plot_boundry_line(nn):
    for data_point in data_points:
        if data_point['output'] is (lambda pred: pred < 0):
            plt.plot([data_point['input'][0]], [data_point['input'][1]], 'ro')
        else:
            plt.plot([data_point['input'][0]], [data_point['input'][1]], 'bo')

    plt.plot([x / 100 for x in range(1000)], [boundry_line(nn.weights, x / 100) for x in range(1000)])
    plt.axis([0.5, 4.5, 0.5, 4.5])
    plt.savefig('neural_net.png')

nn1 = run_neural_network(nn, 40)

nn2 = run_neural_network(nn1, 20)

nn3 = run_neural_network(nn2, 856)