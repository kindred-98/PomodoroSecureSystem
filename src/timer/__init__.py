"""
Módulo: timer/__init__.py
Responsabilidad: Exportar funciones del módulo Pomodoro Timer.
"""

from .banco_tiempo import validar_configuracion_descansos, calcular_descanso_largo
from .estados import (
    calcular_ciclos_jornada,
    obtener_transiciones_validas,
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
    ESTADO_PAUSADO,
)
from .ciclo_pomodoro import (
    iniciar_ciclo,
    obtener_estado_ciclo,
    manejar_evento_timer,
    registrar_callback,
)
from .servicio_sesiones import registrar_sesion_pomodoro

__all__ = [
    # Banco de tiempo
    "validar_configuracion_descansos",
    "calcular_descanso_largo",
    # Estados
    "calcular_ciclos_jornada",
    "obtener_transiciones_validas",
    "ESTADO_INACTIVO",
    "ESTADO_TRABAJANDO",
    "ESTADO_DESCANSO_CORTO",
    "ESTADO_DESCANSO_LARGO",
    "ESTADO_PAUSADO",
    # Ciclo Pomodoro
    "iniciar_ciclo",
    "obtener_estado_ciclo",
    "manejar_evento_timer",
    "registrar_callback",
    # Servicio sesiones
    "registrar_sesion_pomodoro",
]
