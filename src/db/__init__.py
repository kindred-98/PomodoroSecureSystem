"""
Módulo: db/__init__.py
Responsabilidad: Exportar módulos de base de datos.
"""

from src.db.conexion import ConexionMongoDB, conexion_global
from src.db.usuarios import (
    crear_usuario,
    buscar_por_email,
    buscar_por_id,
    actualizar_pomodoro,
    actualizar_ultimo_acceso,
    desactivar_usuario,
)
from src.db.equipos import (
    crear_equipo,
    obtener_miembros,
    obtener_por_encargado,
    añadir_miembro,
)
from src.db.sesiones import (
    crear_sesion,
    actualizar_sesion,
    cerrar_sesion,
    obtener_historial,
)
from src.db.anomalias import (
    registrar_anomalia,
    obtener_por_usuario,
    obtener_por_equipo,
    marcar_revisada,
)

__all__ = [
    # Conexión
    "ConexionMongoDB",
    "conexion_global",
    # Usuarios
    "crear_usuario",
    "buscar_por_email",
    "buscar_por_id",
    "actualizar_pomodoro",
    "actualizar_ultimo_acceso",
    "desactivar_usuario",
    # Equipos
    "crear_equipo",
    "obtener_miembros",
    "obtener_por_encargado",
    "añadir_miembro",
    # Sesiones
    "crear_sesion",
    "actualizar_sesion",
    "cerrar_sesion",
    "obtener_historial",
    # Anomalías
    "registrar_anomalia",
    "obtener_por_usuario",
    "obtener_por_equipo",
    "marcar_revisada",
]
