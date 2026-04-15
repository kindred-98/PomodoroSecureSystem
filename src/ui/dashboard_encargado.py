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
        self._job_refresh = None
        self._crear_widgets()
        self._sincronizar_con_servicio()
        self._iniciar_refresh()

    def _crear_widgets(self):
        # HEADER
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🍅 PomodoroSecure",
            font=("Comic Sans MS", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        nombre = self.usuario.get('nombre', 'Encargado')
        ctk.CTkLabel(
            header, text=f"{nombre} | Encargado",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="right", padx=20)

        # BODY
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # Panel lateral izquierdo (stats + acciones)
        lateral = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=220, corner_radius=12)
        lateral.pack(side="left", fill="y", padx=(0, 15))
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral, text="Hoy",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.label_ciclos = ctk.CTkLabel(
            lateral, text="Ciclos: 0/inf",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_ciclos.pack(anchor="w", padx=15)

        self.label_trabajado = ctk.CTkLabel(
            lateral, text="Trabajado: 0h 0m",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_trabajado.pack(anchor="w", padx=15, pady=(3, 0))

        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            lateral, text="Pausas",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15)

        self.label_pausas = ctk.CTkLabel(
            lateral, text="O O  (0 usadas)",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_pausas.pack(anchor="w", padx=15, pady=(5, 0))

        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        botones_lateral = [
            ("🔑 Contraseña", self.on_ver_contraseña),
            ("📋 Historial", self.on_ver_historial),
            ("Fin de Jornada", self._fin_jornada_click),
            ("🚪 Cerrar Sesión", self._on_logout_click),
        ]
        for texto, cmd in botones_lateral:
            color = BOTON_PELIGRO if "Sesión" in texto else ("#E67E22" if "Jornada" in texto else BOTON_SECUNDARIO)
            hover = BOTON_PELIGRO_HOVER if "Sesión" in texto else ("#D35400" if "Jornada" in texto else BOTON_SECUNDARIO_HOVER)
            ctk.CTkButton(
                lateral, text=texto,
                font=("Comic Sans MS", 12),
                fg_color=color, hover_color=hover,
                text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
                command=cmd,
            ).pack(fill="x", padx=15, pady=3)

        # Panel central
        central = ctk.CTkFrame(body, fg_color="transparent")
        central.pack(side="right", fill="both", expand=True)

        # Card del timer
        timer_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=16)
        timer_card.pack(fill="x", pady=(0, 15))

        self.label_estado = ctk.CTkLabel(
            timer_card, text="INACTIVO",
            font=("Comic Sans MS", 18, "bold"), text_color=TEXTO_SECUNDARIO,
        )
        self.label_estado.pack(pady=(25, 5))

        self.label_countdown = ctk.CTkLabel(
            timer_card, text="25:00",
            font=("Comic Sans MS", 56, "bold"), text_color=TEXTO_PRINCIPAL,
        )
        self.label_countdown.pack()

        self.progreso_pomodoro = ctk.CTkProgressBar(
            timer_card,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            height=8, corner_radius=4,
        )
        self.progreso_pomodoro.pack(fill="x", padx=40, pady=(5, 15))
        self.progreso_pomodoro.set(0)

        botones_control = ctk.CTkFrame(timer_card, fg_color="transparent")
        botones_control.pack(pady=(0, 25))

        self.boton_iniciar = ctk.CTkButton(
            botones_control, text="Iniciar Jornada",
            font=("Comic Sans MS", 14, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45, width=180, corner_radius=10,
            command=self._iniciar_ciclo,
        )
        self.boton_iniciar.pack(side="left", padx=5)

        self.boton_pausar = ctk.CTkButton(
            botones_control, text="Pausar",
            font=("Comic Sans MS", 13),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45, width=130, corner_radius=10,
            command=self._pausar_reanudar,
            state="disabled",
        )
        self.boton_pausar.pack(side="left", padx=5)

        # ── Mi Equipo ──
        equipo_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        equipo_card.pack(fill="both", expand=True)

        header_equipo = ctk.CTkFrame(equipo_card, fg_color="transparent")
        header_equipo.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            header_equipo, text="👥 Mi Equipo",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left")

        self.badge_anomalias = ctk.CTkLabel(
            header_equipo, text="",
            font=("Comic Sans MS", 12, "bold"), text_color=PELIGRO,
        )
        self.badge_anomalias.pack(side="right")

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
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_vacio.pack(pady=20)

        # Cargar equipo
        self._cargar_equipo()

    def _sincronizar_con_servicio(self):
        """Lee el estado del servicio y actualiza la UI."""
        from src.timer.servicio_timer import servicio_timer
        estado = servicio_timer.obtener_estado()
        self._actualizar_labels(estado)

    def _iniciar_refresh(self):
        """Inicia el loop de actualización cada 1 segundo."""
        self._job_refresh = self.after(1000, self._refrescar)

    def _refrescar(self):
        """Lee el estado del servicio y actualiza la UI."""
        try:
            from src.timer.servicio_timer import servicio_timer
            resultado = servicio_timer.tick()
            estado = resultado
            self._actualizar_labels(estado)
            self._actualizar_miembros()
        except Exception:  # nosec
            pass
        self._job_refresh = self.after(1000, self._refrescar)

    def _actualizar_labels(self, estado):
        """Actualiza todos los labels con el estado del servicio."""
        est = estado.get('estado', 'INACTIVO')
        seg = estado.get('segundos_restantes', 0)
        total = estado.get('segundos_totales', 1)
        pom_actual = estado.get('pomodoro_actual', 0)
        pom_total = estado.get('pomodoros_totales', 4)
        pausas = estado.get('pausas_usadas', 0)
        pausas_max = estado.get('pausas_maximas', 2)
        activo = estado.get('ciclo_activo', False)

        # Countdown
        minutos = seg // 60
        segundos = seg % 60
        self.label_countdown.configure(text=f"{minutos:02d}:{segundos:02d}")

        # Progreso
        if total > 0:
            progreso = 1 - (seg / total)
            self.progreso_pomodoro.set(progreso)

        # Estado
        if est == "INACTIVO":
            self.label_estado.configure(text="INACTIVO", text_color=TEXTO_SECUNDARIO)
            self.boton_iniciar.configure(state="normal")
            self.boton_pausar.configure(state="disabled", text="Pausar")
            self.progreso_pomodoro.set(0)
        elif est == "TRABAJANDO":
            self.label_estado.configure(
                text=f"TRABAJANDO (Pom {pom_actual}/{pom_total})",
                text_color=TRABAJO_ACTIVO
            )
            self.boton_iniciar.configure(state="disabled")
            self.boton_pausar.configure(state="normal", text="Pausar")
        elif est == "PAUSADO":
            self.label_estado.configure(text="PAUSADO", text_color=TIMER_PAUSADO)
            self.boton_pausar.configure(state="normal", text="Reanudar")
        elif est == "DESCANSO_CORTO":
            self.label_estado.configure(
                text=f"DESCANSO CORTO ({seg // 60 + 1} min)",
                text_color=TIMER_DESCANSO_CORTO
            )
            self.boton_iniciar.configure(state="disabled")
            self.boton_pausar.configure(state="disabled")
        elif est == "DESCANSO_LARGO":
            self.label_estado.configure(
                text=f"DESCANSO LARGO ({seg // 60 + 1} min)",
                text_color=TIMER_DESCANSO_LARGO
            )
            self.boton_iniciar.configure(state="disabled")
            self.boton_pausar.configure(state="disabled")

        # Pausas
        estados_p = []
        for i in range(pausas_max):
            estados_p.append("X" if i < pausas else "O")
        self.label_pausas.configure(text=f"{' '.join(estados_p)}  ({pausas}/{pausas_max})")

    def _iniciar_ciclo(self):
        """Inicia un ciclo Pomodoro via servicio."""
        try:
            from src.timer.servicio_timer import servicio_timer
            uid = str(self.usuario['_id'])
            servicio_timer.iniciar(uid)
            self._sincronizar_con_servicio()
        except Exception as e:
            self.label_estado.configure(text=f"Error: {e}", text_color=PELIGRO)

    def _pausar_reanudar(self):
        """Pausa o reanuda via servicio."""
        try:
            from src.timer.servicio_timer import servicio_timer
            estado = servicio_timer.obtener_estado()

            if estado['estado'] == "PAUSADO":
                servicio_timer.reanudar()
            else:
                servicio_timer.pausar()

            self._sincronizar_con_servicio()
        except Exception as e:
            self.label_estado.configure(text=str(e), text_color=PELIGRO)

    def _fin_jornada_click(self):
        """Maneja el click en 'Fin de jornada laboral'."""
        from src.timer.servicio_timer import servicio_timer
        
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Fin de Jornada")
        dialogo.geometry("400x200")
        dialogo.transient(self)
        dialogo.grab_set()
        
        x = (dialogo.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialogo.winfo_screenheight() // 2) - (200 // 2)
        dialogo.geometry(f"400x200+{x}+{y}")
        
        ctk.CTkLabel(
            dialogo,
            text="¿Finalizar jornada laboral?",
            font=("Comic Sans MS", 16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialogo,
            text="Se generará un reporte con tu actividad\ny se reiniciarán todos los contadores.",
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=10)
        
        botones = ctk.CTkFrame(dialogo, fg_color="transparent")
        botones.pack(pady=20)
        
        def confirmar():
            uid = str(self.usuario['_id'])
            resultado = servicio_timer.fin_jornada_laboral(uid)
            
            if resultado.get('exito'):
                resumen = resultado.get('resumen', {})
                mensaje = (
                    f"Jornada finalizada\n\n"
                    f"Ciclos: {resumen.get('ciclos_iniciados', 0)}\n"
                    f"Pomodoros: {resumen.get('pomodoros_totales', 0)}\n"
                    f"Trabajado: {resumen.get('tiempo_trabajado', '0m')}"
                )
                ctk.CTkLabel(
                    dialogo,
                    text=mensaje,
                    font=("Comic Sans MS", 12),
                    text_color="#2ECC71",
                ).pack(pady=20)
                
                dialogo.after(2000, dialogo.destroy)
                self._sincronizar_con_servicio()
            else:
                ctk.CTkLabel(
                    dialogo,
                    text=f"Error: {resultado.get('error', 'Desconocido')}",
                    font=("Comic Sans MS", 12),
                    text_color=PELIGRO,
                ).pack(pady=20)
        
        ctk.CTkButton(
            botones, text="Confirmar",
            font=("Comic Sans MS", 12),
            fg_color="#27AE60", hover_color="#219A52",
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=confirmar,
            width=120,
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            botones, text="Cancelar",
            font=("Comic Sans MS", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=dialogo.destroy,
            width=120,
        ).pack(side="left", padx=10)

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
            else:
                self.label_vacio.configure(text="No tienes un equipo asignado.")
        except Exception as e:
            self.label_vacio.configure(text=f"Error al cargar equipo: {e}")

    def _actualizar_miembros(self):
        """Reconstruye la lista de miembros con estado real."""
        for widget in self.frame_miembros.winfo_children():
            widget.destroy()

        from src.db.conexion import conexion_global
        coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')

        if not self._miembros_cache:
            self.label_vacio.configure(text="No tienes un equipo asignado.")
            return

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
                font=("Comic Sans MS", 12, "bold"), text_color=TEXTO_PRINCIPAL,
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                info, text=f"{miembro.get('rol', 'empleado').title()} — {texto}",
                font=("Comic Sans MS", 10), text_color=color,
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
                seg_restantes = ciclo.get('segundos_totales', 1500) - ciclo.get('segundos_restantes', 0)
                min_restantes = max(0, (seg_restantes + 59) // 60)
                return "🟢", COMPLETADO, f"Trabajando ({min_restantes}min - Pom {pom}/{total})"
            elif estado == 'PAUSADO':
                return "🟡", AVISO, "En pausa"
            elif estado in ('DESCANSO_CORTO', 'DESCANSO_LARGO'):
                seg_restantes = ciclo.get('segundos_totales', 300) - ciclo.get('segundos_restantes', 0)
                min_restantes = max(0, (seg_restantes + 59) // 60)
                tipo = "corto" if 'CORTO' in estado else "largo"
                return "☕", TIMER_DESCANSO_CORTO if tipo == "corto" else TIMER_DESCANSO_LARGO, f"Descanso {tipo} ({min_restantes}min)"
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
        except Exception:  # nosec
            pass

    def _on_logout_click(self):
        from src.timer.servicio_timer import servicio_timer
        servicio_timer.destruir()
        if self._job_refresh:
            self.after_cancel(self._job_refresh)
        self.on_logout()

    def destroy(self):
        if self._job_refresh:
            self.after_cancel(self._job_refresh)
        super().destroy()

