"""
Módulo: componentes.py
Responsabilidad: Componentes UI reutilizables (botones, inputs, cards).
"""

import customtkinter as ctk
from src.ui.templates.theme import *
from src.ui.templates.fuentes import *


# ============================================
# BOTONES
# ============================================

class BotonPrimario(ctk.CTkButton):
    """Botón primario violeta."""
    def __init__(self, parent, texto, comando, alto=48, ancho=None):
        super().__init__(
            parent,
            text=texto,
            font=NORMAL_NEGRITA,
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=alto,
            width=ancho,
            corner_radius=8,
            command=comando
        )


class BotonSecundario(ctk.CTkButton):
    """Botón secundario gris."""
    def __init__(self, parent, texto, comando, alto=45, ancho=None):
        super().__init__(
            parent,
            text=texto,
            font=PEQUENO,
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=alto,
            width=ancho,
            corner_radius=8,
            command=comando
        )


class BotonPeligro(ctk.CTkButton):
    """Botón de acción peligrosa (rojo)."""
    def __init__(self, parent, texto, comando, alto=45, ancho=None):
        super().__init__(
            parent,
            text=texto,
            font=NORMAL_NEGRITA,
            fg_color=BOTON_PELIGRO,
            hover_color=BOTON_PELIGRO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=alto,
            width=ancho,
            corner_radius=8,
            command=comando
        )


# ============================================
# INPUTS
# ============================================

class InputTexto(ctk.CTkEntry):
    """Input de texto estándar."""
    def __init__(self, parent, placeholder="", altura=44, tamano_fuente=15):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            font=crear_fuente(tamano_fuente),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=altura,
            corner_radius=8,
        )


class InputPassword(ctk.CTkEntry):
    """Input de contraseña."""
    def __init__(self, parent, placeholder="", altura=44, tamano_fuente=15):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            font=crear_fuente(tamano_fuente),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=altura,
            corner_radius=8,
            show="•"
        )


# ============================================
# LABELS
# ============================================

class LabelTitulo(ctk.CTkLabel):
    """Label para títulos."""
    def __init__(self, parent, texto):
        super().__init__(
            parent,
            text=texto,
            font=TITULO,
            text_color=TEXTO_PRINCIPAL
        )


class LabelNormal(ctk.CTkLabel):
    """Label de texto normal."""
    def __init__(self, parent, texto, color=TEXTO_PRINCIPAL):
        super().__init__(
            parent,
            text=texto,
            font=NORMAL,
            text_color=color
        )


class LabelError(ctk.CTkLabel):
    """Label para errores (rojo)."""
    def __init__(self, parent, texto=""):
        super().__init__(
            parent,
            text=texto,
            font=PEQUENO,
            text_color=PELIGRO
        )


# ============================================
# CONTAINERS
# ============================================

class Card(ctk.CTkFrame):
    """Card contenedor principal."""
    def __init__(self, parent, ancho=660, alto=760):
        super().__init__(
            parent,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=ancho,
            height=alto
        )
        self.place(relx=0.5, rely=0.5, anchor="center")
        self.pack_propagate(False)


class FrameContenido(ctk.CTkFrame):
    """Frame de contenido interno."""
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )


# ============================================
# CHECKBOX Y RADIOS
# ============================================

class Checkbox(ctk.CTkCheckBox):
    """Checkbox personalizado."""
    def __init__(self, parent, texto, variable):
        super().__init__(
            parent,
            text=texto,
            variable=variable,
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            fg_color=FONDO_SECUNDARIO,
            checkmark_color=TEXTO_PRINCIPAL
        )


class Radio(ctk.CTkRadioButton):
    """Radio button personalizado."""
    def __init__(self, parent, texto, variable, valor, comando=None):
        super().__init__(
            parent,
            text=texto,
            variable=variable,
            value=valor,
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            fg_color=TRABAJO_ACTIVO,
            hover_color=BOTON_PRIMARIO_HOVER,
            command=comando
        )


# ============================================
# PROGRESS BAR
# ============================================

class ProgressBar(ctk.CTkProgressBar):
    """Barra de progreso."""
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            height=4
        )