import filecmp

def neural_net_weights():
    #pain

neural_net_weights = generate_neural_net_weights()

neural_net_weights_file = open('genetic_algorithm/neural_net_weights.txt', 'w')

for board_state in neural_net_weights:
    string_board_state = '\n' + ''.join([str(space) for space in board_state])
    neural_net_weights_file.write(string_board_state)