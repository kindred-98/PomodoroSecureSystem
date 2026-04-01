"""
Módulo: dashboard_encargado.py
Responsabilidad: Dashboard del encargado con timer + panel de equipo.
"""

import customtkinter as ctk
from src.config.colores import *


class DashboardEncargado(ctk.CTkFrame):
    """Dashboard del encargado: timer personal + supervisión de equipo."""

    def __init__(self, parent, usuario, on_logout, on_ver_contraseña, on_ver_historial):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_logout = on_logout
        self.on_ver_contraseña = on_ver_contraseña
        self.on_ver_historial = on_ver_historial
        self._crear_widgets()
        self._cargar_equipo()

    def _crear_widgets(self):
        # ── HEADER ──
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🍅 PomodoroSecure",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        nombre = self.usuario.get('nombre', 'Encargado')
        ctk.CTkLabel(
            header, text=f"{nombre} | Encargado",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="right", padx=20)

        # ── BODY ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # Panel lateral izquierdo (acciones + navegación)
        lateral = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=220, corner_radius=12)
        lateral.pack(side="left", fill="y", padx=(0, 15))
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral, text="📊 Acciones",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 10))

        botones_lateral = [
            ("🔑 Contraseña", self.on_ver_contraseña),
            ("📋 Historial", self.on_ver_historial),
            ("🚪 Cerrar Sesión", self._on_logout_click),
        ]
        for texto, cmd in botones_lateral:
            color = BOTON_PELIGRO if "Sesión" in texto else BOTON_SECUNDARIO
            hover = BOTON_PELIGRO_HOVER if "Sesión" in texto else BOTON_SECUNDARIO_HOVER
            ctk.CTkButton(
                lateral, text=texto,
                font=("JetBrains Mono", 12),
                fg_color=color, hover_color=hover,
                text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
                command=cmd,
            ).pack(fill="x", padx=15, pady=3)

        # Panel central (equipo)
        central = ctk.CTkFrame(body, fg_color="transparent")
        central.pack(side="right", fill="both", expand=True)

        # ── Mi Equipo ──
        equipo_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=16)
        equipo_card.pack(fill="both", expand=True)

        header_equipo = ctk.CTkFrame(equipo_card, fg_color="transparent")
        header_equipo.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            header_equipo, text="👥 Mi Equipo",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left")

        self.badge_anomalias = ctk.CTkLabel(
            header_equipo, text="",
            font=("JetBrains Mono", 12, "bold"), text_color=PELIGRO,
        )
        self.badge_anomalias.pack(side="right")

        # Scrollable frame para miembros
        self.frame_miembros = ctk.CTkScrollableFrame(
            equipo_card,
            fg_color="transparent",
            scrollbar_button_color=BORDE,
            scrollbar_button_hover_color=BORDE_ACTIVO,
        )
        self.frame_miembros.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.label_vacio = ctk.CTkLabel(
            self.frame_miembros,
            text="Cargando equipo...",
            font=("JetBrains Mono", 12),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_vacio.pack(pady=20)

    def _cargar_equipo(self):
        """Carga los miembros del equipo del encargado."""
        self._miembros_cache = []
        self._equipo_id = None
        try:
            from src.db.equipos import obtener_por_encargado
            from src.db.equipos import obtener_miembros

            equipo = obtener_por_encargado(str(self.usuario['_id']))
            if equipo:
                self._equipo_id = equipo['_id']
                miembros = obtener_miembros(str(equipo['_id']))
                self._miembros_cache = miembros
                self._actualizar_miembros()
                self._contar_anomalias_equipo(equipo['_id'])
                self._iniciar_polling_equipo()
            else:
                self.label_vacio.configure(text="No tienes un equipo asignado.")
        except Exception as e:
            self.label_vacio.configure(text=f"Error al cargar equipo: {e}")

    def _iniciar_polling_equipo(self):
        """Refresca el estado del equipo cada 5 segundos."""
        self._job_equipo = self.after(5000, self._refrescar_equipo)

    def _refrescar_equipo(self):
        """Refresca el estado real de los miembros."""
        try:
            self._actualizar_miembros()
        except Exception:
            pass
        self._job_equipo = self.after(5000, self._refrescar_equipo)

    def _actualizar_miembros(self):
        """Reconstruye la lista de miembros con estado real."""
        for widget in self.frame_miembros.winfo_children():
            widget.destroy()

        from src.db.conexion import conexion_global
        coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')

        for miembro in self._miembros_cache:
            estado, color, texto = self._obtener_estado_miembro(miembro, coleccion_ciclos)

            frame = ctk.CTkFrame(self.frame_miembros, fg_color=FONDO_SECUNDARIO, corner_radius=8)
            frame.pack(fill="x", pady=3)

            ctk.CTkLabel(
                frame, text=estado,
                font=("Segoe UI Emoji", 18), text_color=color,
            ).pack(side="left", padx=(10, 5), pady=8)

            info = ctk.CTkFrame(frame, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=8)

            ctk.CTkLabel(
                info, text=miembro.get('nombre', 'Sin nombre'),
                font=("JetBrains Mono", 12, "bold"), text_color=TEXTO_PRINCIPAL,
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                info, text=f"{miembro.get('rol', 'empleado').title()} — {texto}",
                font=("JetBrains Mono", 10), text_color=color,
                anchor="w",
            ).pack(fill="x")

    @staticmethod
    def _obtener_estado_miembro(miembro, coleccion_ciclos):
        """Obtiene el estado real de un miembro desde la BD."""
        try:
            mid = miembro.get('_id')
            if mid is None:
                return "⚫", TEXTO_SECUNDARIO, "Sin ID"

            ciclo = coleccion_ciclos.find_one({
                'usuario_id': mid,
                'completado': False,
            })

            if ciclo is None:
                return "⚫", TEXTO_SECUNDARIO, "Fuera de jornada"

            estado = ciclo.get('estado_actual', 'INACTIVO')

            if estado == 'TRABAJANDO':
                pom = ciclo.get('pomodoro_actual', 1)
                total = ciclo.get('pomodoros_totales', 4)
                return "🟢", COMPLETADO, f"Trabajando (Pom {pom}/{total})"
            elif estado == 'PAUSADO':
                return "🟡", AVISO, "En pausa"
            elif estado in ('DESCANSO_CORTO', 'DESCANSO_LARGO'):
                tipo = "corto" if 'CORTO' in estado else "largo"
                return "☕", TIMER_DESCANSO_CORTO if tipo == "corto" else TIMER_DESCANSO_LARGO, f"Descanso {tipo}"
            else:
                return "⚫", TEXTO_SECUNDARIO, "Inactivo"

        except Exception:
            return "⚫", TEXTO_SECUNDARIO, "Sin conexion"

    def _contar_anomalias_equipo(self, equipo_id):
        """Cuenta anomalías pendientes del equipo."""
        try:
            from src.db.anomalias import obtener_por_equipo
            anomalias = obtener_por_equipo(str(equipo_id))
            pendientes = [a for a in anomalias if not a.get('resuelto', False)]
            if pendientes:
                self.badge_anomalias.configure(text=f"🚨 {len(pendientes)} anomalía(s)")
        except Exception:
            pass

    def _on_logout_click(self):
        self.on_logout()
