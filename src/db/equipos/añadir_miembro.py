"""
Módulo: añadir_miembro.py
Responsabilidad: Agregar un usuario a un equipo.
"""

from bson import ObjectId
from ..conexion import conexion_global


def añadir_miembro(equipo_id: str, usuario_id: str) -> dict:
    """
    Agrega un usuario como miembro de un equipo.
    
    Args:
        equipo_id (str): ID del equipo
        usuario_id (str): ID del usuario a agregar
    
    Returns:
        dict: Documento del equipo actualizado
        
    Raises:
        ValueError: Si ID inválido
        TypeError: Si tipos incorrectos
        Exception: Si equipo/usuario no existe o usuario ya es miembro
    """
    if not isinstance(equipo_id, str):
        raise TypeError(f"equipo_id debe ser string, recibido: {type(equipo_id).__name__}")
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    
    try:
        equipo_objeto_id = ObjectId(equipo_id)
        usuario_objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"IDs inválidos: equipo='{equipo_id}', usuario='{usuario_id}'")
    
    # Verificar que equipo existe
    coleccion_equipos = conexion_global.obtener_coleccion('equipos')
    equipo = coleccion_equipos.find_one({'_id': equipo_objeto_id})
    if equipo is None:
        raise Exception(f"Equipo con ID '{equipo_id}' no existe")
    
    # Verificar que usuario existe
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion_usuarios.find_one({'_id': usuario_objeto_id})
    if usuario is None:
        raise Exception(f"Usuario con ID '{usuario_id}' no existe")
    
    # Verificar que no sea duplicado
    if usuario_objeto_id in equipo['miembros']:
        raise Exception(f"Usuario '{usuario_id}' ya es miembro del equipo")
    
    # Agregar miembro
    resultado = coleccion_equipos.find_one_and_update(
        {'_id': equipo_objeto_id},
        {'$push': {'miembros': usuario_objeto_id}},
        return_document=True
    )
    
    return resultado
