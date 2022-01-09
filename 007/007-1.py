import numpy as np
from principal_component_analysis import PrincipalComponentAnalysis

data = np.array([
    [1,2], 
    [2,3], 
    [2,1], 
    [3,4], 
    [3,2],
    [4,3]
])

print('\ndata 1\n', data)
PCA = PrincipalComponentAnalysis()
PCA.fit(data)
print('\ncorrelation matrix 1\n', PCA.correlation_matrix)
print('\neigenvalues 1\n', PCA.eigenvalues)
print('\neigenvectors 1\n', PCA.eigenvectors)
print('\ntransformed 1\n', PCA.transformed_data)

data = np.array([
    [1,2,0],
    [2,3,1],
    [2,1,3],
    [3,4,2],
    [3,2,4],
    [4,3,6],
])

print('\ndata 2\n', data)
PCA = PrincipalComponentAnalysis()
PCA.fit(data)
print('\ncorrelation matrix 2\n', PCA.correlation_matrix)
print('\neigenvalues 2\n', PCA.eigenvalues)
print('\neigenvectors 2\n', PCA.eigenvectors)
print('\ntransformed 2\n', PCA.transformed_data)

print('\ntest transform 1', PCA.transform_point((1,2,0), 1))
print('test transform 2', PCA.transform_point((1,2,0), 2))
print('test transform 3', PCA.transform_point((1,2,0), 3))