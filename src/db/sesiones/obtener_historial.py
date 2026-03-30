"""
Módulo: obtener_historial.py
Responsabilidad: Obtener historial de sesiones de un usuario.
"""

from bson import ObjectId
from ..conexion import conexion_global


def obtener_historial(usuario_id: str, limite: int = 50) -> list:
    """
    Obtiene el historial de sesiones de un usuario.
    
    Args:
        usuario_id (str): ID del usuario
        limite (int): Máximo número de sesiones a retornar (ordena por más recientes)
    
    Returns:
        list: Lista de documentos (sesiones del usuario, más recientes primero)
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si tipos incorrectos
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(limite, int):
        raise TypeError(f"limite debe ser int, recibido: {type(limite).__name__}")
    
    if limite <= 0:
        raise ValueError(f"limite debe ser > 0, recibido: {limite}")
    
    try:
        usuario_objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('sesiones')
    sesiones = list(
        coleccion.find({'usuario_id': usuario_objeto_id})
        .sort('inicio', -1)  # Más recientes primero
        .limit(limite)
    )
    
    return sesiones
