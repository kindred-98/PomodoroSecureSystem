"""
Módulo: colores.py
Colores para la app. Se definen al cargar.
"""

import os
from dotenv import load_dotenv
load_dotenv()

TEMA = os.getenv("TEMA", "dark")

# ============================================
# TEMA OSCURO (por defecto)
# ============================================

if TEMA == "light":
    FONDO_PRINCIPAL = "#F0F4F8"
    FONDO_SECUNDARIO = "#FFFFFF"
    FONDO_CARD = "#FFFFFF"
    TEXTO_PRINCIPAL = "#1E293B"
    TEXTO_SECUNDARIO = "#64748B"
    BORDE = "#CBD5E1"
    BORDE_ACTIVO = "#3B82F6"
    BOTON_PRIMARIO = "#3B82F6"
    BOTON_PRIMARIO_HOVER = "#2563EB"
    BOTON_SECUNDARIO = "#E2E8F0"
    BOTON_SECUNDARIO_HOVER = "#CBD5E1"
    BOTON_PELIGRO = "#EF4444"
    BOTON_PELIGRO_HOVER = "#DC2626"
    BOTON_EXITO = "#10B981"
    BOTON_EXITO_HOVER = "#059669"
    COMPLETADO = "#10B981"
    PELIGRO = "#EF4444"
    AVISO = "#F59E0B"
    INFORMACION = "#3B82F6"
    TRABAJO_ACTIVO = "#3B82F6"
    BLOQUEO_CORTO = "#DBEAFE"
    BLOQUEO_LARGO = "#D1FAE5"
    BLOQUEO_FIJO = "#FEF3C7"
else:
    FONDO_PRINCIPAL = "#1E1E2E"
    FONDO_SECUNDARIO = "#2A2A3E"
    FONDO_CARD = "#313145"
    TEXTO_PRINCIPAL = "#F8F8F2"
    TEXTO_SECUNDARIO = "#94A3B8"
    BORDE = "#3E3E5E"
    BORDE_ACTIVO = "#7C3AED"
    BOTON_PRIMARIO = "#7C3AED"
    BOTON_PRIMARIO_HOVER = "#6D28D9"
    BOTON_SECUNDARIO = "#313145"
    BOTON_SECUNDARIO_HOVER = "#3E3E5E"
    BOTON_PELIGRO = "#EF4444"
    BOTON_PELIGRO_HOVER = "#DC2626"
    BOTON_EXITO = "#10B981"
    BOTON_EXITO_HOVER = "#059669"
    COMPLETADO = "#10B981"
    PELIGRO = "#EF4444"
    AVISO = "#F59E0B"
    INFORMACION = "#3B82F6"
    TRABAJO_ACTIVO = "#7C3AED"
    BLOQUEO_CORTO = "#0F2744"
    BLOQUEO_LARGO = "#0F2F1F"
    BLOQUEO_FIJO = "#2D1B00"

# Timer
TIMER_TRABAJO = TRABAJO_ACTIVO
TIMER_DESCANSO_CORTO = INFORMACION
TIMER_DESCANSO_LARGO = COMPLETADO
TIMER_PAUSADO = AVISO


def aplicar_tema(tema=None):
    """Aplica el tema a CustomTkinter."""
    import customtkinter as ctk
    if tema == "light":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")