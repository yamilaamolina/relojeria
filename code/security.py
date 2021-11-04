from werkzeug.security import safe_str_cmp   #comparar cadenas de forma segura para cadenas con cifrado no den problema

from user import User

users = [
    User(1, 'Yamila', 'Yamila2021+'),
    User(2, 'Martin', 'Martin2021+')
]

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

