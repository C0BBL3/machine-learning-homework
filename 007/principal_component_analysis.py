import numpy as np
import math

class PrincipalComponentAnalysis:
    def __init__(self, data):
        self.data = np.array(data)
        self.transposed_data = self.data.T
        self.dimensions = len(data[0])
        self.correlation_matrix = []

    def correlation(self, data):
        transposed_data = np.array(data).T
        means = np.array([sum(row) / len(row) for row in transposed_data])
        minus_means = np.array([[element - means[i] for element in row] for i, row in enumerate(transposed_data)])
        minus_means_sqaured = np.array([[element ** 2 for element in row] for row in minus_means])
        numerator = sum(np.array([math.prod(row) for row in minus_means.T]))
        return numerator / math.prod([math.sqrt(sum(row)) for row in minus_means_sqaured])

    def calculate_correlation_matrix(self):
        for dim_1 in range(self.dimensions):
            self.correlation_matrix.append([])
            for dim_2 in range(self.dimensions):
                self.transposed_data = np.array(self.data).T
                temp = np.array([self.transposed_data[dim_1]] + [self.transposed_data[dim_2]])
                cor = self.correlation(temp.T)
                self.correlation_matrix[dim_1].append(cor)
        self.correlation_matrix = np.array(self.correlation_matrix)

    def transform(self):
        self.calculate_correlation_matrix()
        temp_1, temp_2 = np.linalg.eig(self.correlation_matrix)
        permutation = [np.where(temp_1 == eigenvalue)[0][0] for eigenvalue in sorted(temp_1)[::-1]]
        self.eigenvalues = np.array([temp_1[index] for index in permutation])
        self.eigenvectors = np.array([temp_2[index] for index in permutation])
        return np.array([np.dot(row, self.eigenvectors.T) for row in self.data])

