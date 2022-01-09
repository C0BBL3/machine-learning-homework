import tensorflow as tf # Import tensorflow library
import matplotlib.pyplot as plt # Import matplotlib library
import numpy as np # Import numpy library
from principal_component_analysis import PrincipalComponentAnalysis

precision = 0.01

mnist = tf.keras.datasets.mnist # Object of the MNIST dataset
(x_train, y_train),(x_test, y_test) = mnist.load_data() # Load data
print('start')
import time
start = time.time()

def remove_zeros(x):
    if x == 0:
        return precision
    else:
        return x

remove_zeros_v = np.vectorize(remove_zeros)

x_train_new = np.apply_along_axis(lambda image: remove_zeros_v(image).flatten(), 0, x_train[0:100])
print('x_train_new', x_train_new)

PCA = PrincipalComponentAnalysis()
PCA.fit(x_train_new)
print('transformed_data', PCA.transformed_data)

print('total time', time.time() - start)

x_test_new = np.apply_along_axis(lambda image: remove_zeros_v(image).flatten(), 1, x_test[0:100])
print('x_test_new', x_test_new)
