import logging
import numpy as np
import traceback
import pandas as pd
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss,mean_absolute_error,mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer
import azure.functions as func
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from pandas.api.types import is_numeric_dtype
import pickle
connection_string = "DefaultEndpointsProtocol=https;AccountName=bdsfunc;AccountKey=OS9EqjlfK+C7klLO9DyBL5PJ+NC0JrCp4a1/jbuMng5WM/4XFTZufoA028jfuVIRKuOrtpF3QfbSmQv53Ssx/g==;EndpointSuffix=core.windows.net"

from sklearn.metrics import accuracy_score,precision_score, recall_score, roc_auc_score, f1_score
def handleMissVar(df):
    for column in df:
        if(is_numeric_dtype(df[column])):
            mean = df[column].mean()
            df[column].fillna(mean,inplace=True)
    return df

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('columns')
    data = req.params.get('data')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('columns')
            data = req_body.get('data')
            df = pd.DataFrame(data, columns = name)
    try:
        ##data prep
        df = df.apply(pd.to_numeric,errors='coerce')
        df['age'] = df['age'].astype(int)
        #df['barthel'] = pd.to_numeric(df['barthel'], errors='coerce')
        #df['charlson'] = df['charlson'].astype(float)
        df['codservicioreal'] = df['codservicioreal'].astype('category')
        df['codidiagingreso'] = df['codidiagingreso'].astype('category')
        '''df['creatinina'] = df['creatinina'].astype(float)
        df['drg'] = df['drg'].astype(float)
        df['estancias'] = df['estancias'].astype(float)
        df['glucosa'] = df['glucosa'].astype(float)
        df['hematocrito'] = df['hematocrito'].astype(float)
        df['leucocitos'] = df['leucocitos'].astype(float)
        df['metastatic_tumor'] = df['metastatic_tumor'].astype(float)
        df['num_grupoact3_HOSP'] = df['num_grupoact3_HOSP'].astype(float)
        df['numurgenciasprevias'] = df['numurgenciasprevias'].astype(float)
        df['potasio'] = df['potasio'].astype(float)
        df['proteina_c_reactiva'] = df['proteina_c_reactiva'].astype(float)
        df['rdw_cv'] = df['rdw_cv'].astype(float)
        df['rdw_sd'] = df['rdw_sd'].astype(float)
        df['sodio'] = df['sodio'].astype(float)
        df['urea'] = df['urea'].astype(float)
        df['label']= df['label'].astype(float)
        '''
        label = df['label']
    
        label = pd.DataFrame(label)
        label.columns =[ 'label']
        label['label']= label['label'].astype('category')
       
        df['codservi2'] = df['codservicioreal'].cat.codes
        df['codiagngr2'] = df['codidiagingreso'].cat.codes
        y = label
        X = df.drop(['codidiagingreso','codservicioreal', 'label'], axis = 1)  
        X = handleMissVar(X)
    except Exception as e:
        return func.HttpResponse(f"Failed at data prep {(traceback.format_exc())}")
    try:
    
        X_train, X_val,y_train,y_val = train_test_split(X,y, test_size = 0.2, random_state = 21)
       
        X_train = handleMissVar(X_train)
        X_val = handleMissVar(X_val)
        y_train = handleMissVar(y_train)
        y_val = handleMissVar(y_val)
        RF = RandomForestClassifier(n_estimators= 100, max_depth = 50,class_weight = 'balanced')
        RF.fit(X_train, y_train)

        y_pred = RF.predict(X_val)
        probclass_1 = RF.predict_proba(X_val)[:, 1]
    except Exception as e:
        return func.HttpResponse(f"Failed at model creating {e}")
    
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = str(uuid.uuid4())
        container_client = blob_service_client.create_container(container_name)
        pickle.dump(RF, open(r"model", "w+b"))
        blob_client = blob_service_client.get_blob_client(container=container_name, blob="model")
        with open(r"model", "rb") as data:
            blob_client.upload_blob(data)  
    except Exception as e:
        return func.HttpResponse(f"Failed at model uploading {(traceback.format_exc())}")
    else : 
        return func.HttpResponse(f"\nUploading to Azure Storage as blob:\n\t" + "model",status_code=200)

    

    if name:
        return func.HttpResponse(f"Columns are , {df.head()}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

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

