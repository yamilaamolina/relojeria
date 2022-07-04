from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS 
from flask_mysqldb import MySQL

from security import authenticate, identity
from user import UserRegister
from empleado import Empleado, ListEmpleado

app = Flask(__name__)
app.secret_key = 'Gestion2021+'
api = Api(app)
CORS(app)

mysql = MySQL(app)

jwt = JWT(app, authenticate, identity)  #/auth

api.add_resource(Empleado, '/empleado/<string:legajo>')
api.add_resource(ListEmpleado, '/empleados')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':   #por si importo la app, así no lo ejecute
    app.run(port=5000, debug=True)  #debug para que tire una página a visitar si da un error

