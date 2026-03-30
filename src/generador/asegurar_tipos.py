import secrets
import string

def asegurar_tipos(password: list, parametros: dict) -> list:
    if parametros["usar_mayusculas"]:
        password[0] = secrets.choice(string.ascii_uppercase)

    if parametros["usar_numeros"]:
        password[1] = secrets.choice(string.digits)

    if parametros["usar_simbolos"]:
        password[2] = secrets.choice(string.punctuation)

    return password