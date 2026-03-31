"""
Módulo: historial_view.py
Responsabilidad: Vista de historial de sesiones Pomodoro.
"""

import customtkinter as ctk
from ..config.colores import *


class HistorialView(ctk.CTkFrame):
    """Pantalla de historial de sesiones del usuario."""

    def __init__(self, parent, usuario, on_volver):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_volver = on_volver
        self._crear_widgets()
        self._cargar_sesiones()

    def _crear_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header, text="← Volver",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=36, corner_radius=8,
            command=self.on_volver,
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkLabel(
            header, text="📋 Historial de Sesiones",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        # Contenido
        contenido = ctk.CTkFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=20, pady=15)

        # Card de resumen
        self.card_resumen = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        self.card_resumen.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.card_resumen, text="📊 Resumen",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.label_resumen = ctk.CTkLabel(
            self.card_resumen, text="Cargando...",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_resumen.pack(anchor="w", padx=20, pady=(0, 15))

        # Lista de sesiones
        ctk.CTkLabel(
            contenido, text="Sesiones recientes",
            font=("JetBrains Mono", 13, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", pady=(0, 5))

        self.frame_sesiones = ctk.CTkScrollableFrame(
            contenido, fg_color=FONDO_CARD, corner_radius=12,
            scrollbar_button_color=BORDE,
        )
        self.frame_sesiones.pack(fill="both", expand=True)

    def _cargar_sesiones(self):
        """Carga las sesiones del usuario desde BD."""
        try:
            from ..db.conexion import conexion_global
            from bson import ObjectId

            coleccion = conexion_global.obtener_coleccion('sesiones')
            sesiones = list(coleccion.find(
                {'usuario_id': self.usuario['_id']}
            ).sort('inicio', -1).limit(50))

            # Resumen
            total_pomodoros = sum(
                1 for s in sesiones if s.get('tipo_sesion') == 'pomodoro'
            )
            total_segundos = sum(
                s.get('duracion_segundos', 0) for s in sesiones
            )
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60

            self.label_resumen.configure(
                text=f"Total Pomodoros: {total_pomodoros} | Tiempo trabajado: {horas}h {minutos}m"
            )

            # Limpiar
            for widget in self.frame_sesiones.winfo_children():
                widget.destroy()

            if not sesiones:
                ctk.CTkLabel(
                    self.frame_sesiones,
                    text="No hay sesiones registradas",
                    font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
                ).pack(pady=30)
                return

            for sesion in sesiones:
                frame = ctk.CTkFrame(self.frame_sesiones, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                # Tipo
                tipo = sesion.get('tipo_sesion', 'pomodoro')
                emoji = "🍅" if tipo == "pomodoro" else "☕"
                color = TRABAJO_ACTIVO if tipo == "pomodoro" else TIMER_DESCANSO_CORTO

                ctk.CTkLabel(
                    frame, text=emoji,
                    font=("Segoe UI Emoji", 16), text_color=color,
                ).pack(side="left", padx=(10, 5), pady=6)

                # Info
                info = ctk.CTkFrame(frame, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, pady=6)

                duracion_min = sesion.get('duracion_segundos', 0) // 60
                ciclo = sesion.get('numero_ciclo', '?')
                pom = sesion.get('pomodoro_numero', '?')

                ctk.CTkLabel(
                    info,
                    text=f"Ciclo {ciclo} — Pomodoro {pom} — {duracion_min} min",
                    font=("JetBrains Mono", 11), text_color=TEXTO_PRINCIPAL,
                    anchor="w",
                ).pack(fill="x")

                inicio = sesion.get('inicio', '')
                if hasattr(inicio, 'strftime'):
                    fecha = inicio.strftime("%d/%m/%Y %H:%M")
                else:
                    fecha = str(inicio)[:16]
                ctk.CTkLabel(
                    info, text=fecha,
                    font=("JetBrains Mono", 10), text_color=TEXTO_SECUNDARIO,
                    anchor="w",
                ).pack(fill="x")

        except Exception as e:
            self.label_resumen.configure(text=f"Error: {e}")
