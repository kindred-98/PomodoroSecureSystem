"""
Módulo: buscar_por_id.py
Responsabilidad: Buscar un equipo por su ID.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def buscar_por_id(equipo_id: str) -> dict:
    """
    Busca un equipo por su ID.
    
    Args:
        equipo_id (str): ID del equipo
    
    Returns:
        dict: Documento del equipo si existe, None si no existe
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si equipo_id no es string
    """
    if not isinstance(equipo_id, str):
        raise TypeError(f"equipo_id debe ser string, recibido: {type(equipo_id).__name__}")
    
    try:
        objeto_id = ObjectId(equipo_id)
    except Exception:
        raise ValueError(f"ID inválido: '{equipo_id}'")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    equipo = coleccion.find_one({'_id': objeto_id})
    
    return equipo
