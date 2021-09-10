from neural_network import NeuralNetwork

weights = {
  (0,2): 1,
  (0,3): 1,
  (0,4): 1,
  (1,2): 1,
  (1,3): 1,
  (1,4): 1,
  (2,5): 1,
  (2,6): 1,
  (2,7): 1,
  (3,5): 1,
  (3,6): 1,
  (3,7): 1,
  (4,5): 1,
  (4,6): 1,
  (4,7): 1,
  (5,8): 1,
  (5,9): 1,
  (5,10): 1,
  (6,8): 1,
  (6,9): 1,
  (6,10): 1,
  (7,8): 1,
  (7,9): 1,
  (7,10): 1,
  (8,11): 1,
  (9,11): 1,
  (10,11): 1,
}
nn = NeuralNetwork(weights)
data_points = [
    {'input': [1, 4], 'output': lambda pred: pred > 0},
    {'input': [1, 2], 'output': lambda pred: pred > 0},
    {'input': [2, 2], 'output': lambda pred: pred > 0},
    {'input': [2, 1], 'output': lambda pred: pred < 0},
    {'input': [3, 2], 'output': lambda pred: pred < 0},
    {'input': [4, 1], 'output': lambda pred: pred < 0}
]

for i in range(1, 20001):
    for edge in weights.keys():
        for data_point in data_points:
            nn.update_weight_gradients(data_point, edge)
    nn.update_weights()
    if i < 6 or i % 1000 == 0:
        print('iteration {}'.format(i))
        print('\tgradient: {}'.format(nn.weight_gradients))
        print('\tupdated weights: {}'.format(nn.weights))
        print()
    nn.set_weight_gradients()
