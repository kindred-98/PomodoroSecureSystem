"""
Módulo: anomalias/__init__.py
Responsabilidad: Exportar funciones CRUD para anomalías.
"""

from src.db.anomalias.registrar_anomalia import registrar_anomalia
from src.db.anomalias.obtener_por_usuario import obtener_por_usuario
from src.db.anomalias.obtener_por_equipo import obtener_por_equipo
from src.db.anomalias.marcar_revisada import marcar_revisada

__all__ = [
    'registrar_anomalia',
    'obtener_por_usuario',
    'obtener_por_equipo',
    'marcar_revisada',
]
