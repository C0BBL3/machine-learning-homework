import math
from nn_directed_weighted_graph import NNDirectedWeightedGraph
import numpy as np

class NeuralNetwork( NNDirectedWeightedGraph ):
    def __init__( self, weights, data_type = 'continuous', functions = None, derivatives = None, data_points = list(), alpha = 0.001, debug = False ):
        
        # Inhereit from a DirectedWeightedGraph to make the net
        node_indices = sorted( set( [ _ for key in weights.keys() for _ in key ] ) )
        super().__init__( weights = weights, vertex_values = node_indices ) 

        if functions is not None and derivatives is not None:

            self.functions = functions
            self.derivatives = derivatives

        else:

            self.functions = [ lambda x: x for _ in range( 0, len( node_indices ) ) ]
            self.derivatives = [ lambda x: 1 for _ in range( 0, len( node_indices ) ) ]
        
        self.alpha = alpha
        self.debug = debug
        self.data_points = data_points
        self.data_type = data_type
        self.set_gradients()
        self.set_predictions()

        if data_type == 'continuous':
            #stuff
            self.data_type = data_type
        elif data_type == 'discrete':
            #stuff
            self.set_misclassifications()

    def set_gradients( self ):
        
        self.weight_gradients = { edge: 0.0 for edge in self.weights.keys() }
        self.neuron_gradients = { node.index: 0.0 for node in self.nodes }
        self.intermediate_neuron_gradients = { edge: None for edge in self.weights.keys() }

    def set_misclassifications( self ):
        self.misclassifications = { tuple( data_point[ 'input' ] ): False for data_point in self.data_points }

    def set_predictions( self ):
        self.predictions = { tuple( data_point[ 'input' ] ): 0.0 for data_point in self.data_points }

    def update_weights( self, print_output = False, iteration = 1 ):

        new_weights = dict( self.weights )

        for edge in self.weights.keys():
            
            # Descent `edge`'s Weight
            new_weights[ edge ] -= self.alpha * self.weight_gradients[ edge ] 

        self.weights = dict( new_weights )
        new_weights = None
        del new_weights

        if print_output and ( iteration < 6 or iteration % 1000 == 0 ):

            self.print_outputs( iteration )

        self.set_gradients()
        self.set_predictions()

        if self.data_type == 'discrete':
            self.set_misclassifications()

    def update_neuron_gradients( self, data_point, node_index ):
        
        if self.data_type == 'continuous':

            prediction = self.predictions[ tuple( data_point[ 'input' ] ) ]

        else:

            prediction = data_point[ 'output' ]( self.predictions[ tuple( data_point[ 'input' ] ) ] )
        
        self.neuron_gradients[ node_index ] += 2.0 * prediction
        total_weight = 0.0
        every_possible_path_containing_edge = self.get_every_possible_path_containing_edge( current_paths = [ list( [ node_index ] ) ] )
        
        # Iterate through every path from the `node_index` to the ( or a ) output node
        for path in every_possible_path_containing_edge: 
            
            intermediate_neuron_gradients_along_path_temp = 1.0
            
            # Iterate through the current path
            for i in range( 0, len( path ) - 1 ): 

                # Get Current Edge
                edge = ( path[ i ], path[ i + 1 ] ) 
                
                if self.intermediate_neuron_gradients[ edge ] is None:
                
                    # Update Intermediate Neuron Gradients
                    self.intermediate_neuron_gradients[ edge ] = self.weights[ edge ] * self.derivatives[ path[ i ] ]( self.nodes[ path[ i + 1 ] ].input ) 
                    intermediate_neuron_gradients_along_path_temp *= self.intermediate_neuron_gradients[ edge ]
                
                else:
                    intermediate_neuron_gradients_along_path_temp *= self.intermediate_neuron_gradients[ edge ]

            total_weight += intermediate_neuron_gradients_along_path_temp
        
        # Update Neuron Gradients
        self.neuron_gradients[ node_index ] *= total_weight  

    def update_weight_gradients( self, data_point, edge ):
        
        # Calculate Gradient
        dE = self.calc_dE( data_point, edge ) 
        
        if self.data_type == 'discrete':

            prediction = data_point[ 'output' ]( self.predictions[ tuple( data_point[ 'input' ] ) ] )

            if self.data_type == 'continuous' and prediction != 0.0:
                
                self.misclassifications[ tuple( data_point[ 'input' ] ) ] = True

        self.weight_gradients[ edge ] += dE # Update Gradient
        
        if self.debug:
            self.print_debugging_variables( data_point, edge, dE )

    def calc_dE( self, data_point, edge ):
        return self.neuron_gradients[ edge[ 1 ] ] * self.derivatives[ edge[ 1 ] ]( self.nodes[ edge[ 1 ] ].input ) * self.nodes[ edge[ 0 ] ].value
        
    def calc_prediction( self, data_point, weights = list() ):
        
        # Start and Depth First Recursion Iteration through input nodes
        # Using recursion, Depth First search through the nodes
        # The output node( s )'s value is be the prediction( s )

        if weights != list():

            for i, edge in enumerate( self.weights.keys() ):

                self.weights[ edge ] = weights[ i ]

        current_depth_nodes = [ node.index for node in self.nodes if self.get_depth( node.index ) == 0 ]
        
        for index, node_index in enumerate( current_depth_nodes ):
            
            if index < len( data_point[ 'input' ] ):
                
                self.nodes[ node_index ].input = data_point[ 'input' ][ index ]
                self.nodes[ node_index ].value = self.functions[ node_index ]( self.nodes[ node_index ].input )
            
            else:
                
                self.nodes[ node_index ].input = 1
                self.nodes[ node_index ].value = self.functions[ node_index ]( self.nodes[ node_index ].input )
        
        self.evaluate_prediction( 1 )
        self.predictions[ tuple( data_point[ 'input' ] ) ] = self.nodes[ -1 ].value
        
        return self.nodes[ -1 ].value

    def evaluate_prediction( self, depth ):
        
        # Depth First Recursion Iteration through nodes
        # Updating their prediction values along the way
        
        current_depth_nodes = [ node.index for node in self.nodes if self.get_depth( node.index ) == depth ]
        
        for node_index in current_depth_nodes:
            
            self.nodes[ node_index ].input = self.get_node_input( node_index )
            self.nodes[ node_index ].value = self.functions[ node_index ]( self.nodes[ node_index ].input )
        
        # If not output node
        if len( self.nodes[ current_depth_nodes[ -1 ] ].children ) > 0: 
            
            self.evaluate_prediction( depth + 1 )

    def mitosis( self ):

        new_weights = dict()

        for edge, weight in self.weights.items():

            new_weights[ edge ] = weight - self.alpha * np.random.normal(0, 1)

        new_alpha = self.alpha * math.e ** ( np.random.normal( 0, 1 ) / ( 2 ** 0.5 * len( new_weights ) ** 0.25 ) )
        
        return NeuralNetwork(
            new_weights, 
            functions = self.functions, 
            derivatives = self.derivatives,
            alpha = new_alpha
        )

    def get_node_input( self, node_index ):
        
        result = 0

        if self.nodes[ node_index ].parents == list():
            self.nodes[ node_index ].input = 1
            return 1
        
        for parent in self.nodes[ node_index ].parents:
            
            result += self.weights[ ( parent, node_index ) ] * self.nodes[ parent ].value
        
        self.nodes[ node_index ].input = result
        
        return result
        
    def print_outputs( self, iteration ):
        print( 'Iteration {}'.format( iteration ) )
        print( '\tWeight Gradients ( dE/w_xy ): {}'.format( self.weight_gradients ) )
        print( '\tNeuron Gradients ( dE/n_x ): {}'.format( self.neuron_gradients ) )
        print( '\tIntermediate Neuron Gradients ( dn_x/dn_y ): {}'.format( self.intermediate_neuron_gradients ) )
        print( '\tMisclassifications: {}'.format( list( self.misclassifications.values() ).count( True ) ) )
        print( '\tPredictions: {}'.format( self.predictions ) )
        print( '\tUpdated Weights: {}'.format( self.weights ) )

    def print_debugging_variables( self, data_point, edge, dE ):
        print( '\nedge', edge )
        print( '\tdata_point', data_point[ 'input' ] )
        print( '\tdE', dE )
        print( '\tmisclassifications', sum( [ 1.0 for classification in self.misclassifications.values() if classification ] ) )
        print( '\tself.weight_gradients[ edge ]', self.weight_gradients[ edge ] )