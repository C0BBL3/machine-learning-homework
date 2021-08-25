import time

avg = []
for i in range(10):
    start_time = time.time()

    array =  [[1, 0, 0], [1, 1, 1],  [1, 2, 4]]
    x = [[0, 1], [1, 1], [2, 1]]
    y = [[0], [1], [4]]

    coeffs = {'beta_0': 0, 'beta_1': 2}
    coeff_order = ["beta_0", "beta_1"]

    def regression_function(coeffs, inputs):
        return sum([coeffs[coeff] * term for (coeff, term) in zip(coeff_order, inputs)])

    def rss(coeffs):
        return sum([(regression_function(coeffs, row[:len(y) - 1]) - row[len(y) - 1]) ** 2 for row in array]) 

    def calc_gradient(coeffs, learning_rate = 0.001):
        gradient = {}
        temp = {beta: coeff for beta, coeff in coeffs.items()}
        for beta in coeffs.keys():
            temp[beta] += learning_rate
            plus_prediction = rss(temp)
            temp[beta] -= 2 * learning_rate
            minus_prediction = rss(temp)
            temp[beta] += learning_rate
            gradient[beta] = (plus_prediction - minus_prediction) / (2 * learning_rate)
        return gradient

    def descend(coeffs, learning_rate = 0.001):
        new_coeffs = {beta: coeff for beta, coeff in coeffs.items()}
        gradient = calc_gradient(coeffs, learning_rate)
        for beta in coeffs.keys():
            new_coeffs[beta] -= gradient[beta] * learning_rate
        return new_coeffs

    for _ in range(10000):
        coeffs = descend(coeffs)

    avg.append(time.time() - start_time)

print('Python:', sum(avg) / 10)