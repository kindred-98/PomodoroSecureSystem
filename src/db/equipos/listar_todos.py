"""
Módulo: listar_todos.py
Responsabilidad: Listar todos los equipos.
"""

from src.db.conexion import conexion_global


def listar_todos() -> list:
    """
    Lista todos los equipos.
    
    Returns:
        list: Lista de documentos de equipos
    """
    coleccion = conexion_global.obtener_coleccion('equipos')
    return list(coleccion.find())
