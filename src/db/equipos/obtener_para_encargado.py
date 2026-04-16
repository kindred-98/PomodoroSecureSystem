"""
Módulo: obtener_para_encargado.py
Responsabilidad: Obtener equipos asignados a un encargado (donde fue asignado).
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def obtener_para_encargado(encargado_id: str) -> list:
    """
    Obtiene todos los equipos donde el encargado fue asignado.
    Esto incluye equipos creados por supervisores y luego asignados.
    
    Args:
        encargado_id (str): ID del encargado
    
    Returns:
        list: Lista de documentos (equipos del encargado)
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si encargado_id no es string
    """
    if not isinstance(encargado_id, str):
        raise TypeError(f"encargado_id debe ser string, recibido: {type(encargado_id).__name__}")
    
    try:
        objeto_id = ObjectId(encargado_id)
    except Exception:  # nosec B110
        raise ValueError(f"ID inválido: '{encargado_id}'")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    equipos = list(coleccion.find({'encargado_id': objeto_id}))
    
    return equipos