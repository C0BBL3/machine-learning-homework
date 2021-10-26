import math
import random

def generate_graph(center, deviation, num_of_points): # (1,3), 3, 50
    xs = [center[0] + random.randint(-deviation * 100, deviation * 100) / 100 for _ in range(num_of_points)]
    ys = [center[1] + random.randint(-deviation * 100, deviation * 100) / 100 for _ in range(num_of_points)]
    return xs, ys

import matplotlib.pyplot as plt

oneone = generate_graph((1,1), 1.25, 50)
onethree = generate_graph((1,3), 1.25, 50)
threeone = generate_graph((3,1), 1.25, 50)
threethree = generate_graph((3,3), 1.25, 50)

plt.scatter(oneone[0], oneone[1], color='red')
plt.scatter(onethree[0], onethree[1], color='blue')
plt.scatter(threeone[0], threeone[1], color='blue')
plt.scatter(threethree[0], threethree[1], color='red')
#plt.axis([-1, 5, -1, 5])
plt.savefig('data.png')