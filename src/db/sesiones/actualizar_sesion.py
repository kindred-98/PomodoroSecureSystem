"""
Módulo: actualizar_sesion.py
Responsabilidad: Actualizar datos de una sesión activa.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def actualizar_sesion(sesion_id: str, actualizaciones: dict) -> dict:
    """
    Actualiza los datos de una sesión.
    
    Args:
        sesion_id (str): ID de la sesión
        actualizaciones (dict): Campos a actualizar
                               (ej: {'pausas_utilizadas': 1})
    
    Returns:
        dict: Documento de sesión actualizado
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si tipos incorrectos
        Exception: Si sesión no existe
    """
    if not isinstance(sesion_id, str):
        raise TypeError(f"sesion_id debe ser string, recibido: {type(sesion_id).__name__}")
    if not isinstance(actualizaciones, dict):
        raise TypeError(f"actualizaciones debe ser dict, recibido: {type(actualizaciones).__name__}")
    
    try:
        objeto_id = ObjectId(sesion_id)
    except Exception:
        raise ValueError(f"ID inválido: '{sesion_id}'")
    
    coleccion = conexion_global.obtener_coleccion('sesiones')
    resultado = coleccion.find_one_and_update(
        {'_id': objeto_id},
        {'$set': actualizaciones},
        return_document=True
    )
    
    if resultado is None:
        raise Exception(f"Sesión con ID '{sesion_id}' no existe")
    
    return resultado
