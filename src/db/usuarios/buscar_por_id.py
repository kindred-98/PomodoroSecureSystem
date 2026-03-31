"""
Módulo: buscar_por_id.py
Responsabilidad: Buscar un usuario por su ID.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def buscar_por_id(usuario_id: str) -> dict:
    """
    Busca un usuario por su ID de MongoDB.
    
    Args:
        usuario_id (str): ID del usuario (formato ObjectId string)
    
    Returns:
        dict: Documento del usuario si existe, None si no existe
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si usuario_id no es string
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"ID inválido: '{usuario_id}' no es un ObjectId válido")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': objeto_id})
    
    return usuario
