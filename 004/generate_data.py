import math
import random
import numpy as np
import pandas as pd

def generate_graph(center, deviation, num_of_points): # (1,3), 3, 50
    xs = [center[0] + random.randint(-deviation * 100, deviation * 100) / 100 for _ in range(num_of_points)]
    ys = [center[1] + random.randint(-deviation * 100, deviation * 100) / 100 for _ in range(num_of_points)]
    return xs, ys

def correct_data(data, labels): # data = [[(1,1),(1,1.3),...], [(3,1),(3,1.3),...],...] labels = [1,0...]
    data_2 = []
    for group in data:
        for element in group:
            data_2.append(element)
    corrected_data = np.array(data_2)
    labels_2 = []
    for i, label in enumerate(labels):
        for _ in range(len(data[i])):
            labels_2.append(label)
    corrected_labels = np.array(labels_2)
    return corrected_data, corrected_labels

#import matplotlib.pyplot as plt

#oneone = generate_graph((1,1), 1.25, 50)
#onethree = generate_graph((1,3), 1.25, 50)
#threeone = generate_graph((3,1), 1.25, 50)
#threethree = generate_graph((3,3), 1.25, 50)

#plt.scatter(oneone[0], oneone[1], color='red')
#plt.scatter(onethree[0], onethree[1], color='blue')
#plt.scatter(threeone[0], threeone[1], color='blue')
#plt.scatter(threethree[0], threethree[1], color='red')
#plt.axis([-1, 5, -1, 5])
#plt.savefig('data.png')