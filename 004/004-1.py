from sklearn.neighbors  import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

import pandas
from generate_data import generate_graph

def correct_data(data, labels): # data = [[(1,1),(1,1.3),...], [(3,1),(3,1.3),...],...] labels = [1,0...]
    data_2 = list(zip(data))
    data_3 = np.array(data_2)
    data_4 = pd.from_array(data_3)
    return x, y

def KNN(x,y,k,len_dataframe): # k is num neighbors
    training_x, testing_x, training_y, testing_y = train_test_split(X, y, test_size=0.3, random_state=1)
    KNN = KNeighborsClassifier(n_neighbors = k)
    KNN.fit(training_x, training_y)
    return KNN.score(testing_x, testing_y)

#def DTC(x,y,k): # k is min size split
 #   correct = 0
  #  for i in range():

#def RFC(x,y,k): # k is num trees

oneone = generate_graph((1,1), 1.25, 50)
onethree = generate_graph((1,3), 1.25, 50)
threeone = generate_graph((3,1), 1.25, 50)
threethree = generate_graph((3,3), 1.25, 50)

corrected_data = correct_data([oneone, onethree, threeone, threethree], [1,0,1,0])