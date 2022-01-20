import numpy as np
import math

class PrincipalComponentAnalysis:
    def fit(self, data):
        self.data = np.array(data)
        self.correlation_matrix = np.corrcoef(self.data.T)
        temp_1, temp_2 = np.linalg.eig(self.correlation_matrix)
        permutation = [np.where(temp_1 == eigenvalue)[0][0] for eigenvalue in sorted(temp_1)[::-1]]
        self.eigenvalues = temp_1[permutation]
        self.eigenvectors = np.apply_along_axis(lambda row: np.array([round(value, 15) for value in row]), 0, temp_2[permutation])
        #self.eigenvectors = np.array([temp_2[index] / min(np.array(temp_2[index])) for index in permutation]) #temp_2[:, permutation]#np.apply_along_axis(lambda row: row / min(row), 0, temp_2[:, permutation])
        self.transformed_data = self.data @ self.eigenvectors.T

    def transform_point(self, point, principal_component):
        return np.array(point) @ self.eigenvectors[principal_component].T

