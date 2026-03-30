"""
Módulo: generar_contraseña.py
Responsabilidad: Generar contraseñas criptográficamente seguras
basadas en parámetros del usuario.
"""

import secrets
import string
from .asegurar_tipos_caracteres import asegurar_tipos_caracteres


def generar_contraseña(parametros: dict) -> str:
    """
    Genera una contraseña segura basada en parámetros especificados.
    
    Args:
        parametros (dict): Diccionario con configuración:
            - longitud (int): Entre 8 y 128
            - usar_mayusculas (bool): Incluir A-Z
            - usar_numeros (bool): Incluir 0-9
            - usar_simbolos (bool): Incluir !@#$%...
            - excluir_ambiguos (bool): Excluir 0,O,l,I,1
    
    Returns:
        str: Contraseña generada
        
    Raises:
        ValueError: Si longitud está fuera de rango (8-128)
        TypeError: Si parametros no es dict o faltan claves
    """
    # Validación de entrada
    if not isinstance(parametros, dict):
        raise TypeError("Los parámetros deben ser un diccionario")
    
    claves_requeridas = {"longitud", "usar_mayusculas", "usar_numeros", 
                         "usar_simbolos", "excluir_ambiguos"}
    claves_faltantes = claves_requeridas - set(parametros.keys())
    if claves_faltantes:
        raise ValueError(f"Faltan claves en parámetros: {claves_faltantes}")
    
    longitud = parametros["longitud"]
    
    if not isinstance(longitud, int) or longitud < 8 or longitud > 128:
        raise ValueError(f"Longitud debe estar entre 8 y 128, recibido: {longitud}")
    
    # Construir juego de caracteres
    juego_caracteres = string.ascii_lowercase
    
    if parametros["usar_mayusculas"]:
        juego_caracteres += string.ascii_uppercase
    if parametros["usar_numeros"]:
        juego_caracteres += string.digits
    if parametros["usar_simbolos"]:
        juego_caracteres += string.punctuation
    
    # Si se especifica excluir ambiguos, remover esos caracteres
    if parametros.get("excluir_ambiguos", False):
        caracteres_ambiguos = "0Ol1I"
        juego_caracteres = "".join(
            c for c in juego_caracteres if c not in caracteres_ambiguos
        )
    
    # Generar lista aleatoria de caracteres
    contraseña = [secrets.choice(juego_caracteres) for _ in range(longitud)]
    
    # Asegurar que hay al menos 1 de cada tipo seleccionado
    contraseña = asegurar_tipos_caracteres(contraseña, parametros)
    
    return "".join(contraseña)
