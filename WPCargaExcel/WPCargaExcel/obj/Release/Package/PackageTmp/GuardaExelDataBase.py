from flask import Flask, request , render_template
import requests
import json
from json import JSONEncoder
from flask import jsonify
app = Flask(__name__)

import pandas as pnd
from pandas import read_excel
import urllib
from sqlalchemy import create_engine
import sqlalchemy as sa

API_ENDPOINT = 'http://appbackendtest.azurewebsites.net//api/ApiBackEnd/Invoke'#'http://localhost:62297/api/ApiBackEnd/Invoke'
APLICATIVO = '4NzC6P4FC6Qst2xLRWPnhOXuMvm7IsEb/2QxkymcLGY='
@app.route("/")
def index():
    return render_template('index.html')   


@app.route('/GuardarArchivoDataBase', methods=['POST'])
def GuardarArchivoDataBase():
    try:
        files = request.files['file']
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
        config.llave_Config1 = 'API'
        config.llave_Config2 = 'PYTHON'
        config.llave_Config3 = 'CONEXION'
        config.llave_Config4 = 'ACCESOS'
        config.llave_Config5 = 'SQL'

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

        #'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' +
        #database + ';UID=' + usuario + ';PWD=' + password
        quoted = urllib.parse.quote_plus(results[0]["Dato_Char1"])
        engine = sa.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
        df = pnd.read_excel(files.read(), results[0]["Dato_Char2"])
        df.to_sql(files.filename, schema=results[0]["Dato_Char3"], con = engine)

        result = engine.execute('SELECT COUNT(*) FROM [' + results[0]["Dato_Char3"] + '].[' + files.filename + ']')

    except Exception as ex:
        return jsonify(mensaje = 'Error detalle: ' + ex)
    else:
        return jsonify(mensaje = 'Archivo almacenado Nombre: ' + files.filename)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    #app.debug = True
    app.run()
