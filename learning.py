# Load libraries
from six.moves import input
import datetime
import pandas
import numpy
from numpy import mean, absolute
from pandas.tools.plotting import scatter_matrix
from scipy import stats
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from cProfile import label

numpy.set_printoptions(threshold=numpy.inf)        

class learning:
    def _init_(self):
        super(learning, self)._init_()
        
    def mad(self, data, axis=None):
        return mean(absolute(data-mean(data,axis)), axis)
    
    def processData(self, data, model):
        segment_X = preprocessing.normalize(data)
        features = numpy.empty(36)
        for j in range(0, features.shape[0] - 1, 3):
            features[j] = segment_X[ : , j // 3].mean()
            features[j + 1] = segment_X[ : , j // 3].std()
            features[j + 2] = self.mad(segment_X[ : , j // 3])
        string = (model.predict([features]))
        return le.inverse_transform([int(string[0])])
    
    def machineTrain(self):
        # Load dataset
        #url = "C:/Users/CheeYeo/Desktop/CG3002/Code/nextFiveMovesv1/6pplData2.csv" #CY's computer file path
        #url = "C:/Users/User/Documents/SEM5/CG3002/Project3002/Week11 Readings/6pplData.csv"
        #url = "C:/Users/User/Documents/SEM5/CG3002/Project3002/New 2/6pplData.csv"  # Kelvin's computer file path
        url = "/home/pi/Desktop/6pplData.csv"
        dataset = pandas.read_csv(url)
        
        global window_size
        window_size = 120
        shift_size = 30
        models = []
        models.append(('KNN', KNeighborsClassifier(n_neighbors=7)))
        knn = KNeighborsClassifier(n_neighbors=3)
        
        # Split-out validation dataset
        array = dataset.values
        X = array[:, 0:12]
        Y = array[:, 12]

        # label encode
        global le 
        le = preprocessing.LabelEncoder()
        le.fit(['NoMove', 'wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping', 'jumpingjack', 'turnclap', 'squatturnclap', 'window', 'window360', 'final'])
        Y_encoded = le.transform(Y)
        print(Y_encoded)
#         print(le.inverse_transform([0]))
#         print(le.inverse_transform([1]))
#         print(le.inverse_transform([2]))
#         print(le.inverse_transform([3]))
#         print(le.inverse_transform([4]))
#         print(le.inverse_transform([5]))
        N = dataset.shape[0]
        dim_X = X.shape[1]
        # dim_X = 6
        K = (N // shift_size) - 7
        segments_X = numpy.empty((K, window_size, dim_X))
        segments_Y = numpy.empty((K, window_size))
        
        for i in range(K):
            segment_X = X[i * shift_size : (i * shift_size) + window_size , :]
            # segment_X = preprocessing.normalize(segment_X)
            segment_Y = Y_encoded[i * shift_size : (i * shift_size) + window_size]
            segments_X[i] = segment_X
            segments_Y[i] = segment_Y
        
        # for i in range(K):
        #     segment_X[0:3] = X[i * shift_size : (i * shift_size) + window_size , :3]
        #     segment_X[3:6] = X[i * shift_size : (i * shift_size) + window_size , 6:]
        #     # segment_X = preprocessing.normalize(segment_X)
        #     segment_Y = Y_encoded[i * shift_size : (i * shift_size) + window_size]
        #     segments_X[i] = segment_X
        #     segments_Y[i] = segment_Y
        
        features = numpy.empty((K, 36))
        outputs = numpy.empty((K))
        
        for i in range(K):
            for j in range(0, features.shape[1] - 1, 3):
                features[i, j] = segments_X[i, : , j // 3].mean()
                features[i, j + 1] = segments_X[i, : , j // 3].std()
                features[i, j + 2] = self.mad(data = segments_X[i, : , j // 3])

            outputs[i] = stats.mode(segments_Y[i])[0]
        validation_size = 0.2
        seed = 7
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(features, outputs, test_size=validation_size, random_state=seed)

        # Test options and evaluation metric
        scoring = 'accuracy'
        
        # evaluate each model in turn
        results = []
        
        names = []
        for name, model in models:
        	kfold = model_selection.KFold(n_splits=10, random_state=seed)
        	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        	results.append(cv_results)
        	names.append(name)
        	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        	print(msg)
         
        # Make predictions on validation dataset
        knn.fit(X_train, Y_train)
        print("exit training")
        predictions = knn.predict(X_validation)
        print("Accuracy Score: ", accuracy_score(Y_validation, predictions), file=open('summary.txt', 'a'))
        print("Confusion Matrix: \n", confusion_matrix(Y_validation, predictions, labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), file=open('summary.txt', 'a'))
        print("Classification Report: \n", classification_report(Y_validation, predictions), file=open('summary.txt', 'a'))
        
        
        return knn


run = learning()
run.machineTrain()
