"""
Módulo: ver_contraseña.py
Responsabilidad: Ver la contraseña encriptada de un usuario.
Requiere validación de identidad (contraseña de login).
"""

from src.db.conexion import conexion_global
from src.seguridad.encriptacion import verificar_contraseña, descifrar


def ver_contraseña(usuario_id: str, contraseña_login: str) -> str:
    """
    Muestra la contraseña encriptada del usuario tras validación.
    
    El usuario debe introducir su contraseña de login para
    verificar su identidad antes de ver la contraseña almacenada.
    
    Args:
        usuario_id (str): ID del usuario
        contraseña_login (str): Contraseña de login para verificación
    
    Returns:
        str: Contraseña desencriptada
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si campos están vacíos o ID inválido
        Exception: Si validación falla o usuario no encontrado
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(contraseña_login, str):
        raise TypeError(f"contraseña_login debe ser string, recibido: {type(contraseña_login).__name__}")
    
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if not contraseña_login:
        raise ValueError("contraseña_login no puede estar vacía")
    
    from bson import ObjectId
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': objeto_id})
    
    if usuario is None:
        raise Exception("Usuario no encontrado")
    
    # Verificar identidad con contraseña de login
    hash_almacenado = usuario.get('contraseña_hash', '')
    if not verificar_contraseña(contraseña_login, hash_almacenado):
        raise Exception("Contraseña de verificación incorrecta")
    
    # Desencriptar y retornar
    contraseña_encriptada = usuario.get('contraseña_encriptada', '')
    if not contraseña_encriptada:
        raise Exception("No hay contraseña encriptada almacenada")
    
    return descifrar(contraseña_encriptada)
