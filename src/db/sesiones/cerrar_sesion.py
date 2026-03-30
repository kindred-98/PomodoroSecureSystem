"""
Módulo: cerrar_sesion.py
Responsabilidad: Cerrar una sesión de trabajo.
"""

from datetime import datetime
from bson import ObjectId
from ..conexion import conexion_global


def cerrar_sesion(sesion_id: str, completada: bool = True) -> dict:
    """
    Cierra una sesión y calcula su duración.
    
    Args:
        sesion_id (str): ID de la sesión
        completada (bool): Si la sesión fue completada exitosamente
    
    Returns:
        dict: Documento de sesión cerrada
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si tipos incorrectos
        Exception: Si sesión no existe
    """
    if not isinstance(sesion_id, str):
        raise TypeError(f"sesion_id debe ser string, recibido: {type(sesion_id).__name__}")
    if not isinstance(completada, bool):
        raise TypeError(f"completada debe ser bool, recibido: {type(completada).__name__}")
    
    try:
        objeto_id = ObjectId(sesion_id)
    except Exception:
        raise ValueError(f"ID inválido: '{sesion_id}'")
    
    coleccion = conexion_global.obtener_coleccion('sesiones')
    sesion = coleccion.find_one({'_id': objeto_id})
    
    if sesion is None:
        raise Exception(f"Sesión con ID '{sesion_id}' no existe")
    
    # Calcular duración
    fin = datetime.utcnow()
    duracion = (fin - sesion['inicio']).total_seconds()
    
    # Actualizar
    resultado = coleccion.find_one_and_update(
        {'_id': objeto_id},
        {'$set': {
            'fin': fin,
            'duracion_segundos': int(duracion),
            'completada': completada
        }},
        return_document=True
    )
    
    return resultado
