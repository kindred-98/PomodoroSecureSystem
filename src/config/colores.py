"""
Módulo: colores.py
Responsabilidad: Paleta de colores centralizada para toda la UI.
Tema oscuro profesional inspirado en Linear/VSCode/Vercel.
"""

# Fondos
FONDO_PRINCIPAL = "#1E1E2E"
FONDO_SECUNDARIO = "#2A2A3E"
FONDO_CARD = "#313145"

# Acentos funcionales
TRABAJO_ACTIVO = "#7C3AED"      # violeta — pomodoro corriendo
COMPLETADO = "#10B981"           # verde esmeralda
AVISO = "#F59E0B"                # naranja ámbar
PELIGRO = "#EF4444"              # rojo
INFORMACION = "#3B82F6"          # azul

# Texto
TEXTO_PRINCIPAL = "#F8F8F2"
TEXTO_SECUNDARIO = "#94A3B8"

# Pantalla de bloqueo
BLOQUEO_CORTO = "#0F2744"        # azul oscuro
BLOQUEO_LARGO = "#0F2F1F"        # verde oscuro
BLOQUEO_FIJO = "#2D1B00"         # naranja oscuro

# Bordes y separadores
BORDE = "#3E3E5E"
BORDE_ACTIVO = "#7C3AED"

# Botones
BOTON_PRIMARIO = "#7C3AED"
BOTON_PRIMARIO_HOVER = "#6D28D9"
BOTON_SECUNDARIO = "#313145"
BOTON_SECUNDARIO_HOVER = "#3E3E5E"
BOTON_PELIGRO = "#EF4444"
BOTON_PELIGRO_HOVER = "#DC2626"
BOTON_EXITO = "#10B981"
BOTON_EXITO_HOVER = "#059669"

# Timer
TIMER_TRABAJO = "#7C3AED"
TIMER_DESCANSO_CORTO = "#3B82F6"
TIMER_DESCANSO_LARGO = "#10B981"
TIMER_PAUSADO = "#F59E0B"

# Configuración de CustomTkinter
def aplicar_tema():
    """Aplica el tema oscuro a CustomTkinter."""
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
