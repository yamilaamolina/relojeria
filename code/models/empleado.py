import sqlite3
from db import db

class EmpleadoModel(db.Model):
    __tablename__ = 'empleado'

    id = db.Column(db.Integer, primary_key = True)
    legajo = db.Column(db.String(4))
    nombre = db.Column(db.String(80))

    def __init__(self, legajo, nombre):
        self.legajo = legajo
        self.nombre = nombre

    def json(self):
        return {'nombre': self.nombre, 'legajo': self.legajo}

    @classmethod
    def find_by_legajo(cls, legajo):
        return cls.query.filter_by(legajo=legajo).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()
