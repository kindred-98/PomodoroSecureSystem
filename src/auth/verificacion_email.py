"""
Módulo: verificacion_email.py
Responsabilidad: Sistema de verificación de email con token seguro.
"""

import secrets
import string
import time
import hashlib
from datetime import datetime, timezone, timedelta
from bson import ObjectId


def generar_token(longitud: int = 6) -> str:
    """
    Genera un token numérico aleatorio.
    """
    digitos = string.digits
    return ''.join(secrets.choice(digitos) for _ in range(longitud))


def hash_token(token: str) -> str:
    """
    Genera hash del token para almacenar de forma segura.
    """
    return hashlib.sha256(token.encode()).hexdigest()


def verificar_token_hash(token_input: str, token_hash: str) -> bool:
    """Verifica si el token coincide con el hash."""
    return hash_token(token_input) == token_hash


def crear_o_actualizar_verificacion(email: str, expiracion_minutos: int = 5, max_intentos: int = 5) -> str:
    """
    Crea o actualiza un token de verificación para un email.
    
    Args:
        email: Email del usuario
        expiracion_minutos: Minutos hasta expiración (default 5)
        max_intentos: Intentos máximos (default 5)
    
    Returns:
        str: Token para enviar al usuario
    """
    from src.db.conexion import conexion_global
    
    token = generar_token(6)
    token_hash = hash_token(token)
    unixtime = int(time.time())
    expira = unixtime + (expiracion_minutos * 60)
    
    documento = {
        'email': email.lower(),
        'token_hash': token_hash,
        'expira': expira,
        'intentos': 0,
        'max_intentos': max_intentos,
        'creado_en': unixtime,
        'bloqueado_hasta': None
    }
    
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    
    # Eliminar verificación anterior si existe
    coleccion.delete_one({'email': email.lower()})
    
    # Insertar nuevo token
    coleccion.insert_one(documento)
    
    return token


def verificar_token_db(email: str, token_input: str) -> dict:
    """
    Verifica un token de verificación.
    
    Args:
        email: Email del usuario
        token_input: Token introducido por el usuario
    
    Returns:
        dict: {'valido': bool, 'mensaje': str}
    """
    from src.db.conexion import conexion_global
    
    email = email.lower()
    unixtime = int(time.time())
    
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    verificacion = coleccion.find_one({'email': email})
    
    # No hay verificación activa
    if not verificacion:
        return {
            'valido': False,
            'mensaje': 'No hay verificación activa. Solicita un nuevo código.'
        }
    
    # Verificar si está bloqueado
    bloqueado_hasta = verificacion.get('bloqueado_hasta')
    if bloqueado_hasta and unixtime < bloqueado_hasta:
        tiempo_espera = bloqueado_hasta - unixtime
        return {
            'valido': False,
            'mensaje': f'Demasiados intentos. Espera {tiempo_espera} segundos.'
        }
    
    # Verificar expiración
    expira = verificacion.get('expira', 0)
    if unixtime > expira:
        return {
            'valido': False,
            'mensaje': 'Token expirado. Solicita un nuevo código.'
        }
    
    # Verificar intentos
    intentos = verificacion.get('intentos', 0)
    max_intentos = verificacion.get('max_intentos', 5)
    
    if intentos >= max_intentos:
        # Bloquear por 15 minutos
        coleccion.update_one(
            {'email': email},
            {'$set': {'bloqueado_hasta': unixtime + 900}}
        )
        return {
            'valido': False,
            'mensaje': 'Demasiados intentos. Intenta de nuevo en 15 minutos.'
        }
    
    # Verificar token
    token_hash = verificacion.get('token_hash', '')
    if not verificar_token_hash(token_input, token_hash):
        # Incrementar intentos
        coleccion.update_one(
            {'email': email},
            {'$inc': {'intentos': 1}}
        )
        intentos_restantes = max_intentos - intentos - 1
        return {
            'valido': False,
            'mensaje': f'Token incorrecto. Intentos restantes: {intentos_restantes}'
        }
    
    # Token correcto - Marcar usuario como verificado
    usuarios = conexion_global.obtener_coleccion('usuarios')
    usuarios.update_one(
        {'email': email},
        {'$set': {
            'email_verified': True,
            'fecha_verificacion': datetime.now(timezone.utc)
        }}
    )
    
    # Eliminar token usado
    coleccion.delete_one({'email': email})
    
    return {
        'valido': True,
        'mensaje': 'Email verificado correctamente'
    }


