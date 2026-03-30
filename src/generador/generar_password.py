import secrets
import string
from .asegurar_tipos import asegurar_tipos

def generar_password(parametros: dict) -> str:
    longitud = parametros["longitud"]

    charset = string.ascii_lowercase

    if parametros["usar_mayusculas"]:
        charset += string.ascii_uppercase
    if parametros["usar_numeros"]:
        charset += string.digits
    if parametros["usar_simbolos"]:
        charset += string.punctuation

    password = [secrets.choice(charset) for _ in range(longitud)]

    password = asegurar_tipos(password, parametros)

    return "".join(password)