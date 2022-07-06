import sqlite3
from sqlite3.dbapi2 import Cursor, connect
from flask_restful import Resource, reqparse
from models.user import UserModel

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

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message": "Ya existe un usuario con ese username."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO user VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'])) #siempre tupla

        connection.commit()
        connection.close()

        return {"message": "El usuario se creó correctamente."}, 201
