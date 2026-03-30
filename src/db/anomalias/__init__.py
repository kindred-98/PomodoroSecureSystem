"""
Módulo: anomalias/__init__.py
Responsabilidad: Exportar funciones CRUD para anomalías.
"""

from .registrar_anomalia import registrar_anomalia
from .obtener_por_usuario import obtener_por_usuario
from .obtener_por_equipo import obtener_por_equipo
from .marcar_revisada import marcar_revisada

__all__ = [
    'registrar_anomalia',
    'obtener_por_usuario',
    'obtener_por_equipo',
    'marcar_revisada',
]
