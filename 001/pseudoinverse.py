import time
import numpy as np

points = [[0,0],[1,1],[2,4],[3,9]]


avg = []
for i in range(0,10):
    temp = time.time()
    x = np.array([[1,0],[1,1],[1,2],[1,3]])
    x_inverse = np.linalg.pinv(x)
    y = np.array([[0],[1],[4],[9]])
    beta = np.dot(x_inverse, y)
    avg.append(time.time() - temp)

print('python:', sum(avg) / 10)