def obtener_verificacion_pendiente(email: str) -> dict | None:
    """
    Obtiene información de verificación activa para un email.
    """
    from src.db.conexion import conexion_global
    
    coleccion = conexion_global.obtener_coleccion('verificaciones_email')
    verificacion = coleccion.find_one({'email': email.lower()})
    
    if not verificacion:
        return None
    
    expira = verificacion.get('expira', 0)
    unixtime = int(time.time())
    
    return {
        'email': verificacion['email'],
        'expira': expira,
        'intentos': verificacion.get('intentos', 0),
        'max_intentos': verificacion.get('max_intentos', 5),
        'expired': unixtime > expira,
        'bloqueado_hasta': verificacion.get('bloqueado_hasta')
    }


def esta_verificado(email: str) -> bool:
    """
    Verifica si un email ya fue verificado.
    """
    from src.db.conexion import conexion_global
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'email': email.lower()})
    
    if not usuario:
        return False
    
    return usuario.get('email_verified', False)


def enviar_token_por_email(email: str, token: str, asunto: str = "Verificación de cuenta") -> dict:
    """
    Envía el token por email al usuario.
    
    Usa configuración de environment:
    - EMAIL_ENABLED=False (default): Solo print en consola
    - EMAIL_ENABLED=True + SMTP config: Envía email real
    """
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Mensaje HTML
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #f5f5f5; padding: 20px; border-radius: 10px;">
            <h2 style="color: #333;">Verificación de Cuenta</h2>
            <p style="color: #666;">Tu código de verificación es:</p>
            <div style="background: #4CAF50; color: white; padding: 15px 30px; 
                        font-size: 32px; font-weight: bold; letter-spacing: 5px; 
                        text-align: center; border-radius: 5px; margin: 20px 0;">
                {token}
            </div>
            <p style="color: #666; font-size: 14px;">
                Este código expira en 5 minutos.<br>
                Si no solicitaste este código, puedes ignorar este email.
            </p>
        </div>
    </body>
    </html>
    """
    
    texto = f"Tu código de verificación es: {token}\n\nEste código expira en 5 minutos."
    
    # Verificar si está habilitado el envío real
    email_enabled = os.environ.get('EMAIL_ENABLED', 'false').lower() == 'true'
    
    if not email_enabled:
        # Modo desarrollo: solo print
        print("=" * 50)
        print(f"📧 EMAIL DE VERIFICACIÓN")
        print("=" * 50)
        print(f"Para: {email}")
        print(f"Token: {token}")
        print(f"Expira en: 5 minutos")
        print("=" * 50)
        return {'enviado': True, 'modo': 'desarrollo'}
    
    # Configuración SMTP
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_usuario = os.environ.get('SMTP_USUARIO', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    email_from = os.environ.get('EMAIL_FROM', smtp_usuario)
    
    if not smtp_usuario or not smtp_password:
        print("⚠️ SMTP no configurado. Usa EMAIL_ENABLED=false para modo desarrollo.")
        return {'enviado': False, 'error': 'SMTP no configurado'}
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = asunto
        msg['From'] = email_from
        msg['To'] = email
        
        parte1 = MIMEText(texto, 'plain')
        parte2 = MIMEText(html, 'html')
        
        msg.attach(parte1)
        msg.attach(parte2)
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_usuario, smtp_password)
            server.send_message(msg)
        
        print(f"✅ Email enviado a {email}")
        return {'enviado': True, 'modo': 'produccion'}
    
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return {'enviado': False, 'error': str(e)}


# Funciones legacy (compatibilidad)
def generar_token_verificacion(longitud: int = 6) -> str:
    """Alias para compatibilidad."""
    return generar_token(longitud)


def crear_token_verificacion(email: str, expiracion_minutos: int = 30) -> dict:
    """Alias para compatibilidad con sistema antiguo."""
    token = crear_o_actualizar_verificacion(email, expiracion_minutos)
    return {
        'token': token,
        'expira': int(time.time()) + (expiracion_minutos * 60),
        'email': email.lower()
    }


def verificar_token_legacy(email: str, token: str) -> dict:
    """Alias para verificación básica."""
    return verificar_token_db(email, token)


def verificar_email_esta_verificado(email: str) -> bool:
    """Alias para verificar si está verificado."""
    return esta_verificado(email)


def obtener_token_pendiente(email: str) -> dict | None:
    """Alias para obtener token pendiente."""
    return obtener_verificacion_pendiente(email)