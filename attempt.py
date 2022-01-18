import pickle
import time
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report, precision_score, recall_score, roc_auc_score, f1_score,precision_recall_fscore_support


def handleMissVar(df):
    for column in df:
        if(is_numeric_dtype(df[column])):
            mean = df[column].mean()
            df[column].fillna(mean,inplace=True)
    return df

try:
    data = pd.read_csv('inadvance_synth.csv',sep=';')
    label = data['label']
    label = pd.DataFrame(label)
    label.columns =[ 'label']
    data['codservicioreal'] = data['codservicioreal'].astype('category')
    data['codidiagingreso'] = data['codidiagingreso'].astype('category')
    label['label']= label['label'].astype('category')
    data['codservi2'] = data['codservicioreal'].cat.codes
    data['codiagngr2'] = data['codidiagingreso'].cat.codes
    loaded_model = pickle.load(open("RandomForest.pkl", 'rb'))
    print(loaded_model)
    y = label
    X = data.drop(['Unnamed: 0','codidiagingreso','codservicioreal', 'label'], axis = 1)  
    X = handleMissVar(X)
    X_train, X_val,y_train,y_val = train_test_split(X,y, test_size = 0.2, random_state = 21)
       
    
    X_val = handleMissVar(X_val)
    y_val = handleMissVar(y_val)
    y_pred = loaded_model.predict(X_val)
    submit_df = pd.DataFrame(data=y_pred,columns=['Label'])
    print(submit_df.head())
    print(print(f"Accuray : {accuracy_score(y_val, y_pred) * 100:.2f}%"))

except Exception as ex:
    print('Exception:')
    print(ex)


