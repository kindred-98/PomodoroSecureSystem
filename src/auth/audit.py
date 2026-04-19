"""
Módulo: audit.py
Responsabilidad: Logging de auditoría para eventos de seguridad.
"""

import logging as log
import os
from typing import Optional


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


def audit_registro(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de registro de usuario."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    if exitoso:
        logger.info(f"REGISTRO_EXITOSO - Email: {email}{ip_info}")
    else:
        logger.warning(f"REGISTRO_FALLIDO - Email: {email}{ip_info}")


def audit_verificacion(email: str, exitosa: bool, ip: Optional[str] = None):
    """Log de verificación de email."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    if exitosa:
        logger.info(f"VERIFICACION_EXITOSA - Email: {email}{ip_info}")
    else:
        logger.warning(f"VERIFICACION_FALLIDA - Email: {email}{ip_info}")


def audit_login(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de inicio de sesión."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    if exitoso:
        logger.info(f"LOGIN_EXITOSO - Email: {email}{ip_info}")
    else:
        logger.warning(f"LOGIN_FALLIDO - Email: {email}{ip_info}")


def audit_logout(email: str, ip: Optional[str] = None):
    """Log de cierre de sesión."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    logger.info(f"LOGOUT - Email: {email}{ip_info}")


def audit_cambio_contraseña(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de cambio de contraseña."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    if exitoso:
        logger.info(f"CAMBIO_CONTRASEÑA_EXITOSO - Email: {email}{ip_info}")
    else:
        logger.warning(f"CAMBIO_CONTRASEÑA_FALLIDO - Email: {email}{ip_info}")


def audit_recuperacion_contraseña(email: str, exitoso: bool, ip: Optional[str] = None):
    """Log de recuperación de contraseña."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    if exitoso:
        logger.info(f"RECUPERACION_EXITOSA - Email: {email}{ip_info}")
    else:
        logger.warning(f"RECUPERACION_FALLIDA - Email: {email}{ip_info}")


def audit_bloqueo_cuenta(email: str, razon: str, ip: Optional[str] = None):
    """Log de bloqueo de cuenta."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    logger.warning(f"BLOQUEO_CUENTA - Email: {email} - Razón: {razon}{ip_info}")


def audit_desbloqueo_cuenta(email: str, ip: Optional[str] = None):
    """Log de desbloqueo de cuenta."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    logger.info(f"DESBLOQUEO_CUENTA - Email: {email}{ip_info}")


def audit_intento_sospechoso(evento: str, detalles: str, ip: Optional[str] = None):
    """Log de intento sospechoso."""
    logger = obtener_logger()
    ip_info = f" - IP: {ip}" if ip else ""
    logger.critical(f"INTENTO_SOSPECHOSO - {evento} - Detalles: {detalles}{ip_info}")


def audit_error(func_name: str, error: str):
    """Log de error en función."""
    logger = obtener_logger()
    logger.error(f"ERROR en {func_name}: {error}")