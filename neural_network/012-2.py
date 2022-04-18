import math
import sys
from generate_weights import generate_weights
from neural_network import NeuralNetwork

def tanh( x ):
    e_x = math.e ** x
    e_neg_x = math.e ** ( - x )
    numerator = e_x - e_neg_x
    denominator = e_x + e_neg_x
    return numerator / denominator

def sech( x ):
    e_x = math.e ** x
    e_neg_x = math.e ** ( - x )
    denominator = e_x + e_neg_x
    return 2 / denominator

dataset = [ 
    (0.0 , 7.0), 
    (0.2 , 5.6), 
    (0.4 , 3.56), 
    (0.6 , 1.23), 
    (0.8 , -1.03),
    (1.0 , -2.89),
    (1.2 , -4.06), 
    (1.4 , -4.39), 
    (1.6 , -3.88), 
    (1.8 , -2.64), 
    (2.0 , -0.92), 
    (2.2 , 0.95), 
    (2.4 , 2.63), 
    (2.6 , 3.79), 
    (2.8 , 4.22),
    (3.0 , 3.8), 
    (3.2 , 2.56), 
    (3.4 , 0.68), 
    (3.6 , -1.58), 
    (3.8 , -3.84), 
    (4.0 , -5.76), 
    (4.2 , -7.01), 
    (4.4 , -7.38), 
    (4.6 , -6.76), 
    (4.8 , -5.22) 
]

max_x = abs ( 
        max( 
        dataset, 
        key = lambda data: abs( data[ 0 ] )
    ) [ 1 ]
)

max_y = abs ( 
        max( 
        dataset, 
        key = lambda data: abs( data[ 1 ] )
    ) [ 1 ]
)

dataset = [ 
    { 
        'input': [ data[0] / max_x ], 
        'output': data[1] / max_y 
    }  
    for data in dataset
]

neural_networks = list()
total_rss = []
worst_nn = None
best_nn = None

for _ in range( 30 ):

    weights = generate_weights(
        [1, 6, 6, 6, 6, 6, 1], 
        random_bool = True, 
        random_range = [ -1, 1 ],
        layers_with_bias_nodes = [True, True, True, True, True, False]
    )

    activation_functions = [ lambda x: x ] + [ 
        tanh 
        for _ in range( len( weights ) - 2 )
    ] + [ lambda x: x ]

    activation_function_derivatives = [lambda x: 1 ] + [
        lambda x: sech(x) ** 2 
        for _ in range( len( weights ) - 2 )
    ] + [ lambda x: 1 ]

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
    
plt.scatter(xs, ys)
plt.plot(xs, ys_1)
plt.plot(xs, ys_2)
plt.legend( [ 'Data Points', 'Worst Neural Network', 'Best Neural Network'] )
plt.savefig('images/012-2-2.png')
plt.clf()
