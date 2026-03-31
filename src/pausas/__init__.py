"""
Módulo: pausas/__init__.py
Responsabilidad: Exportar funciones del módulo de pausas manuales.
"""

from src.pausas.gestor_pausas import iniciar_pausa, finalizar_pausa

__all__ = [
    "iniciar_pausa",
    "finalizar_pausa",
]
