
from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)

#Variables GLOBALES
id = ""
KEY_VALUES_MUNI = ['codmuni', 'nombre', 'codpro']
KEY_VALUES_PROV = ['codpro', 'nombre', 'codauton', 'comunidad', 'capital']
KEY_VALUES_T_MUNI = ['codmuni', 'fecha', 'minima', 'maxima', 'lluvia']
KEY_VALUES_T_PROV = ['codprov', 'hoy', 'manana', 'fecha']


#Define la conexion a la base de datos
def get_db():
    conn = sqlite3.connect("tiempo.db")
    return conn


#Enrutamiento hacia la url .../municipios la cual devuelve todo el listado de municipios en formato JSON
@app.route('/municipios/')
def get_municipios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select nombre from municipios')
    municipios = cursor.fetchall()
    #TODO DICCIONARIO
    return jsonify(municipios)


#Enrutamiento hacia la url .../provincias la cual devuelve todo el listado de las provincias en formato JSON
@app.route('/provincias/')
def get_provincias():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select codprov, nombre from provincias')
    provincias = cursor.fetchall()
    #TODO diccionario
    return jsonify(provincias)


#Enrutamiento hacia la url .../municipios/codmuni la cual devuelve los datos del municipio especifico en formato JSON
@app.route('/municipios/<id>')
def get_municipio(id):
    db = get_db()
    #KEY_VALUES_MUNI = ['codmuni', 'nombre', 'codpro']
    cursor = db.cursor()
    #key_values = cursor.description
    #cursor.execute("select * from municipios where codmuni ='"+id+"'")

    #Consulta modificada para buscar por nombre de municipio
    cursor.execute("select * from municipios where lower(nombre) =lower('"+id+"')") #lower() convierte el texto a minusculas
    municipio = cursor.fetchall()
    municipios = []
    
    for municipios in municipio:
        d = dict(zip(KEY_VALUES_MUNI, municipios))

    return jsonify(d)


#Enrutamiento hacia la url .../provincias/codprov la cual devuelve los datos de la provincia especifica en formato JSON
@app.route('/provincias/<id>')
def  get_provincia(id):
    db = get_db()
    cursor = db.cursor()
    #KEY_VALUES_PROV =  ['codpro', 'nombre', 'codauton', 'comunidad', 'capital']
    cursor.execute("select * from provincias where codprov = '"+id+"'")

    #Consulta para buscar por nombre de provincia
    #cursor.execute("select * from provincias where lower(nombre) = lower('"+id+"')")
    provincia = cursor.fetchall()

    for provincias in provincia:
        d = dict(zip(KEY_VALUES_PROV, provincias))
    return jsonify(d)


#Enrutamiento hacia la url .../tiempomunicipio/codmuni la cual devuelve los datos del tiempo de un municipio en formato JSON
@app.route('/tiempomunicipio/<id>')
def get_tiempomunicipio(id):
    db = get_db()
    #KEY_VALUES_T_MUNI = ['codmuni', 'fecha', 'minima', 'maxima', 'lluvia']
    cursor = db.cursor()
    #cursor.execute("select * from tiempoMunicipio where fecha = date() and codmuni = '"+id+"'")

    #Consulta modificada para buscar por nombre de municipio
    cursor.execute("select * from tiempoMunicipio where  fecha = date() and codmuni = (select codmuni from municipios where lower(nombre)=lower('"+id+"'))")
    tiempomunicipio = cursor.fetchall()

    for i in tiempomunicipio:
        d = dict(zip(KEY_VALUES_T_MUNI, i))

    return jsonify(d)

#Enrutamiento hacia la url .../tiempomunicipio/codmuni/fecha la cual devuelve los datos del tiempo de un día en concreto
# de municipio en formato JSON
@app.route('/tiempomunicipioFecha/<id>/<fecha>')
def get_tiempomunicipioFecha(id,fecha):
    db = get_db()
    #KEY_VALUES_T_MUNI = ['codmuni', 'fecha', 'minima', 'maxima', 'lluvia']
    cursor = db.cursor()
    #cursor.execute("select * from tiempoMunicipio where fecha = date() and codmuni = '"+id+"'")
    #Consulta modificada para buscar por nombre de municipio
    cursor.execute("select * from tiempoMunicipio where fecha = '" + fecha + "' and codmuni = (select codmuni from municipios where lower(nombre)=lower('"+id+"'))")
    tiempomunicipio = cursor.fetchall()

    for i in tiempomunicipio:
        d = dict(zip(KEY_VALUES_T_MUNI, i))

    return jsonify(d)


#Enrutamiento hacia la url .../tiempoprovincia/conprov la cual devuelve los datos del tiempo de una provincia en formato JSON
@app.route('/tiempoprovincia/<id>')
def get_tiempoprovincia(id):
    db = get_db()
    #KEY_VALUES_T_PROV = ['codprov', 'hoy', 'manana', 'fecha']
    cursor = db.cursor()
    cursor.execute("select * from tiempoProvincia where fecha = date() and codprov = '"+id+"'")
    
    #Consulta para busqueda por nombre
    #cursor.execute("select * from tiempoProvincia where fecha = date() and codprov = (select codprov from provincias where lower(nombre) = lower('"+id+"'))")
    tiempoprovincia = cursor.fetchall()

    for i in tiempoprovincia:
        d = dict(zip(KEY_VALUES_T_PROV, i))

    return jsonify(d)    

#Enrutamiento hacia la url .../tiempoprovinciaFecha/codprov/fecha la cual devuelve los datos del tiempo de una día en concreto 
# de una provincia en formato JSON
@app.route('/tiempoprovinciaFecha/<id>/<fecha>')
def get_tiempoprovinciaFecha(id,fecha):
    db = get_db()
    #KEY_VALUES_T_PROV = ['codprov', 'hoy', 'manana', 'fecha']
    cursor = db.cursor()
    cursor.execute("select * from tiempoProvincia where fecha = '" + fecha + "' and codprov = '"+id+"'")
    #Consulta para busqueda por nombre
    #cursor.execute("select * from tiempoProvincia where fecha = date() and codprov = (select codprov from provincias where lower(nombre) = lower('"+id+"'))")
    tiempoprovincia = cursor.fetchall()

    for i in tiempoprovincia:
        d = dict(zip(KEY_VALUES_T_PROV, i))

    return jsonify(d)   

#Devuelve el id de ese nombre de municipio
@app.route('/idmunicipio/<nombre>')
def get_idMunicipio(nombre):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select codmuni from municipios where nombre = '"+nombre+"'")
    nombres = cursor.fetchall()

    for i in nombres:
        d = dict(zip('codmuni', i))

    return jsonify(d)

#Devuelve el id de ese nombre de provincia
@app.route('/idprovincia/<nombre>')
def get_idProvincia(nombre):
    db = get_db()
    key_values = ['codprov']
    cursor = db.cursor()
    cursor.execute("select codprov from provincias where nombre = '"+nombre+"'")
    nombres = cursor.fetchall()

    for i in nombres:
        d = dict(zip(key_values, i))

    return jsonify(d)

#@app.route('/idmunicipio/<nombre>')
#def get_idMunicipio(nombre):
#    db = get_db()
#    cursor = db.cursor()
#    cursor.execute("select codmuni, nombre from municipios where nombre like '"+nombre+"%'")
#    nombres = cursor.fetchall()
#    return jsonify(d)


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response    

if __name__ == "__main__":
    app.run()