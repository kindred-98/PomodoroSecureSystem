"""
Módulo: obtener_por_supervisor.py
Responsabilidad: Obtener equipos creados por un supervisor.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def obtener_por_supervisor(supervisor_id: str) -> list:
    """
    Obtiene todos los equipos creados por un supervisor específico.
    
    Args:
        supervisor_id (str): ID del supervisor
    
    Returns:
        list: Lista de documentos (equipos del supervisor)
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si supervisor_id no es string
    """
    if not isinstance(supervisor_id, str):
        raise TypeError(f"supervisor_id debe ser string, recibido: {type(supervisor_id).__name__}")
    
    try:
        objeto_id = ObjectId(supervisor_id)
    except Exception:
        raise ValueError(f"ID inválido: '{supervisor_id}'")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    equipos = list(coleccion.find({'supervisor_id': objeto_id}))
    
    return equipos