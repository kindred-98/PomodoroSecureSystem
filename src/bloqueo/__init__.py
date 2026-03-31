"""
Módulo: bloqueo/__init__.py
Responsabilidad: Exportar funciones del módulo de bloqueo.
"""

from src.bloqueo.windows_lock import bloquear_escritorio

__all__ = [
    "bloquear_escritorio",
]
