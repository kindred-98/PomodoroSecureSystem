"""
Módulo: audit.py
Responsabilidad: Logging de auditoría para eventos de seguridad.
Los emails se sanitizan (hash) para proteger privacidad.
"""

import logging as log
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional


def _asegurar_directorio_logs():
    """Crea el directorio logs si no existe."""
    directorio = 'logs'
    if not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)


def _sanitizar_email(email: str) -> str:
    """
    Hashea el email para no guardarlo en texto plano.
    Usa los primeros 8 caracteres del hash para identificación.
    """
    if not email:
        return "unknown"
    hash_email = hashlib.sha256(email.lower().encode()).hexdigest()[:8]
    return f"user_{hash_email}"


def _formatear_json(accion: str, email: str, exitoso: bool, detalles: dict = None) -> str:
    """Formatea mensaje como JSON estructurado con email sanitizado."""
    data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'accion': accion,
        'email_hash': _sanitizar_email(email),
        'exitoso': exitoso,
    }
    if detalles:
        data['detalles'] = detalles
    return json.dumps(data, ensure_ascii=False)


def obtener_logger() -> log.Logger:
    """Obtiene el logger de auditoría."""
    logger = log.getLogger('auditoria')

    if not logger.handlers:
        log.basicConfig(
            level=log.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                log.StreamHandler(),
            ]
        )

        if not os.environ.get('ENVIRONMENT') or os.environ.get('ENVIRONMENT') == 'produccion':
            try:
                _asegurar_directorio_logs()
                import logging.handlers
                file_handler = logging.handlers.RotatingFileHandler(
                    'logs/auditoria.log',
                    maxBytes=10*1024*1024,
                    backupCount=5,
                    encoding='utf-8'
                )
                file_handler.setFormatter(
                    log.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                )
                logger.addHandler(file_handler)
            except Exception:
                pass

    return logger


def _formatear_mensaje(accion: str, email: str, exitoso: bool, ip: Optional[str] = None) -> str:
    """Formatea mensaje con email sanitizado."""
    email_seguro = _sanitizar_email(email)
    ip_info = f" - IP: {ip}" if ip else ""
    resultado = "EXITOSO" if exitoso else "FALLIDO"
    return f"{accion}_{resultado} - Email: {email_seguro}{ip_info}"


def audit_registro(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de registro de usuario."""
    logger = obtener_logger()
    logger.info(_formatear_mensaje("REGISTRO", email, exitoso, ip))


def audit_verificacion(email: str, exitosa: bool, ip: Optional[str] = None):
    """Log de verificación de email."""
    logger = obtener_logger()
    logger.info(_formatear_mensaje("VERIFICACION", email, exitosa, ip))


def audit_login(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de inicio de sesión."""
    logger = obtener_logger()
    logger.info(_formatear_mensaje("LOGIN", email, exitoso, ip))


def audit_logout(email: str, ip: Optional[str] = None):
    """Log de cierre de sesión."""
    logger = obtener_logger()
    email_seguro = _sanitizar_email(email)
    ip_info = f" - IP: {ip}" if ip else ""
    logger.info(f"LOGOUT - Email: {email_seguro}{ip_info}")


def audit_cambio_contrasena(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de cambio de contrasena."""
    logger = obtener_logger()
    logger.info(_formatear_mensaje("CAMBIO_CONTRASENA", email, exitoso, ip))


def audit_recuperacion_contrasena(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de recuperacion de contrasena."""
    logger = obtener_logger()
    logger.info(_formatear_mensaje("RECUPERACION_CONTRASENA", email, exitoso, ip))


def audit_bloqueo_cuenta(email: str, razon: str, ip: Optional[str] = None):
    """Log de bloqueo de cuenta."""
    logger = obtener_logger()
    email_seguro = _sanitizar_email(email)
    ip_info = f" - IP: {ip}" if ip else ""
    logger.warning(f"BLOQUEO_CUENTA - Email: {email_seguro} - Razón: {razon}{ip_info}")


def audit_desbloqueo_cuenta(email: str, ip: Optional[str] = None):
    """Log de desbloqueo de cuenta."""
    logger = obtener_logger()
    email_seguro = _sanitizar_email(email)
    ip_info = f" - IP: {ip}" if ip else ""
    logger.info(f"DESBLOQUEO_CUENTA - Email: {email_seguro}{ip_info}")


def audit_intento_sospechoso(evento: str, detalles: str, ip: Optional[str] = None):
    """Log de intento sospechoso."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    logger.critical(f"INTENTO_SOSPECHOSO - {evento} - Detalles: {detalles}{ip_info}")


def audit_error(func_name: str, error: str):
    """Log de error en función."""
    logger = obtener_logger()
    logger.error(f"ERROR en {func_name}: {error}")