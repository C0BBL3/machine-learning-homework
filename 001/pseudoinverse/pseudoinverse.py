import time
import numpy as np

avg = []
for i in range(10):
    temp = time.time()

    points = [[0,0],[1,1],[2,4],[3,9]]
    x = np.array([[1,0],[1,1],[1,2],[1,3]])
    x_inverse = np.linalg.pinv(x)
    y = np.array([[0],[1],[4],[9]])
    beta = np.dot(x_inverse, y)

    avg.append(time.time() - temp)

print('Python:', sum(avg) / 10)