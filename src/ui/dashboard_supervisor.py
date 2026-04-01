"""
Módulo: dashboard_supervisor.py
Responsabilidad: Dashboard del supervisor con gestión global.
"""

import customtkinter as ctk
from src.config.colores import *


class DashboardSupervisor(ctk.CTkFrame):
    """Dashboard del supervisor: gestión de equipos, anomalías, configuración."""

    def __init__(self, parent, usuario, on_logout, on_ver_contraseña, on_ver_historial):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_logout = on_logout
        self.on_ver_contraseña = on_ver_contraseña
        self.on_ver_historial = on_ver_historial
        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        # ── HEADER ──
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🍅 PomodoroSecure",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        nombre = self.usuario.get('nombre', 'Supervisor')
        ctk.CTkLabel(
            header, text=f"{nombre} | Supervisor",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="right", padx=20)

        # ── BODY ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # ── Panel lateral: navegación ──
        lateral = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=220, corner_radius=12)
        lateral.pack(side="left", fill="y", padx=(0, 15))
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral, text="⚙️ Gestión",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 10))

        botones = [
            ("📋 Historial", self.on_ver_historial),
            ("☕ Descansos Fijos", self._ver_descansos_fijos),
            ("🔑 Contraseña", self.on_ver_contraseña),
            ("🚪 Cerrar Sesión", self._on_logout_click),
        ]
        for texto, cmd in botones:
            color = BOTON_PELIGRO if "Sesión" in texto else BOTON_SECUNDARIO
            hover = BOTON_PELIGRO_HOVER if "Sesión" in texto else BOTON_SECUNDARIO_HOVER
            ctk.CTkButton(
                lateral, text=texto,
                font=("JetBrains Mono", 12),
                fg_color=color, hover_color=hover,
                text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
                command=cmd,
            ).pack(fill="x", padx=15, pady=3)

        # ── Panel central ──
        central = ctk.CTkFrame(body, fg_color="transparent")
        central.pack(side="right", fill="both", expand=True)

        # ── Resumen general ──
        resumen_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        resumen_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            resumen_card, text="📊 Resumen General",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.frame_stats = ctk.CTkFrame(resumen_card, fg_color="transparent")
        self.frame_stats.pack(fill="x", padx=20, pady=(0, 15))

        self.label_stats = ctk.CTkLabel(
            self.frame_stats, text="Cargando...",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_stats.pack()

        # ── Equipos ──
        equipos_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        equipos_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            equipos_card, text="👥 Equipos",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.frame_equipos = ctk.CTkScrollableFrame(
            equipos_card, fg_color="transparent",
            height=150,
            scrollbar_button_color=BORDE,
        )
        self.frame_equipos.pack(fill="x", padx=20, pady=(0, 15))

        # ── Usuarios ──
        usuarios_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        usuarios_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            usuarios_card, text="Usuarios",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.frame_usuarios = ctk.CTkScrollableFrame(
            usuarios_card, fg_color="transparent",
            height=150,
            scrollbar_button_color=BORDE,
        )
        self.frame_usuarios.pack(fill="x", padx=20, pady=(0, 15))

        # ── Anomalías ──
        anomalias_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        anomalias_card.pack(fill="both", expand=True)

        header_anom = ctk.CTkFrame(anomalias_card, fg_color="transparent")
        header_anom.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header_anom, text="🚨 Anomalías Recientes",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left")

        self.badge_anomalias = ctk.CTkLabel(
            header_anom, text="",
            font=("JetBrains Mono", 12, "bold"), text_color=PELIGRO,
        )
        self.badge_anomalias.pack(side="right")

        self.frame_anomalias = ctk.CTkScrollableFrame(
            anomalias_card, fg_color="transparent",
            scrollbar_button_color=BORDE,
        )
        self.frame_anomalias.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def _cargar_datos(self):
        """Carga los datos del supervisor."""
        self._cargar_equipos()
        self._cargar_usuarios()
        self._cargar_anomalias()

    def _cargar_equipos(self):
        """Carga todos los equipos."""
        try:
            from src.db.equipos import obtener_por_encargado
            from src.db.conexion import conexion_global

            coleccion = conexion_global.obtener_coleccion('equipos')
            equipos = list(coleccion.find())

            total_usuarios = 0
            for widget in self.frame_equipos.winfo_children():
                widget.destroy()

            for equipo in equipos:
                frame = ctk.CTkFrame(self.frame_equipos, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                ctk.CTkLabel(
                    frame, text=f"📁 {equipo.get('nombre', 'Sin nombre')}",
                    font=("JetBrains Mono", 12), text_color=TEXTO_PRINCIPAL,
                ).pack(side="left", padx=10, pady=6)

                miembros = equipo.get('miembros', [])
                total_usuarios += len(miembros)
                ctk.CTkLabel(
                    frame, text=f"{len(miembros)} miembros",
                    font=("JetBrains Mono", 10), text_color=TEXTO_SECUNDARIO,
                ).pack(side="right", padx=10)

            self.label_stats.configure(
                text=f"Total: {len(equipos)} equipos | {total_usuarios} usuarios"
            )
        except Exception as e:
            self.label_stats.configure(text=f"Error: {e}")

    def _cargar_usuarios(self):
        """Carga todos los usuarios con opción de cambiar rol."""
        for widget in self.frame_usuarios.winfo_children():
            widget.destroy()

        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            usuarios = list(coleccion.find({'activo': True}))

            if not usuarios:
                ctk.CTkLabel(
                    self.frame_usuarios,
                    text="No hay usuarios registrados.",
                    font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
                ).pack(pady=10)
                return

            for usr in usuarios:
                frame = ctk.CTkFrame(self.frame_usuarios, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                nombre = usr.get('nombre', 'Sin nombre')
                email = usr.get('email', '')
                rol = usr.get('rol', 'empleado')

                info = ctk.CTkFrame(frame, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, padx=10, pady=6)

                ctk.CTkLabel(
                    info, text=f"{nombre} ({email})",
                    font=("JetBrains Mono", 11), text_color=TEXTO_PRINCIPAL, anchor="w",
                ).pack(fill="x")

                rol_label = ctk.CTkLabel(
                    info, text=rol.upper(),
                    font=("JetBrains Mono", 9, "bold"),
                    text_color=self._color_rol(rol),
                    anchor="w",
                )
                rol_label.pack(fill="x")

                # Combo para cambiar rol
                combo = ctk.CTkComboBox(
                    frame, values=["empleado", "encargado", "supervisor"],
                    font=("JetBrains Mono", 10), width=120, height=28,
                    fg_color=FONDO_CARD, text_color=TEXTO_PRINCIPAL,
                    button_color=TRABAJO_ACTIVO,
                    command=lambda r, u=usr, rl=rol_label: self._cambiar_rol(u, r, rl),
                )
                combo.set(rol)
                combo.pack(side="right", padx=10)

        except Exception as e:
            ctk.CTkLabel(
                self.frame_usuarios,
                text=f"Error: {e}",
                font=("JetBrains Mono", 12), text_color=PELIGRO,
            ).pack(pady=10)

    def _cambiar_rol(self, usuario, nuevo_rol, label_rol):
        """Cambia el rol de un usuario."""
        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            coleccion.update_one(
                {'_id': usuario['_id']},
                {'$set': {'rol': nuevo_rol}}
            )
            label_rol.configure(text=nuevo_rol.upper(), text_color=self._color_rol(nuevo_rol))
        except Exception:
            pass

    @staticmethod
    def _color_rol(rol):
        return {
            'supervisor': AVISO,
            'encargado': INFORMACION,
            'empleado': TEXTO_SECUNDARIO,
        }.get(rol, TEXTO_SECUNDARIO)

    def _cargar_anomalias(self):
        """Carga anomalías recientes."""
        try:
            from src.db.conexion import conexion_global

            coleccion = conexion_global.obtener_coleccion('anomalias')
            anomalias = list(coleccion.find().sort('fecha_registro', -1).limit(20))

            for widget in self.frame_anomalias.winfo_children():
                widget.destroy()

            if not anomalias:
                ctk.CTkLabel(
                    self.frame_anomalias,
                    text="No hay anomalías registradas",
                    font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
                ).pack(pady=20)
                return

            pendientes = sum(1 for a in anomalias if not a.get('resuelto', False))
            self.badge_anomalias.configure(text=f"🚨 {pendientes} pendientes")

            for anom in anomalias:
                frame = ctk.CTkFrame(self.frame_anomalias, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                color = PELIGRO if not anom.get('resuelto', False) else COMPLETADO
                icono = "🔴" if not anom.get('resuelto', False) else "✅"

                ctk.CTkLabel(
                    frame, text=f"{icono} {anom.get('tipo', 'desconocido')}",
                    font=("JetBrains Mono", 11, "bold"), text_color=color,
                ).pack(side="left", padx=10, pady=6)

                ctk.CTkLabel(
                    frame, text=anom.get('detalle', '')[:50],
                    font=("JetBrains Mono", 10), text_color=TEXTO_SECUNDARIO,
                ).pack(side="left", padx=5)

                if not anom.get('resuelto', False):
                    ctk.CTkButton(
                        frame, text="Marcar vista",
                        font=("JetBrains Mono", 9),
                        fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
                        text_color=TEXTO_PRINCIPAL, height=24, width=80, corner_radius=4,
                        command=lambda a=anom: self._marcar_anomalia(a),
                    ).pack(side="right", padx=10)
        except Exception:
            pass

    def _marcar_anomalia(self, anomalia):
        """Marca una anomalía como revisada."""
        try:
            from src.db.anomalias import marcar_revisada
            marcar_revisada(str(anomalia['_id']))
            self._cargar_anomalias()
        except Exception:
            pass

    def _ver_descansos_fijos(self):
        """Abre la vista de configuración de descansos fijos."""
        try:
            from src.ui.config_descansos_view import ConfigDescansosView
            vista = ConfigDescansosView(self, self.usuario)
            vista.grab_set()
        except Exception:
            pass

    def _on_logout_click(self):
        self.on_logout()
