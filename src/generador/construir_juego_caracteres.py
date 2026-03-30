"""
Módulo: construir_juego_caracteres.py
Responsabilidad: Construir dinámicamente el juego de caracteres
basado en los parámetros especificados.
"""

import string


def construir_juego_caracteres(parametros: dict) -> str:
    """
    Construye un conjunto de caracteres válidos basado en parámetros.
    
    Args:
        parametros (dict): Diccionario con configuración:
            - usar_mayusculas (bool): Incluir A-Z
            - usar_numeros (bool): Incluir 0-9
            - usar_simbolos (bool): Incluir !@#$%...
            - excluir_ambiguos (bool): Excluir 0,O,l,I,1
    
    Returns:
        str: Juego de caracteres permitidos
        
    Raises:
        TypeError: Si parametros no es dict o faltan claves
        ValueError: Si no se solicita al menos un tipo de carácter
    """
    # Validación de entrada
    if not isinstance(parametros, dict):
        raise TypeError("Los parámetros deben ser un diccionario")
    
    claves_requeridas = {"usar_mayusculas", "usar_numeros", 
                         "usar_simbolos", "excluir_ambiguos"}
    claves_faltantes = claves_requeridas - set(parametros.keys())
    if claves_faltantes:
        raise ValueError(f"Faltan claves en parámetros: {claves_faltantes}")
    
    # Validar que todos los valores sean booleanos
    for clave, valor in parametros.items():
        if not isinstance(valor, bool):
            raise TypeError(f"El parámetro '{clave}' debe ser bool, "
                          f"recibido: {type(valor).__name__}")
    
    # Comenzar con minúsculas (siempre presente)
    juego_caracteres = string.ascii_lowercase
    
    # Agregar tipos solicitados
    if parametros["usar_mayusculas"]:
        juego_caracteres += string.ascii_uppercase
    
    if parametros["usar_numeros"]:
        juego_caracteres += string.digits
    
    if parametros["usar_simbolos"]:
        juego_caracteres += string.punctuation
    
    # Excluir caracteres ambiguos si se solicita
    if parametros.get("excluir_ambiguos", False):
        caracteres_ambiguos = "0Ol1I"
        juego_caracteres = "".join(
            c for c in juego_caracteres if c not in caracteres_ambiguos
        )
        
        # Validar que aún haya caracteres disponibles
        if not juego_caracteres:
            raise ValueError(
                "No hay caracteres disponibles después de excluir ambiguos"
            )
    
    return juego_caracteres
