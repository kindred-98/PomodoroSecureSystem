"""
Módulo: desactivar_usuario.py
Responsabilidad: Desactivar un usuario (soft delete).
"""

from bson import ObjectId
from ..conexion import conexion_global


def desactivar_usuario(usuario_id: str) -> dict:
    """
    Desactiva un usuario sin eliminar sus datos (soft delete).
    
    Args:
        usuario_id (str): ID del usuario a desactivar
    
    Returns:
        dict: Documento actualizado del usuario (con activo=False)
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si usuario_id no es string
        Exception: Si usuario no existe
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"ID inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    resultado = coleccion.find_one_and_update(
        {'_id': objeto_id},
        {'$set': {'activo': False}},
        return_document=True
    )
    
    if resultado is None:
        raise Exception(f"Usuario con ID '{usuario_id}' no existe")
    
    return resultado
