import time
import numpy as np

avg = []
for i in range(10):
    start_time = time.time()

    x = np.array([[0,1],[1,1],[2,1],[3,1]])
    x_inverse = np.linalg.pinv(x)
    y = np.array([[0],[1],[4],[9]])
    beta = np.dot(x_inverse, y)

    avg.append(time.time() - start_time)

print('Python:', sum(avg) / 10)