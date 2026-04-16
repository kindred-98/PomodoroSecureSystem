"""
Módulo: obtener_miembros.py
Responsabilidad: Obtener lista de miembros de un equipo.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def obtener_miembros(equipo_id: str) -> list:
    """
    Obtiene lista de miembros de un equipo.
    
    Args:
        equipo_id (str): ID del equipo
    
    Returns:
        list: Lista de documentos de usuarios (miembros del equipo)
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si equipo_id no es string
        Exception: Si equipo no existe
    """
    if not isinstance(equipo_id, str):
        raise TypeError(f"equipo_id debe ser string, recibido: {type(equipo_id).__name__}")
    
    try:
        objeto_id = ObjectId(equipo_id)
    except Exception:  # nosec B110
        raise ValueError(f"ID inválido: '{equipo_id}'")
    
    coleccion_equipos = conexion_global.obtener_coleccion('equipos')
    equipo = coleccion_equipos.find_one({'_id': objeto_id})
    
    if equipo is None:
        raise Exception(f"Equipo con ID '{equipo_id}' no existe")
    
    # Obtener detalles de los miembros
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    miembros = list(coleccion_usuarios.find({'_id': {'$in': equipo['miembros']}}))
    
    return miembros
