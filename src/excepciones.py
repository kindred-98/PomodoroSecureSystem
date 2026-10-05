"""
Módulo: excepciones.py
Responsabilidad: Jerarquía de excepciones de dominio de PomodoroSecure.

Sustituye a los `Exception` genéricos para que cada fallo indique
qué regla del negocio se incumplió. Todas heredan de `ErrorPomodoro`,
de modo que el código existente que captura `Exception` sigue funcionando.
"""


class ErrorPomodoro(Exception):
    """Base de todas las errores de dominio de la aplicación."""


class ErrorAutenticacion(ErrorPomodoro):
    """Las credenciales o el estado de la cuenta no permiten continuar."""


class ErrorSesion(ErrorPomodoro):
    """La sesión no existe, expiró o ya fue cerrada."""


class ErrorValidacion(ErrorPomodoro):
    """Los datos de entrada no cumplen las reglas del dominio."""


class ErrorRecursoNoEncontrado(ErrorPomodoro):
    """El recurso solicitado (equipo, usuario, anomalía) no existe."""


class ErrorEstadoInvalido(ErrorPomodoro):
    """La operación no es válida para el estado actual del timer o ciclo."""
