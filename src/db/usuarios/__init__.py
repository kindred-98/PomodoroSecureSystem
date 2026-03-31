"""
Módulo: usuarios/__init__.py
Responsabilidad: Exportar funciones CRUD para usuarios.
"""

from src.db.usuarios.crear_usuario import crear_usuario
from src.db.usuarios.buscar_por_email import buscar_por_email
from src.db.usuarios.buscar_por_id import buscar_por_id
from src.db.usuarios.actualizar_pomodoro import actualizar_pomodoro
from src.db.usuarios.actualizar_ultimo_acceso import actualizar_ultimo_acceso
from src.db.usuarios.desactivar_usuario import desactivar_usuario

__all__ = [
    'crear_usuario',
    'buscar_por_email',
    'buscar_por_id',
    'actualizar_pomodoro',
    'actualizar_ultimo_acceso',
    'desactivar_usuario',
]
