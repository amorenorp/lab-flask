from flask import Flask, request
from helpers import mongoConnection
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient()
db = client.labflask
collec = db.celebs


#Muestra los detalles de un ID dado
def details(id):
    
    return db.celebs.find({"_id": ObjectId(id)},{"_id":0})
    
#Añade un celebrity dandole un nombre, ocupacion y una frase suya
def insert_data_celebrity(name, occupation, catch_phrase = "None"):
    
    dic = {
        "Name": f"{name}",
        "occupation": f"{occupation}",
        "catch_phrase": f"{catch_phrase}"   
    }
    
    i = db.celebs.insert_one(dic)
    
    return i

#Borra una celebrity dandole su ID
def borrar_id(id):
    return db.celebs.remove({"_id": ObjectId(id)})



#Crear API

app = Flask("lab_api")

#Endpoints: 

@app.route("/")
def root():
    return {"Welcome": "to my API!!!"}


@app.route("/celebrities")
def info_celeb():
    celebrity = db.celebs.find({},{"Name":1})

    return dumps(celebrity)


@app.route("/celebrities/details/<id>")
def info_details(id):
    id = str(id)

    try:
        info_final= details(id)
    
        return dumps(info_final)

    except: 
        return "Ese Id no existe, crack"

@app.route("/celebrities/new/<name>/<occupation>/<catch_phrase>")
def new(name, occupation, catch_phrase):
    insert_data_celebrity(name, occupation, catch_phrase)

    return "Ya se ha añadido la nueva celebrity"

@app.route("/celebrities/delete/<id>")
def delete_id(id):
    id= str(id)

    try:
        borrar_id(id)

        return f"Se ha borrado celebrity: {id}"
    
    except:
        return "No existe ese Id, maquina"


app.run(debug= True)





