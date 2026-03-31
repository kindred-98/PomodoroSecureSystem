"""
Módulo: equipos/__init__.py
Responsabilidad: Exportar funciones CRUD para equipos.
"""

from src.db.equipos.crear_equipo import crear_equipo
from src.db.equipos.buscar_por_id import buscar_por_id
from src.db.equipos.obtener_miembros import obtener_miembros
from src.db.equipos.obtener_por_encargado import obtener_por_encargado
from src.db.equipos.añadir_miembro import añadir_miembro

__all__ = [
    'crear_equipo',
    'buscar_por_id',
    'obtener_miembros',
    'obtener_por_encargado',
    'añadir_miembro',
]
