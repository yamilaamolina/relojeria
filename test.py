import sqlite3

connection = sqlite3.connect('data.db') #string de conección

cursor = connection.cursor()

create_table = "CREATE TABLE user (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'Yamila', 'Yamila2021+')
insert_query = "INSERT INTO user VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Martin', 'Martin2021+'),
    (3, 'Alicia', 'Alicia2021+')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM user"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
