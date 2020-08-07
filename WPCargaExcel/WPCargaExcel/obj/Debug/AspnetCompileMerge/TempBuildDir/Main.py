class clsCargaExcel(object):
    """description of class"""
import requests
import json
from json import JSONEncoder
from datetime import datetime
from flask import jsonify
from pandas import read_excel
from azure.storage.blob import BlobServiceClient
import pandas as pnd

API_ENDPOINT = 'http://appbackendtest.azurewebsites.net//api/ApiBackEnd/Invoke'#'http://localhost:62297/api/ApiBackEnd/Invoke'
APLICATIVO = '4NzC6P4FC6Qst2xLRWPnhOXuMvm7IsEb/2QxkymcLGY='

def procesaExcel():
    class TabConfigSys:
                llave_Config1 = None
                llave_Config2 = None
                llave_Config3 = None
                llave_Config4 = None
                llave_Config5 = None

    class ObjetoJava:
        Parametros = None
        NombreSp = None
        Aplicativo = None
        DataBase = None

    config = TabConfigSys()
    config.llave_Config1 = 'SERVICIO'
    config.llave_Config2 = 'CONFIGURACION'
    config.llave_Config3 = 'SERVIDOR'
    config.llave_Config4 = 'URL'
    config.llave_Config5 = 'CONECTION'

    objJava = ObjetoJava()
    objJava.Parametros = json.dumps(config.__dict__)
    objJava.NombreSp = 'Configuracion'
    objJava.Aplicativo = APLICATIVO
    data = json.dumps(objJava.__dict__)

    headers = {'content-type': 'application/json'}
    r = requests.post(url = API_ENDPOINT, data =data,headers=headers) 
    if r.status_code == requests.codes.ok:
        results = json.loads(r.text)
    else:
        print(mensaje = 'Error al consultar el api')

    conn_str = results[0]["Dato_Char1"]
    container_name = results[0]["Dato_Char2"]
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)
    container = blob_service_client.get_container_client(container=container_name)
    generator = container.list_blobs()

    class ClientesDomiciliados:
        Identificacion = None
        EstadoExclusion = None
        AreaSolicitante = None
        FechaVigenciaExclu = None
        UsrModifica = None

    for blobs in generator:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blobs.name)
        df = pnd.read_excel(blob_client.download_blob().readall(), sheet_name=results[0]["Dato_Char3"])
        #print( df.columns.values[1])
        for _, row in df.iterrows():
            objClientDomi = ClientesDomiciliados()
            objClientDomi.Identificacion = row['Identificacion']
            objClientDomi.EstadoExclusion = row['EstadoExclusion']
            objClientDomi.AreaSolicitante = row['AreaSolicitante']
            objClientDomi.FechaVigenciaExclu =  row['FechaVigenciaExclu']._date_repr
            objClientDomi.UsrModifica = 'ServProcesaExcel'
            #print(objClientDomi.Identificacion)
            objJava = ObjetoJava()
            objJava.Parametros = json.dumps(objClientDomi.__dict__)
            objJava.NombreSp = 'ExclusionDomiciliaciones'
            objJava.Aplicativo = APLICATIVO
            data = json.dumps(objJava.__dict__)
            headers = {'content-type': 'application/json'}
            r = requests.post(url = API_ENDPOINT, data =data,headers=headers) 
            if r.status_code == requests.codes.ok:
                results = json.loads(r.text)
                #print(results)
            else:
                print('Error al consultar el api')
        #print(df)
        #dfs = []
        #for framename in df.keys():
           #print(df[framename])

            #temp_df = df[framename]
            #temp_df['Session'] = framename
            #dfs.append(temp_df)

        #print(dfs)
        #blob_client.delete_blob()

        # Main method.
if __name__ == '__main__':
    procesaExcel()

