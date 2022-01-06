from principal_component_analysis import PrincipalComponentAnalysis

data = [
    [1,2], 
    [2,3], 
    [2,1], 
    [3,4], 
    [3,2],
    [4,3]
]

print('\ndata 1\n', data)
PCA = PrincipalComponentAnalysis(data)
print('transformed 1\n', PCA.transform())
data = [
    [1,2,0],
    [2,3,1],
    [2,1,3],
    [3,4,2],
    [3,2,4],
    [4,3,6],
]

print('\ndata 2\n', data)
PCA = PrincipalComponentAnalysis(data)
print('transformed 2\n', PCA.transform())