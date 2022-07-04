from os import close
import sqlite3
from sqlite3.dbapi2 import Cursor, connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask_cors import cross_origin

class Empleado(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('nombre', 
        type=str, 
        required=True, 
        help="Este campo no puede dejarse vacío"
    )

    def get(self, legajo):
        empleado = self.find_by_legajo(legajo)

        if empleado:
            return empleado

        return {'message': 'Empleado no encontrado'}, 404

    @cross_origin
    @jwt_required()
    def post(self, legajo):
        if self.find_by_legajo(legajo):
            return {'message': "Ya existe un empleado con el legajo {}".format(legajo)}, 400

        #data = request.get_json()     #force=True significa que no se fijará en el Content-Type, asumirá que es un json #silent=True simplemente no da error, no devuelve nada
        data = Empleado.parser.parse_args()
        
        empleado = {'legajo': legajo, 'nombre': data['nombre']}

        try:
            self.insert(empleado)
        except:
            return {'message': 'Un error ocurrió insertando el empleado'}, 500

        return empleado, 201

    @cross_origin
    @jwt_required()
    def delete(self, legajo):
        if self.find_by_legajo(legajo):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM empleado WHERE legajo = ?"
            cursor.execute(query, (legajo,))
            connection.commit()
            connection.close()

            return {'message': 'Empleado eliminado'}, 200

        return {'message': "No existe un empleado con el legajo {}".format(legajo)}, 404

    @cross_origin
    @jwt_required()
    def put(self, legajo):
        data = Empleado.parser.parse_args()
        empleado = self.find_by_legajo(legajo)
        update_empleado = {'legajo': legajo, 'nombre': data['nombre']}
        
        try:
            if empleado:
                self.update(update_empleado)
            else:
                self.insert(update_empleado)
        except:
            return {'message': 'Oucrrió un error en el servidor'}, 500
        
        return update_empleado, 200

    @classmethod
    def find_by_legajo(cls, legajo):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM empleado WHERE legajo = ?"
        result = cursor.execute(query, (legajo,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'empleado': {'legajo': row[0], 'nombre': row[1]}}, 200 

    @classmethod
    def insert(cls, empleado):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO empleado VALUES (?, ?)"
        cursor.execute(query, (empleado['legajo'], empleado['nombre']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, empleado):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE empleado SET nombre = ? WHERE legajo = ?"
        cursor.execute(query, (empleado['legajo'], empleado['nombre']))
        connection.commit()
        connection.close()

class ListEmpleado(Resource):
    @cross_origin
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
        