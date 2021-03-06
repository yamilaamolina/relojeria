from os import close
import sqlite3
from sqlite3.dbapi2 import Cursor, connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.empleado import EmpleadoModel

class Empleado(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('nombre', 
        type=str, 
        required=True, 
        help="Este campo no puede dejarse vacío"
    )

    def get(self, legajo):
        empleado = EmpleadoModel.find_by_legajo(legajo)

        if empleado:
            return empleado.json()

        return {'message': 'Empleado no encontrado'}, 404

    @jwt_required()
    def post(self, legajo):
        if EmpleadoModel.find_by_legajo(legajo):
            return {'message': "Ya existe un empleado con el legajo {}".format(legajo)}, 400

        #data = request.get_json()     #force=True significa que no se fijará en el Content-Type, asumirá que es un json #silent=True simplemente no da error, no devuelve nada
        data = Empleado.parser.parse_args()
        
        empleado = EmpleadoModel(legajo, data['nombre'])

        try:
            empleado.save_to_db()
        except:
            return {'message': 'Un error ocurrió insertando el empleado'}, 500

        return empleado.json(), 201

    @jwt_required()
    def delete(self, legajo):
        empleado = EmpleadoModel.find_by_legajo(legajo)
        
        if empleado:
            empleado.delete_to_db()
            return {'message': 'Empleado eliminado'}, 200

        return {'message': "No existe un empleado con el legajo {}".format(legajo)}, 404

    @jwt_required()
    def put(self, legajo):
        data = Empleado.parser.parse_args()

        empleado = EmpleadoModel.find_by_legajo(legajo)
        
        if empleado is None:
            empleado = EmpleadoModel(legajo, data['nombre'])
        else:
            empleado.nombre = data['nombre']

        empleado.save_to_db()
        return empleado.json(), 200


class ListEmpleado(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM empleado"
        result = cursor.execute(query)

        empleados = []

        for row in result:
            empleados.append({'legajo': row[1], 'nombre': row[2]})

        connection.close()

        return {'empleados': empleados}
        