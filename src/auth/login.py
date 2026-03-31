"""
Módulo: login.py
Responsabilidad: Autenticación de usuarios con email y contraseña.
"""

from datetime import datetime, timezone
from src.db.conexion import conexion_global
from src.seguridad.encriptacion import verificar_contraseña, generar_token_sesion
from src.auth.sesion import crear_sesion


def iniciar_sesion(email: str, contraseña: str) -> dict:
    """
    Autentica un usuario y crea una sesión activa.
    
    Flujo:
    1. Busca usuario por email
    2. Verifica contraseña contra hash bcrypt
    3. Actualiza último acceso
    4. Genera token de sesión
    5. Retorna usuario + token
    
    Args:
        email (str): Email del usuario
        contraseña (str): Contraseña en texto plano
    
    Returns:
        dict: {
            'usuario': dict,
            'token_sesion': str
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si campos están vacíos
        Exception: Si credenciales incorrectas o usuario inactivo
    """
    # Validación de tipos
    if not isinstance(email, str):
        raise TypeError(f"email debe ser string, recibido: {type(email).__name__}")
    if not isinstance(contraseña, str):
        raise TypeError(f"contraseña debe ser string, recibido: {type(contraseña).__name__}")
    
    email = email.strip()
    
    if not email:
        raise ValueError("email no puede estar vacío")
    if not contraseña:
        raise ValueError("contraseña no puede estar vacía")
    
    # Buscar usuario por email
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion_usuarios.find_one({'email': email})
    
    if usuario is None:
        raise Exception("Credenciales incorrectas")
    
    # Verificar que está activo
    if not usuario.get('activo', True):
        raise Exception("Usuario desactivado")
    
    # Verificar contraseña
    hash_almacenado = usuario.get('contraseña_hash', '')
    if not verificar_contraseña(contraseña, hash_almacenado):
        raise Exception("Credenciales incorrectas")
    
    # Actualizar último acceso
    coleccion_usuarios.update_one(
        {'_id': usuario['_id']},
        {'$set': {'ultimo_acceso': datetime.now(timezone.utc)}}
    )
    
    # Generar token y crear sesión
    token_sesion = generar_token_sesion()
    crear_sesion(str(usuario['_id']), token_sesion)
    
    return {
        'usuario': usuario,
        'token_sesion': token_sesion
    }
