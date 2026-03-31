"""
Módulo: sesion.py
Responsabilidad: Gestión de sesiones activas de usuario.
"""

from datetime import datetime, timezone
from ..db.conexion import conexion_global


def crear_sesion(usuario_id: str, token_sesion: str) -> dict:
    """
    Crea una nueva sesión activa para un usuario.
    
    Args:
        usuario_id (str): ID del usuario
        token_sesion (str): Token de sesión generado
    
    Returns:
        dict: Documento de la sesión creada
    
    Raises:
        TypeError: Si los tipos son incorrectos
        ValueError: Si los campos están vacíos
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(token_sesion, str):
        raise TypeError(f"token_sesion debe ser string, recibido: {type(token_sesion).__name__}")
    
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if not token_sesion.strip():
        raise ValueError("token_sesion no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    sesion = {
        'usuario_id': usuario_oid,
        'token_sesion': token_sesion,
        'inicio': datetime.now(timezone.utc),
        'activa': True,
    }
    
    coleccion = conexion_global.obtener_coleccion('sesiones_auth')
    resultado = coleccion.insert_one(sesion)
    sesion['_id'] = resultado.inserted_id
    
    return sesion


def verificar_sesion(token_sesion: str) -> dict:
    """
    Verifica si un token de sesión es válido y retorna el usuario.
    
    Args:
        token_sesion (str): Token de sesión a verificar
    
    Returns:
        dict: Documento del usuario asociado a la sesión
    
    Raises:
        TypeError: Si token_sesion no es string
        ValueError: Si token_sesion está vacío
        Exception: Si sesión inválida, expirada o usuario inactivo
    """
    if not isinstance(token_sesion, str):
        raise TypeError(f"token_sesion debe ser string, recibido: {type(token_sesion).__name__}")
    if not token_sesion.strip():
        raise ValueError("token_sesion no puede estar vacío")
    
    coleccion_sesiones = conexion_global.obtener_coleccion('sesiones_auth')
    sesion = coleccion_sesiones.find_one({
        'token_sesion': token_sesion,
        'activa': True
    })
    
    if sesion is None:
        raise Exception("Sesión inválida o expirada")
    
    # Verificar expiración (8 horas)
    inicio = sesion.get('inicio')
    if inicio:
        ahora = datetime.now(timezone.utc)
        # Manejar datetime naive de mongomock
        if hasattr(ahora, 'tzinfo') and ahora.tzinfo is not None:
            if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None:
                ahora = ahora.replace(tzinfo=None)
        diferencia = (ahora - inicio).total_seconds()
        if diferencia > 28800:  # 8 horas
            # Marcar sesión como inactiva
            coleccion_sesiones.update_one(
                {'_id': sesion['_id']},
                {'$set': {'activa': False}}
            )
            raise Exception("Sesión expirada")
    
    # Obtener usuario
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion_usuarios.find_one({'_id': sesion['usuario_id']})
    
    if usuario is None or not usuario.get('activo', False):
        raise Exception("Usuario inactivo o no encontrado")
    
    return usuario


def cerrar_sesion_por_token(token_sesion: str) -> bool:
    """
    Cierra una sesión activa por su token.
    
    Args:
        token_sesion (str): Token de la sesión a cerrar
    
    Returns:
        bool: True si se cerró correctamente
    
    Raises:
        TypeError: Si token_sesion no es string
        ValueError: Si token_sesion está vacío
        Exception: Si sesión no existe o ya está cerrada
    """
    if not isinstance(token_sesion, str):
        raise TypeError(f"token_sesion debe ser string, recibido: {type(token_sesion).__name__}")
    if not token_sesion.strip():
        raise ValueError("token_sesion no puede estar vacío")
    
    coleccion = conexion_global.obtener_coleccion('sesiones_auth')
    sesion = coleccion.find_one({'token_sesion': token_sesion})
    
    if sesion is None:
        raise Exception("Sesión no encontrada")
    
    if not sesion.get('activa', False):
        raise Exception("La sesión ya está cerrada")
    
    coleccion.update_one(
        {'_id': sesion['_id']},
        {'$set': {'activa': False}}
    )
    
    return True
