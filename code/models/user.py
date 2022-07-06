import sqlite3

class UserModel:
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