"""
Módulo: equipos/__init__.py
Responsabilidad: Exportar funciones CRUD para equipos.
"""

from .crear_equipo import crear_equipo
from .buscar_por_id import buscar_por_id
from .obtener_miembros import obtener_miembros
from .obtener_por_encargado import obtener_por_encargado
from .añadir_miembro import añadir_miembro

__all__ = [
    'crear_equipo',
    'buscar_por_id',
    'obtener_miembros',
    'obtener_por_encargado',
    'añadir_miembro',
]
