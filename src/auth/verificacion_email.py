"""
Módulo: verificacion_email.py
Responsabilidad: Sistema de verificación de email con token seguro.
"""

import secrets
import string
from datetime import datetime, timezone, timedelta
from src.db.conexion import conexion_global


def generar_token_verificacion(longitud: int = 6) -> str:
    """
    Genera un token numérico seguro para verificación de email.
    
    Args:
        longitud: Número de dígitos del token (default 6)
    
    Returns:
        str: Token numérico
    """
    digitos = string.digits
    token = ''.join(secrets.choice(digitos) for _ in range(longitud))
    return token


def crear_token_verificacion(email: str, expiracion_minutos: int = 30) -> dict:
    """
    Crea un token de verificación para un email.
    
    Args:
        email: Email del usuario a verificar
        expiracion_minutos: Minutos hasta expiración (default 30)
    
    Returns:
        dict: {
            'token': str,
            'expira': datetime,
            'email': str
        }
    """
    token = generar_token_verificacion(6)
    expira = datetime.now(timezone.utc) + timedelta(minutes=expiracion_minutos)
    
    # Guardar en BD
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    
    # Eliminar tokens anteriores para este email
    coleccion.delete_many({'email': email.lower()})
    
    # Insertar nuevo token
    documento = {
        'email': email.lower(),
        'token': token,
        'expira': expira,
        'creado': datetime.now(timezone.utc),
        'verificado': False
    }
    coleccion.insert_one(documento)
    
    return {
        'token': token,
        'expira': expira,
        'email': email.lower()
    }


def verificar_token(email: str, token: str) -> dict:
    """
    Verifica un token de verificación.
    
    Args:
        email: Email del usuario
        token: Token a verificar
    
    Returns:
        dict: {
            'valido': bool,
            'mensaje': str
        }
    """
    email = email.lower()
    
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    verificacion = coleccion.find_one({
        'email': email,
        'token': token,
        'verificado': False
    })
    
    if not verificacion:
        return {
            'valido': False,
            'mensaje': 'Token inválido o no encontrado'
        }
    
    # Verificar expiración
    expira = verificacion.get('expira')
    if isinstance(expira, datetime):
        if expira.tzinfo is None:
            expira = expira.replace(tzinfo=timezone.utc)
    
    if datetime.now(timezone.utc) > expira:
        return {
            'valido': False,
            'mensaje': 'Token expirado'
        }
    
    # Marcar como verificado
    coleccion.update_one(
        {'_id': verificacion['_id']},
        {'$set': {'verificado': True, 'verificado_en': datetime.now(timezone.utc)}}
    )
    
    return {
        'valido': True,
        'mensaje': 'Email verificado correctamente'
    }


def verificar_email_esta_verificado(email: str) -> bool:
    """
    Verifica si un email ya ha sido verificado.
    
    Args:
        email: Email a verificar
    
    Returns:
        bool: True si está verificado
    """
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    verificacion = coleccion.find_one({
        'email': email.lower(),
        'verificado': True
    })
    return verificacion is not None


def obtener_token_pendiente(email: str) -> dict | None:
    """
    Obtiene el token pendientes para un email.
    
    Args:
        email: Email a verificar
    
    Returns:
        dict | None: Token y expiration si existe
    """
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    verificacion = coleccion.find_one({
        'email': email.lower(),
        'verificado': False
    })
    
    if not verificacion:
        return None
    
    return {
        'token': verificacion['token'],
        'expira': verificacion['expira'],
        'email': verificacion['email']
    }


def limpiar_tokens_expirados():
    """Elimina tokens expirados de la BD."""
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    resultado = coleccion.delete_many({
        'expira': {'$lt': datetime.now(timezone.utc)},
        'verificado': False
    })
    return resultado.deleted_count