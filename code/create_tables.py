import sqlite3
from sqlite3.dbapi2 import Cursor

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS empleado (id INTEGER PRIMARY KEY, legajo text, nombre text)"
cursor.execute(create_table)

connection.commit()

connection.close()