import sqlite3

class EmpleadoModel:
    def __init__(self, legajo, nombre):
        self.legajo = legajo
        self.nombre = nombre

    def json(self):
        return {'nombre': self.nombre, 'legajo': self.legajo}

    @classmethod
    def find_by_legajo(cls, legajo):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM empleado WHERE legajo = ?"
        result = cursor.execute(query, (legajo,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row) #row[0], row[1]

    def insert(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO empleado VALUES (?, ?)"
        cursor.execute(query, (self.legajo, self.nombre))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE empleado SET nombre = ? WHERE legajo = ?"
        cursor.execute(query, (self.legajo, self.nombre))
        connection.commit()
        connection.close()