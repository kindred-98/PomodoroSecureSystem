"""
Módulo: encriptacion.py
Responsabilidad: Funciones de encriptación y hashing para el sistema.
- bcrypt: hash irreversible para verificación de login
- Fernet: encriptación reversible para recuperación de contraseñas
"""

import os
import bcrypt
from cryptography.fernet import Fernet


def hashear_contraseña(contraseña: str) -> str:
    """
    Genera un hash bcrypt de una contraseña.
    
    Args:
        contraseña (str): Contraseña en texto plano
    
    Returns:
        str: Hash bcrypt (verificable, no reversible)
    
    Raises:
        TypeError: Si contraseña no es string
        ValueError: Si contraseña está vacía
    """
    if not isinstance(contraseña, str):
        raise TypeError(
            f"contraseña debe ser string, recibido: {type(contraseña).__name__}"
        )
    if not contraseña:
        raise ValueError("La contraseña no puede estar vacía")
    
    bytes_contraseña = contraseña.encode('utf-8')
    hash_bytes = bcrypt.hashpw(bytes_contraseña, bcrypt.gensalt(rounds=12))
    return hash_bytes.decode('utf-8')


def verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool:
    """
    Verifica si una contraseña coincide con un hash bcrypt.
    
    Args:
        contraseña (str): Contraseña en texto plano a verificar
        hash_almacenado (str): Hash bcrypt almacenado
    
    Returns:
        bool: True si coincide, False si no
    """
    if not isinstance(contraseña, str) or not isinstance(hash_almacenado, str):
        return False
    
    try:
        return bcrypt.checkpw(
            contraseña.encode('utf-8'),
            hash_almacenado.encode('utf-8')
        )
    except (ValueError, Exception):
        return False


def cifrar(texto: str) -> str:
    """
    Encripta un texto usando Fernet (AES-128-CBC + HMAC-SHA256).
    
    La clave se obtiene de la variable de entorno FERNET_KEY.
    
    Args:
        texto (str): Texto a encriptar
    
    Returns:
        str: Texto encriptado (base64)
    
    Raises:
        TypeError: Si texto no es string
        ValueError: Si texto vacío o FERNET_KEY no configurada
    """
    if not isinstance(texto, str):
        raise TypeError(f"texto debe ser string, recibido: {type(texto).__name__}")
    if not texto:
        raise ValueError("El texto no puede estar vacío")
    
    clave = os.getenv('FERNET_KEY')
    if not clave:
        raise ValueError(
            "FERNET_KEY no configurada en variables de entorno"
        )
    
    fernet = Fernet(clave.encode() if isinstance(clave, str) else clave)
    texto_bytes = texto.encode('utf-8')
    texto_cifrado = fernet.encrypt(texto_bytes)
    return texto_cifrado.decode('utf-8')


def descifrar(texto_cifrado: str) -> str:
    """
    Desencripta un texto previamente cifrado con Fernet.
    
    Args:
        texto_cifrado (str): Texto encriptado (base64)
    
    Returns:
        str: Texto original desencriptado
    
    Raises:
        TypeError: Si texto_cifrado no es string
        ValueError: Si texto vacío, clave no configurada o texto inválido
    """
    if not isinstance(texto_cifrado, str):
        raise TypeError(
            f"texto_cifrado debe ser string, recibido: {type(texto_cifrado).__name__}"
        )
    if not texto_cifrado:
        raise ValueError("El texto cifrado no puede estar vacío")
    
    clave = os.getenv('FERNET_KEY')
    if not clave:
        raise ValueError(
            "FERNET_KEY no configurada en variables de entorno"
        )
    
    try:
        fernet = Fernet(clave.encode() if isinstance(clave, str) else clave)
        texto_bytes = texto_cifrado.encode('utf-8')
        texto_descifrado = fernet.decrypt(texto_bytes)
        return texto_descifrado.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error al descifrar: texto inválido o clave incorrecta: {e}")


def generar_token_sesion() -> str:
    """
    Genera un token de sesión criptográficamente seguro.
    
    Returns:
        str: Token hexadecimal de 64 caracteres
    """
    import secrets
    return secrets.token_hex(32)
