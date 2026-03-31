"""
Módulo: splash.py
Responsabilidad: Splash Screen de carga inicial.
"""

import customtkinter as ctk
from ..config.colores import *


class SplashView(ctk.CTkFrame):
    """Splash Screen — se muestra 2-3 segundos al iniciar la app."""

    def __init__(self, parent, on_complete):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.on_complete = on_complete
        self._crear_widgets()

    def _crear_widgets(self):
        # Contenedor central
        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        # Logo emoji
        ctk.CTkLabel(
            centro,
            text="🍅🔐",
            font=("Segoe UI Emoji", 64),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 20))

        # Nombre de la app
        ctk.CTkLabel(
            centro,
            text="PomodoroSecure",
            font=("JetBrains Mono", 32, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack()

        # Subtítulo
        ctk.CTkLabel(
            centro,
            text="Sistema de Gestión Segura de Tiempo",
            font=("JetBrains Mono", 12),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=(5, 30))

        # Barra de progreso
        self.progreso = ctk.CTkProgressBar(
            centro,
            width=300,
            height=6,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
        )
        self.progreso.pack()
        self.progreso.set(0)

        # Versión
        ctk.CTkLabel(
            centro,
            text="v1.0.0",
            font=("JetBrains Mono", 10),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=(20, 0))

    def iniciar_animacion(self):
        """Inicia la barra de progreso y transición a login."""
        self._animar_progreso(0)

    def _animar_progreso(self, valor):
        if valor < 1:
            self.progreso.set(valor)
            self.after(50, self._animar_progreso, valor + 0.02)
        else:
            self.progreso.set(1)
            self.after(300, self.on_complete)
