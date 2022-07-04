import sqlite3
from sqlite3.dbapi2 import Cursor, connect
from flask_restful import Resource, reqparse
from flask_cors import cross_origin

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db') #string de conección
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone() #solo trae la primera fila

        if row:
            user = cls(*row)   #row[0], row[1], row[2]
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db') #string de conección
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone() #solo trae la primera fila

        if row:
            user = cls(*row)   #row[0], row[1], row[2]
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str, 
        required=True, 
        help="Este campo no puede dejarse vacío."
    )
    parser.add_argument('password', 
        type=str, 
        required=True, 
        help="Este campo no puede dejarse vacío."
    )

    @cross_origin
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {"message": "Ya existe un usuario con ese username."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO user VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'])) #siempre tupla

        connection.commit()
        connection.close()

        return {"message": "El usuario se creó correctamente."}, 201
