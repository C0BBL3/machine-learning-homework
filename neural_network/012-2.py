import math
import sys
from generate_weights import generate_weights
from neural_network import NeuralNetwork

def tanh( x ):
    numerator = math.e ** x - math.e ** ( - x )
    denominator = math.e ** x + math.e ** ( - x )
    return numerator / denominator

def sech( x ):
    denominator = math.e ** x + math.e ** ( - x )
    return 2 / denominator

dataset = [
    ( 0.0 , 0.7 ), 
    ( 0.2 , 0.56 ), 
    ( 0.4 , 0.356 ), 
    ( 0.6 , 0.123 ), 
    ( 0.8 , -0.103 ),
    ( 1.0 , -0.289 ), 
    ( 1.2 , -0.406 ), 
    ( 1.4 , -0.439 ), 
    ( 1.6 , -0.388 ), 
    ( 1.8 , -0.264 ),
    ( 2.0 , -0.092 ), 
    ( 2.2 , 0.095 ), 
    ( 2.4 , 0.263 ), 
    ( 2.6 , 0.379 ), 
    ( 2.8 , 0.422 ),
    ( 3.0 , 0.38 ), 
    ( 3.2 , 0.256 ), 
    ( 3.4 , 0.068 ), 
    ( 3.6 , -0.158 ), 
    ( 3.8 , -0.384 ),
    ( 4.0 , -0.576 ), 
    ( 4.2 , -0.701 ), 
    ( 4.4 , -0.738 ), 
    ( 4.6 , -0.676 ), 
    ( 4.8 , -0.522 )
]

dataset = [ 
    { 
        'input': [ data[ 0 ] ], 
        'output': data[ 1 ] 
    }  
    for data in dataset
]

neural_networks = list()
total_rss = []
worst_nn = None
best_nn = None

for _ in range( 30 ):

    weights = generate_weights(
        [1, 10, 6, 3, 1], 
        random_bool = True, 
        random_range = [ -0.2, 0.2 ],
        layers_with_bias_nodes = [0, 1, 2, 3]
    )

    activation_functions = [ 
        tanh 
        for _ in range( len( weights ) )
    ]

    activation_function_derivatives = [
        lambda x: sech(x) ** 2 
        for _ in range( len( weights ) )
    ]

    nn = NeuralNetwork(
        weights, 
        functions = activation_functions, 
        derivatives = activation_function_derivatives,
        alpha = 0.01
    )

    neural_networks.append( { 'neural network': nn, 'rss': 0 } )

for i in range( 1, 1001 ):

    if i % 100 == 0 or i < 6:
        print('\nIteration:', i)

    for nn in neural_networks:

        for data_point in dataset:

            prediction = nn[ 'neural network' ].calc_prediction( data_point )
            nn[ 'rss' ] += ( prediction - data_point[ 'output' ] ) ** 2

    total_rss.append(
        sum( 
            [ 
                nn[ 'rss' ] / len( neural_networks )
                for nn in neural_networks
            ] 
        )
    )

    neural_networks = sorted(
        neural_networks, 
        key = lambda nn: nn[ 'rss' ], 
        reverse = True 
    )

    if i == 1: worst_nn = neural_networks[ -1 ]
    if i == 1000: best_nn = neural_networks[ 0 ]

    neural_networks = [ 
        {
            'neural network': nn[ 'neural network' ], 
            'rss': 0 
        } 
        for nn in neural_networks[ 15 : ]
    ]

    neural_networks += [ 
        {
            'neural network': nn[ 'neural network' ].mitosis(), 
            'rss': 0 
        } 
        for nn in neural_networks 
    ]

import matplotlib.pyplot as plt

plt.plot( list( range( 1000 ) ), total_rss )
plt.savefig('images/012-2-1.png')
plt.clf()

def run_neural_network(nn, iterations):
    for i in range(1, iterations + 1):
        for data_point in dataset:
            nn.calc_prediction(data_point)
            for node in nn.nodes[::-1]:
                nn.update_neuron_gradients(data_point, node.index)
            for edge in nn.weights.keys():
                nn.update_weight_gradients(data_point, edge)
        nn.update_weights(print_output=False, iteration=i)
    return nn

fitted_nn = NeuralNetwork(
    best_nn[ 'neural network' ].weights, 
    functions = best_nn[ 'neural network' ].functions, 
    derivatives = best_nn[ 'neural network' ].derivatives,
    alpha = 0.01
)

fitted_nn = run_neural_network(fitted_nn, 20000)

xs = []
ys = []
ys_1 = []
ys_2 = []
ys_3 = []

for data in dataset:
    xs.append( data[ 'input' ][ 0 ] )
    ys.append( data[ 'output' ] )
    ys_1.append( worst_nn[ 'neural network' ].calc_prediction( data ) )
    ys_2.append( best_nn[ 'neural network' ].calc_prediction( data ) )
    ys_3.append( fitted_nn.calc_prediction( data ) )

plt.scatter(xs, ys)
plt.plot(xs, ys_1)
plt.plot(xs, ys_2)
plt.plot(xs, ys_3)
plt.legend( [ 'Data Points', 'Worst Neural Network', 'Best Neural Network', 'Fitted Neural Network' ] )
plt.savefig('images/012-2-2.png')