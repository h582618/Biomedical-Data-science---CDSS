import os, uuid
from timeit import Timer
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import pickle
import time
from sklearn.ensemble import RandomForestClassifier

connection_string = "DefaultEndpointsProtocol=https;AccountName=bdsfunc;AccountKey=OS9EqjlfK+C7klLO9DyBL5PJ+NC0JrCp4a1/jbuMng5WM/4XFTZufoA028jfuVIRKuOrtpF3QfbSmQv53Ssx/g==;EndpointSuffix=core.windows.net"

def get_weights_blob(blob_name):
    blob_client = BlobClient.from_connection_string(connection_string, container_name, blob_name)
    downloader = blob_client.download_blob(0)

    # Load to pickle
    b = downloader.readall()
    weights = pickle.loads(b)

    return weights

try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = str(uuid.uuid4())
    container_client = blob_service_client.create_container(container_name)

    print(container_name)
    favorite_color = { "lion": "yellow", "kitty": "red" }
    loaded_model = pickle.load(open("GradientBoostingClas.pkl", 'rb'))
    pickle.dump( loaded_model, open(r"Model", "wb" ) )

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="Model")

    print("\nUploading to Azure Storage as blob:\n\t" + "RandomForest")

    with open(r"Model", "rb") as data:
        blob_client.upload_blob(data)    
    time.sleep(200)


    weights = get_weights_blob(blob_name = 'Model')
    print(f"weight is ",weights)

except Exception as ex:
    print('Exception:')
    print(ex)

def get_weights_blob(blob_name):
    connection_string = 'my_connection_string'
    blob_client = BlobClient.from_connection_string(connection_string, container_name, blob_name)
    downloader = blob_client.download_blob(0)

    # Load to pickle
    b = downloader.readall()
    weights = pickle.loads(b)

    return weights

    #DefaultEndpointsProtocol=https;AccountName=bdsfunc;AccountKey=OS9EqjlfK+C7klLO9DyBL5PJ+NC0JrCp4a1/jbuMng5WM/4XFTZufoA028jfuVIRKuOrtpF3QfbSmQv53Ssx/g==;EndpointSuffix=core.windows.net