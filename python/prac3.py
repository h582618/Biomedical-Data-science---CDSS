import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss,mean_absolute_error,mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer

import sys


def getPredictions(csvfile):
    df = pd.read_csv(csvfile,sep=";",decimal=',',index_col = 0)
    Binarizer = LabelBinarizer()
    y = Binarizer.fit_transform(df["TYPE"])
    df = df.drop(['TYPE'], axis=1)
    X_train, X_val,Y_train,Y_val = train_test_split(df, y, test_size = 0.3, random_state = 21)

    transformer = RobustScaler(quantile_range=(2.5,97.5))
    transformer.fit_transform(X_train)
    transformer.fit_transform(X_val)

    classifier = MLPClassifier(hidden_layer_sizes=(50,100,50), batch_size = 10, learning_rate_init = 0.001, learning_rate = "adaptive",max_iter=100)

    classifier.fit(X_train, Y_train)

    y_pred = classifier.predict_proba(X_val)
  
    submit_df = pd.DataFrame(data=y_pred,columns=['MENINGIOMA','ASTROCYTOMA','GLIOBLASTOMA'])
    submit_df['RECOMMENDED TUMOR DIAGNOSIS'] = submit_df[['MENINGIOMA', 'ASTROCYTOMA','GLIOBLASTOMA']].idxmax(axis=1)
    submit_df['MENINGIOMA'] = submit_df['MENINGIOMA'].astype(float).map(lambda n: '{:.2%}'.format(n))
    submit_df['ASTROCYTOMA'] = submit_df['ASTROCYTOMA'].astype(float).map(lambda n: '{:.2%}'.format(n))
    submit_df['GLIOBLASTOMA'] = submit_df['GLIOBLASTOMA'].astype(float).map(lambda n: '{:.2%}'.format(n))
    submit_df.to_csv('Probabilities.csv')
    print("Done, check Probabilities.csv")
    
if __name__ == '__main__':
    url_csv_file = sys.argv[1]
    getPredictions(url_csv_file)