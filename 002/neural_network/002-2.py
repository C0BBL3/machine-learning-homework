from neural_network import NeuralNetwork

weights = {(0,2): 1, (1,2): 1}
linear_function = lambda x: x
linear_derivative = lambda x: 1

activation_types = ['linear', 'linear', 'linear']
activation_functions = {
    'linear': {
        'function': linear_function,
        'derivative': linear_derivative
    }
}

nn = NeuralNetwork(weights, activation_types, activation_functions)
data_points = [[1,4], [1,2], [2,2], [2,1], [3,2], [4,1]]

for i in range(1,1001):
    for edge in weights.keys():
        for data_point in data_points:
            nn.update_weight_gradients(data_point, edge)
    nn.update_weights()
    if i < 5 or i % 1000 == 0:
            print('iteration {}'.format(i))
            print('\tgradient: {}'.format(nn.weight_gradients))
            print('\tupdated weights: {}'.format(nn.weights))
            print()
    nn.set_weight_gradients()
        