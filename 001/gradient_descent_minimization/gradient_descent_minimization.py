import time

avg = []
for i in range(10):
    start_time = time.time()

    derivatives = {'x': (lambda coords: 4 * coords['x']), 'y': (lambda coords: 6 * coords['y'])}
    best_coords = {'x': 0, 'y': 0} # f(x,y) = 1
    current_coords = {'x': 1, 'y': 2} # f(x,y) = 15

    def descend(current_coords, learning_rate = 0.001):
        new_coords = {cart: pos for cart, pos in current_coords.items()}
        for cart in current_coords.keys():
            new_coords[cart] -= derivatives[cart](current_coords) * learning_rate
        return new_coords

    def f(coords):
        return 1 + 2 * coords['x'] ** 2 + 3 * coords['y'] ** 2

    while f(current_coords) > f(best_coords): # or for _ in range(10000):
        current_coords = descend(current_coords)

    avg.append(time.time() - start_time)

print('Python:', sum(avg) / 10)