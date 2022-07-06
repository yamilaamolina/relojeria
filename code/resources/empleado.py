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
            empleado.insert()
        except:
            return {'message': 'Un error ocurrió insertando el empleado'}, 500

        return empleado.json(), 201

    @jwt_required()
    def delete(self, legajo):
        if EmpleadoModel.find_by_legajo(legajo):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM empleado WHERE legajo = ?"
            cursor.execute(query, (legajo,))
            connection.commit()
            connection.close()

            return {'message': 'Empleado eliminado'}, 200

        return {'message': "No existe un empleado con el legajo {}".format(legajo)}, 404

    @jwt_required()
    def put(self, legajo):
        data = Empleado.parser.parse_args()
        empleado = EmpleadoModel.find_by_legajo(legajo)
        update_empleado = EmpleadoModel(legajo, data['nombre'])
        
        if empleado is None:
            try:
                update_empleado.insert()
            except:
                return {'message': 'Un error ocurrió insertando el Empleado'}, 500
        else:
            try:
                empleado.update()
            except:
                return {'message': 'Un error ocurrió actualizando el Empleado'}, 500

        return update_empleado.json(), 200


class ListEmpleado(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM empleado"
        result = cursor.execute(query)

        empleados = []

        for row in result:
            empleados.append({'legajo': row[0], 'nombre': row[1]})

        connection.close()

        return {'empleados': empleados}
        