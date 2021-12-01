
from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)

#Define la conexion a la base de datos
def get_db():
    conn = sqlite3.connect("tiempo.db")
    return conn

#Enrutamiento hacia la url .../municipios la cual devuelve todo el listado de municipios en formato JSON
#@app.route('/municipios/')
#def get_municipios():
#    db = get_db()
#    cursor = db.cursor()
#    cursor.execute('select * from municipios')
#    municipios = cursor.fetchall()
#    #TODO DICCIONARIO
#    return jsonify(municipios)

#Enrutamiento hacia la url .../provincias la cual devuelve todo el listado de las provincias en formato JSON
#@app.route('/provincias')
#def get_provincias():
#    db = get_db()
#    cursor = db.cursor()
#    cursor.execute('select * from provincias')
#    provincias = cursor.fetchall()
#    #TODO diccionario
#    return jsonify(provincias)

#Enrutamiento hacia la url .../municipios/codmuni la cual devuelve los datos del municipio especifico en formato JSON
@app.route('/municipios/<id>')
def get_municipio(id):
    db = get_db()
    key_values = ['codmuni', 'nombre', 'codpro']
    cursor = db.cursor()
    #key_values = cursor.description
    cursor.execute('select * from municipios where codmuni ='+id)
    municipio = cursor.fetchall()

    for municipios in municipio:
        d = dict(zip(key_values, municipios))

    return jsonify(d)

#Enrutamiento hacia la url .../provincias/codprov la cual devuelve los datos de la provincia especifica en formato JSON
@app.route('/provincias/<id>')
def  get_provincia(id):
    db = get_db()
    cursor = db.cursor()
    key_values =  ['codpro', 'nombre', 'codauton', 'comunidad', 'capital']
    cursor.execute('select * from provincias where codprov = '+id)
    provincia = cursor.fetchall()

    for provincias in provincia:
        d = dict(zip(key_values, provincias))
    return jsonify(d)

#Enrutamiento hacia la url .../tiempomunicipio/codmuni la cual devuelve los datos del tiempo de un municipio en formato JSON
@app.route('/tiempomunicipio/<id>')
def get_tiempomunicipio(id):
    db = get_db()
    key_values = ['codmun', 'fecha', 'minima', 'maxima', 'lluvia']
    cursor = db.cursor()
    cursor.execute('select * from tiempoMunicipio where codmuni = '+id)
    tiempomunicipio = cursor.fetchall()

    for i in tiempomunicipio:
        d = dict(zip(key_values, i))

    return jsonify(d)

#Enrutamiento hacia la url .../tiempoprovincia/conprov la cual devuelve los datos del tiempo de una provincia en formato JSON
@app.route('/tiempoprovincia/<id>')
def get_tiempoprovincia(id):
    db = get_db()
    key_values = ['codprov', 'fecha', 'minima', 'maxima', 'lluvia']
    cursor = db.cursor()
    cursor.execute('select * from tiempoProvincia where codprov = '+id)
    tiempoprovincia = cursor.fetchall()

    for i in tiempoprovincia:
        d = dict(zip(key_values, i))

    return jsonify(d)    

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response    

if __name__ == "__main__":
    app.run()