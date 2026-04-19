"""
Módulo: rate_limiting.py
Responsabilidad: Rate limiting global para Login y Verificación.
"""

import time
import os
from typing import Optional

_intentos_login: dict = {}
_intentos_verificacion: dict = {}


def limpiar_expirados():
    """Limpia intentos expirados."""
    timestamp = int(time.time())
    global _intentos_login, _intentos_verificacion

    _intentos_login = {
        k: v for k, v in _intentos_login.items()
        if v.get('expires', 0) > timestamp
    }
    _intentos_verificacion = {
        k: v for k, v in _intentos_verificacion.items()
        if v.get('expires', 0) > timestamp
    }


def verificar_rate_limit_login(email: str) -> tuple[bool, str]:
    """
    Verifica si el email puede intentar login.

    Returns:
        tuple: (puede_intentar, mensaje)
    """
    limpiar_expirados()
    key = email.lower()

    if key not in _intentos_login:
        return True, ""

    data = _intentos_login[key]
    if data.get('bloqueado_hasta', 0) > int(time.time()):
        tiempo_espera = data['bloqueado_hasta'] - int(time.time())
        return False, f"Cuenta bloqueada. Espera {tiempo_espera} segundos."

    if data.get('intentos', 0) >= 5:
        _intentos_login[key] = {
            'intentos': data['intentos'],
            'expires': int(time.time()) + 900,
            'bloqueado_hasta': int(time.time()) + 900
        }
        return False, "Demasiados intentos. Bloqueado por 15 minutos."

    return True, ""


def registrar_intento_login(email: str, exitoso: bool):
    """Registra intento de login."""
    limpiar_expirados()
    key = email.lower()

    if exitoso:
        if key in _intentos_login:
            del _intentos_login[key]
        return

    if key not in _intentos_login:
        _intentos_login[key] = {
            'intentos': 0,
            'expires': int(time.time()) + 300
        }

    _intentos_login[key]['intentos'] = _intentos_login[key].get('intentos', 0) + 1
    _intentos_login[key]['expires'] = int(time.time()) + 300


def verificar_rate_limit_verificacion(ip: str) -> tuple[bool, str]:
    """
    Verifica si la IP puede solicitar verificación.

    Returns:
        tuple: (puede_intentar, mensaje)
    """
    limpiar_expirados()

    if ip not in _intentos_verificacion:
        return True, ""

    data = _intentos_verificacion[ip]
    if data.get('bloqueado_hasta', 0) > int(time.time()):
        tiempo_espera = data['bloqueado_hasta'] - int(time.time())
        return False, f"IP bloqueada. Espera {tiempo_espera} segundos."

    return True, ""


def registrar_intento_verificacion(ip: str, exitoso: bool):
    """Registra intento de verificación."""
    limpiar_expirados()

    if exitoso:
        if ip in _intentos_verificacion:
            del _intentos_verificacion[ip]
        return

    if ip not in _intentos_verificacion:
        _intentos_verificacion[ip] = {
            'intentos': 0,
            'expires': int(time.time()) + 900
        }

    _intentos_verificacion[ip]['intentos'] = _intentos_verificacion[ip].get('intentos', 0) + 1

    if _intentos_verificacion[ip].get('intentos', 0) >= 10:
        _intentos_verificacion[ip]['bloqueado_hasta'] = int(time.time()) + 3600


def obtener_intentos_login(email: str) -> int:
    """Obtiene número de intentos."""
    key = email.lower()
    return _intentos_login.get(key, {}).get('intentos', 0)


def obtener_intentos_verificacion(ip: str) -> int:
    """Obtiene número de intentos."""
    return _intentos_verificacion.get(ip, {}).get('intentos', 0)


def reiniciar_intentos_login(email: str):
    """Reinicia intentos (para testing)."""
    key = email.lower()
    if key in _intentos_login:
        del _intentos_login[key]


def reiniciar_intentos_verificacion(ip: str):
    """Reinicia intentos (para testing)."""
    if ip in _intentos_verificacion:
        del _intentos_verificacion[ip]