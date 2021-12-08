#\left[\left(1,1.5\right),\left(2,2\right),\left(3,3\right),\left(4,\ 4\right),\left(5,5.5\right)\right]

import sys
sys.path.append('neural_network')
from neural_network import NeuralNetwork
import math
import numpy as np

RSS = lambda a,b: (a*b**(1)-1.5) ** 2 + (a*b**(2)-2) ** 2 + (a*b**(3)-3) ** 2 + (a*b**(4)-4) ** 2 + (a*b**(5)-5.5) ** 2
dRSSda = lambda a,b: 2*a*b**(10) + 2*a*b**8 + 2*a*b**6 - 11*b**5 + 2*a*b**4 - 8*b**4 - 6*b**3 + 2*a*b**2 - 4*b**2 - 3*b
dRSSdb = lambda a,b: 10*(a**2)*(b**9) + 8*(a**2)*(b**7) + 6*(a**2)*(b**5) - 55*a*(b**4) + 4*(a**2)*(b**3) - 32*a*(b**3) - 18*a*(b**2) + 2*(a**2)*b - 8*a*b - 3*a

print('\n1, pseudoinverse')
data = [(1,1.5), (2,2), (3,3), (4,4), (5,5.5)]

x = np.array([[1,math.log(1)],[1,math.log(2)],[1,math.log(3)],[1,math.log(4)],[1,math.log(5)]])
x_inverse = np.linalg.pinv(x)
y = np.array([[math.log(1.5)],[math.log(2)],[math.log(3)],[math.log(4)],[math.log(5.5)]])
beta = np.dot(x_inverse, y)

print('\nuntransformed\n', beta)
a = float(beta[0])
b = float(beta[1])
print('RSS', RSS(a,b))

print('\n2, guess')
print('RSS with a=1.1 and b = 1.4', RSS(1.1, 1.4))

print('\n3, gradient descent')

ta = 1.1
b = 1.4

print('\nRSS initial from b_0 = 1.1, b_1 = 1.4:', RSS(a,b))

for i in range(20000):
    da = dRSSda(a,b)
    db = dRSSdb(a,b)
    a -= 0.0001 * da
    b -= 0.0001 * db
    rss = RSS(a,b)

print('RSS final from b_0 = 1.1, b_1 = 1.4:', RSS(a,b))
print('Final a: {}, Final b: {}'.format(a,b))

a, b = float(beta[0]), float(beta[1])
temp_a, temp_b = float(beta[0]), float(beta[1])
print('\nRSS initial from b_0 = {}, b_1 = {}:'.format(temp_a,temp_b), RSS(a,b))

for i in range(20000):
    da = dRSSda(a,b)
    db = dRSSdb(a,b)
    a -= 0.0001 * da
    b -= 0.0001 * db
    rss = RSS(a,b)

print('RSS final from b_0 = {}, b_1 = {}:'.format(temp_a, temp_b), RSS(a,b))
print('Final a: {}, Final b: {}'.format(a,b), '\n')