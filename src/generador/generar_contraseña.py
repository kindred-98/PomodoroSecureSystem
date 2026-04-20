"""
Módulo: generar_contraseña.py
Responsabilidad: Generar contraseñas criptográficamente seguras
basadas en parámetros del usuario.
"""

import secrets
import string
from src.generador.asegurar_tipos_caracteres import asegurar_tipos_caracteres


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


def generar_contraseña_segura(longitud: int = 16) -> str:
    """
    Genera una contraseña segura automáticamente.
    
    Args:
        longitud (int): Entre 8 y 32. Por defecto 16.
    
    Returns:
        str: Contraseña segura aleatoria.
    """
    parametros = {
        'longitud': longitud,
        'usar_mayusculas': True,
        'usar_numeros': True,
        'usar_simbolos': True,
        'excluir_ambiguos': True,
    }
    return generar_contraseña(parametros)


def generar_contraseña_personalizada(semilla: str, longitud: int = 0) -> str:
    """
    Genera una contraseña fuerte usando 4 letras y 4 números de la semilla.
    
    La semilla debe tener al menos 4 letras distintas y 4 números distintos.
    Se usan exactamente 4 letras y 4 números (mezclados) para crear la contraseña.
    
    Args:
        semilla (str): Caracteres que el usuario quiere usar (mín 8 chars)
        longitud (int): Longitud deseada. Si 0, usa 16 por defecto.
    
    Returns:
        str: Contraseña generada con 4 letras + 4 números mezclados
    
    Raises:
        TypeError: Si semilla no es string
        ValueError: Si semilla no cumple requisitos
    """
    if not isinstance(semilla, str):
        raise TypeError(f"semilla debe ser string, recibido: {type(semilla).__name__}")
    if not semilla:
        raise ValueError("semilla no puede estar vacía")
    
    letras = [c for c in semilla.lower() if c.isalpha()]
    numeros = [c for c in semilla if c.isdigit()]
    
    letras_unicas = list(dict.fromkeys(letras))
    numeros_unicos = list(dict.fromkeys(numeros))
    
    if len(letras_unicas) < 4:
        raise ValueError(
            f"La semilla debe tener al menos 4 letras distintas. "
            f"Tienes {len(letras_unicas)}: {''.join(letras_unicas)}"
        )
    
    if len(numeros_unicos) < 4:
        raise ValueError(
            f"La semilla debe tener al menos 4 números distintos. "
            f"Tienes {len(numeros_unicos)}: {''.join(numeros_unicos)}"
        )
    
    if len(semilla) < 8:
        raise ValueError(
            f"La semilla debe tener al menos 8 caracteres. "
            f"Tienes {len(semilla)}"
        )
    
    letras_seleccionadas = letras_unicas[:4]
    numeros_seleccionados = numeros_unicos[:4]
    
    pool = letras_seleccionadas + numeros_seleccionados
    
    if longitud > 8:
        pool_extendido = pool * ((longitud // 8) + 1)
        pool = pool_extendido[:longitud]
    
    for i in range(len(pool) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        pool[i], pool[j] = pool[j], pool[i]
    
    return "".join(pool)
