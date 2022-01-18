import logging
import numpy as np
import traceback
import pandas as pd
import json
from sklearn.metrics import log_loss,mean_absolute_error,mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from pandas.api.types import is_numeric_dtype
from sklearn.metrics import accuracy_score,precision_score, recall_score, roc_auc_score, f1_score
import pickle
import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer
import azure.functions as func
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
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

def get_weights_blob(blob_name, container_name):
    
    blob_client = BlobClient.from_connection_string(connection_string, container_name, blob_name)
    downloader = blob_client.download_blob(0)

    # Load to pickle
    b = downloader.readall()
    weights = pickle.loads(b)

    return weights

def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')

    container_n = req.params.get('container_name')
    columns = req.params.get('columns')
    data = req.params.get('data')
    if not container_n:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            container_n = req_body.get('container_name')
            columns = req_body.get('columns')
            data = req_body.get('data')
            df = pd.DataFrame(data, columns = columns)
    try:
        ##data prep
        df = df.apply(pd.to_numeric,errors='coerce')
        df['age'] = df['age'].astype(int)
        #df['barthel'] = pd.to_numeric(df['barthel'], errors='coerce')
        #df['charlson'] = df['charlson'].astype(float)
        df['codservicioreal'] = df['codservicioreal'].astype('category')
        df['codidiagingreso'] = df['codidiagingreso'].astype('category')
       
        df['codservi2'] = df['codservicioreal'].cat.codes
        df['codiagngr2'] = df['codidiagingreso'].cat.codes
        X = df.drop(['codidiagingreso','codservicioreal'], axis = 1)  
        X = handleMissVar(X)
    except Exception as e:
        return func.HttpResponse(f"Failed at data prep {(traceback.format_exc())}")
    try:
        weights = get_weights_blob(blob_name = 'Model',container_name=container_n)
    except Exception as e:
         return func.HttpResponse(f"Failed at {(traceback.format_exc())}")
    logging.info('Python HTTP trigger function processed a request.')

    try:
        
        
        
        y_pred = weights.predict(X)
        results = {"label":y_pred.tolist()}
        logging.info(f'{results}')
        logging.info(f't. {df.dtypes}')
        return func.HttpResponse(   
            json.dumps(results),
        mimetype="application/json",
    )
        return func.HttpResponse({y_pred},status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Failed at model predicting {(traceback.format_exc())}")
    

    return func.HttpResponse(f"Weights received {weights}")
    
