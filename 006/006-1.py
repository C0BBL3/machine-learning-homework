import sys
sys.path.append('neural_network')
from neural_network import NeuralNetwork
import math
import numpy as np

RSS = lambda a,b: (a*(1)**b-1) ** 2 + (a*(2)**b-2) ** 2 + (a*(3)**b-9) ** 2 + (a*(4)**b-16) ** 2
dRSSda = lambda a,b: 2*(a-1) + (2**(1+b))*((2**b)*a-2) + 2*(a*(3**b)-9)*(3**b) + (2**(1+2*b))*((4**b)*a-16)
dRSSdb = lambda a,b: math.log(2)*(2**(1+b))*a*((2**b)*a-2) + 2*(a*(3**b)-9)*math.log(3)*(3**b)*a + math.log(2)*(2**(2+2*b))*a*((4**b)*a-16) 

print('\n1, pseudoinverse')
data = [(1,1), (2,2), (3,9), (4,16)]

x = np.array([[1,math.log(1)],[1,math.log(2)],[1,math.log(3)],[1,math.log(4)]])
x_inverse = np.linalg.pinv(x)
y = np.array([[math.log(1)],[math.log(2)],[math.log(9)],[math.log(16)]])
beta = np.dot(x_inverse, y)

print('\nuntransformed\n', beta)
a = float(beta[0])
b = float(beta[1])
print('RSS', RSS(a,b))

beta[0] = math.e ** (beta[0])

print('transformed\n', beta)
a = float(beta[0])
b = float(beta[1])
print('RSS', RSS(a,b))

print('')

print('\n2, guess')
print('RSS with a=1 and b = 1', RSS(1, 1))

print('\n3, gradient descent')

a = 1
b = 1

print('\nRSS initial from b_0 = 1, b_1 = 1:', RSS(a,b))

for i in range(20000):
    da = dRSSda(a,b)
    db = dRSSdb(a,b)
    a -= 0.0001 * da
    b -= 0.0001 * db
    rss = RSS(a,b)

print('RSS final from b_0 = 1, b_1 = 1:', RSS(a,b))
print('Final a: {}, Final b: {}'.format(a,b))

temp_a, temp_b = a, b
print('\nRSS initial from b_0 = {}, b_1 = {}:'.format(a,b), RSS(a,b))

for i in range(20000):
    da = dRSSda(a,b)
    db = dRSSdb(a,b)
    a -= 0.0001 * da
    b -= 0.0001 * db
    rss = RSS(a,b)

print('RSS final from b_0 = {}, b_1 = {}:'.format(temp_a, temp_b), RSS(a,b))
print('Final a: {}, Final b: {}'.format(a,b), '\n')