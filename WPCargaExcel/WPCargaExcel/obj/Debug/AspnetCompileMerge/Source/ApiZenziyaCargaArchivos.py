class ApiZenziyaCargaArchivos(object):
    """description of class"""


from flask import Flask, request
import requests
import json
from json import JSONEncoder
#import time
from flask import jsonify
from azure.storage.blob import BlobServiceClient
app = Flask(__name__)

#blob config
#container_name = "cosito"
API_ENDPOINT = 'http://appbackendtest.azurewebsites.net//api/ApiBackEnd/Invoke'#'http://localhost:62297/api/ApiBackEnd/Invoke'
APLICATIVO = '4NzC6P4FC6Qst2xLRWPnhOXuMvm7IsEb/2QxkymcLGY='
@app.route("/")
def index():
    return render_template("index.html")   


@app.route('/GuardarArchivo', methods=['POST'])
def GuardarArchivo():
    try:
        files = request.files['file']
        try:
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
              return jsonify(mensaje = 'Error al consultar el api')
        except Exception as exx:   return jsonify(mensaje = 'Error al consultar el api: ' + xx.message) #print(exx)
        conn_str = results[0]["Dato_Char1"]
        container_name = results[0]["Dato_Char2"]
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=files.filename)
            container = blob_service_client.get_container_client(container=container_name)
            generator = container.list_blobs()
            counter = 0
            for blob in generator:
                counter = counter + 1
                if blob.name == files.filename:
                  return jsonify(mensaje = 'Ya existe un archivo con este nombre: ' + files.filename)
                else :
                      blob_client.upload_blob(files.read())
                      return jsonify(mensaje = 'Archivo almacenado')
            if counter == 0:
                blob_client.upload_blob(files.read())
                return jsonify(mensaje = 'Archivo almacenado')
        except Exception as aa: return jsonify(mensaje = 'Ya existe un archivo con este nombre: ' + aa.message)

    except Exception as ex:
        return jsonify(mensaje = 'Ya existe un archivo con este nombre: ' + ex.message)
    else:
        return jsonify(mensaje = 'Archivo almacenado')

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    app.run()