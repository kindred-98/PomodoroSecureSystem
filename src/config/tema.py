"""
Actualizador de tema en tiempo real.
"""

import customtkinter as ctk

tema_actual = "dark"

def cambiar_tema_a(nuevo_tema):
    """Cambia el tema de toda la aplicación."""
    global tema_actual
    tema_actual = nuevo_tema

    ctk.set_appearance_mode(nuevo_tema)

    from src.config import colores
    colores.tema_actual = nuevo_tema

    _actualizar_ui()


def _actualizar_ui():
    """Fuerza actualización de UI."""
    for widget in ctk.CTk._app_layer:
        try:
            widget.update()
        except:
            pass


def obtener_tema_actual():
    """Retorna el tema actual."""
    return tema_actual