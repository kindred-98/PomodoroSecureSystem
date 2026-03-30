"""
Módulo: construir_juego_caracteres.py
Responsabilidad: Construir dinámicamente el juego de caracteres
disponibles según los parámetros del usuario
"""

import string


def construir_juego_caracteres(
    usar_mayusculas: bool,
    usar_numeros: bool,
    usar_simbolos: bool,
    excluir_ambiguos: bool
) -> str:
    """
    Construye dinámicamente el juego de caracteres disponibles.
    
    Args:
        usar_mayusculas (bool): Incluir A-Z
        usar_numeros (bool): Incluir 0-9
        usar_simbolos (bool): Incluir !@#$%...
        excluir_ambiguos (bool): Excluir 0,O,l,I,1
        
    Returns:
        str: String con todos los caracteres disponibles
    """
    # TODO: Construir el juego de caracteres según parámetros
    pass