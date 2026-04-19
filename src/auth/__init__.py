"""
Módulo: auth/__init__.py
Responsabilidad: Exportar funciones de autenticación y gestión de contraseñas.
"""

from src.auth.registro import registrar_usuario
from src.auth.login import iniciar_sesion
from src.auth.logout import cerrar_sesion
from src.auth.sesion import crear_sesion, verificar_sesion, cerrar_sesion_por_token
from src.auth.ver_contraseña import ver_contraseña
from src.auth.regenerar_contraseña import regenerar_contraseña
from src.auth.cambiar_contraseña import cambiar_contraseña
from src.auth.exportar_contraseña import exportar_contraseña
from src.auth.verificacion_email import (
    crear_token_verificacion,
    verificar_token,
    verificar_email_esta_verificado,
    obtener_token_pendiente,
)

def obtener_contraseña(usuario_id: str) -> str:
    """
    Obtiene la contraseña desencriptada del usuario.
    Sin verificación (el usuario ya está autenticado).
    """
    from bson import ObjectId
    from src.db.conexion import conexion_global
    from src.seguridad.encriptacion import descifrar
    
    try:
        oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError("ID inválido")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': oid})
    
    if not usuario:
        raise Exception("Usuario no encontrado")
    
    return descifrar(usuario.get('contraseña_encriptada', ''))

__all__ = [
    "registrar_usuario",
    "iniciar_sesion",
    "cerrar_sesion",
    "crear_sesion",
    "verificar_sesion",
    "cerrar_sesion_por_token",
    "ver_contraseña",
    "regenerar_contraseña",
    "cambiar_contraseña",
    "exportar_contraseña",
    "obtener_contraseña",
    "crear_token_verificacion",
    "verificar_token",
    "verificar_email_esta_verificado",
    "obtener_token_pendiente",
]
