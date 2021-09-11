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

nn = NeuralNetwork(weights, data_points=data_points, debug = False)

def print_outputs(i, temp, nn):
    print('iteration {}'.format(i))
    print('\tgradient: {}'.format(nn.weight_gradients))
    print('\tmisclassifications: {}'.format(temp))
    print('\tupdated weights: {}'.format(nn.weights))
    print()

i = 0
while True:
    for edge in weights.keys():
        for data_point in data_points:
            nn.update_weight_gradients(data_point, edge)
    nn.update_weights()
    temp = list(nn.misclassifications.values()).count(True)
    if i < 6 or i % 100 == 0:
        print_outputs(i, temp, nn)
    if temp < 1 or i > 1000:
        print_outputs(i, temp, nn)
        break
    nn.set_weight_gradients()
    nn.set_misclassifications()
    i += 1
