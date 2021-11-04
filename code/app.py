from typing import Text
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Gestion2021+'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth

empleados = []

class Empleado(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('nombre', 
        type=Text, 
        required=True, 
        help="Este campo no puede dejarse vacío"
    )

    def get(self, legajo):
        empleado = next(filter(lambda x: x['legajo'] == legajo, empleados), None)
        return {'empleado': empleado}, 200 if empleado is not None else 404
    
    def post(self, legajo):
        if next(filter(lambda x: x['legajo'] == legajo, empleados), None):
            return {'message': "Ya existe un empleado con el legajo {}".format(legajo)}, 400

        #data = request.get_json()     #force=True significa que no se fijará en el Content-Type, asumirá que es un json #silent=True simplemente no da error, no devuelve nada
        data = Empleado.parser.parse_args()
        empleado = {'legajo': legajo, 'nombre': data['nombre']}
        empleados.append(empleado)
        return empleado, 201

    @jwt_required()
    def delete(self, legajo):
        global empleados
        empleados = list(filter(lambda x: x['legajo'] != legajo, empleados))
        return{'message': 'Empleado eliminado'}

    def put(self, legajo):
        data = Empleado.parser.parse_args()
        empleado = next(filter(lambda x: x['legajo'] == legajo, empleados), None)
        if empleado is None:
            empleado = {'legajo': legajo, 'nombre': data['nombre']}
            empleados.append(empleado)
        else:
            empleado.update(data)
        return empleado


class ListEmpleado(Resource):
    def get(self):
        return {'empleados': empleados}

api.add_resource(Empleado, '/empleado/<string:legajo>')
api.add_resource(ListEmpleado, '/empleados')

app.run(port=5000, debug=True)  #debug para que tire una página a visitar si da un error


