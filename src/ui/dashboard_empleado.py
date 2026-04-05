"""
Módulo: dashboard_empleado.py
Responsabilidad: Dashboard principal del empleado con timer Pomodoro.
Lee el estado del servicio_timer (no lo posee).
"""

import customtkinter as ctk
from src.config.colores import *


class DashboardEmpleado(ctk.CTkFrame):
    """Dashboard del empleado con timer, pausas y navegación."""

    def __init__(self, parent, usuario, on_logout, on_ver_contraseña):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_logout = on_logout
        self.on_ver_contraseña = on_ver_contraseña
        self._job_refresh = None
        self._crear_widgets()
        self._sincronizar_con_servicio()
        self._iniciar_refresh()

    def _crear_widgets(self):
        from src.timer.servicio_timer import servicio_timer

        # HEADER
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="PomodoroSecure",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        nombre = self.usuario.get('nombre', 'Usuario')
        rol = self.usuario.get('rol', 'empleado')
        ctk.CTkLabel(
            header, text=f"{nombre} | {rol.title()}",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="right", padx=20)

        # BODY
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # Panel lateral
        lateral = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=220, corner_radius=12)
        lateral.pack(side="left", fill="y", padx=(0, 15))
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral, text="Hoy",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.label_ciclos = ctk.CTkLabel(
            lateral, text="Ciclos: 0/inf",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_ciclos.pack(anchor="w", padx=15)

        self.label_trabajado = ctk.CTkLabel(
            lateral, text="Trabajado: 0h 0m",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_trabajado.pack(anchor="w", padx=15, pady=(3, 0))

        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            lateral, text="Pausas",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15)

        self.label_pausas = ctk.CTkLabel(
            lateral, text="O O  (0 usadas)",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_pausas.pack(anchor="w", padx=15, pady=(5, 0))

        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        # Botón Descansos solo para supervisor
        if self.usuario.get('rol') == 'supervisor':
            ctk.CTkButton(
                lateral, text="Descansos (empresa)",
                font=("JetBrains Mono", 12),
                fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
                text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
                command=self._ver_descansos,
            ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            lateral, text="Contrasena",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=self.on_ver_contraseña,
        ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            lateral, text="Fin de Jornada",
            font=("JetBrains Mono", 12),
            fg_color="#E67E22", hover_color="#D35400",
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=self._fin_jornada_click,
        ).pack(fill="x", padx=15, pady=(3, 0))

        ctk.CTkButton(
            lateral, text="Cerrar Sesion",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_PELIGRO, hover_color=BOTON_PELIGRO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=self._on_logout_click,
        ).pack(fill="x", padx=15, pady=3)

        # Panel central
        central = ctk.CTkFrame(body, fg_color="transparent")
        central.pack(side="right", fill="both", expand=True)

        # Card del timer
        timer_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=16)
        timer_card.pack(fill="x", pady=(0, 15))

        self.label_estado = ctk.CTkLabel(
            timer_card, text="INACTIVO",
            font=("JetBrains Mono", 18, "bold"), text_color=TEXTO_SECUNDARIO,
        )
        self.label_estado.pack(pady=(25, 5))

        self.label_countdown = ctk.CTkLabel(
            timer_card, text="25:00",
            font=("JetBrains Mono", 56, "bold"), text_color=TEXTO_PRINCIPAL,
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
            font=("JetBrains Mono", 14, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45, width=180, corner_radius=10,
            command=self._iniciar_ciclo,
        )
        self.boton_iniciar.pack(side="left", padx=5)

        self.boton_pausar = ctk.CTkButton(
            botones_control, text="Pausar",
            font=("JetBrains Mono", 13),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45, width=130, corner_radius=10,
            command=self._pausar_reanudar,
            state="disabled",
        )
        self.boton_pausar.pack(side="left", padx=5)

        # Info de descansos
        descansos_card = ctk.CTkFrame(central, fg_color=FONDO_CARD, corner_radius=12)
        descansos_card.pack(fill="x")

        ctk.CTkLabel(
            descansos_card, text="Proximos descansos",
            font=("JetBrains Mono", 13, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.label_descansos = ctk.CTkLabel(
            descansos_card,
            text="Corto 1: 5 min\nCorto 2: 5 min\nCorto 3: 5 min\nCorto 4: 5 min\nLargo: 30 min",
            font=("JetBrains Mono", 11),
            text_color=TEXTO_SECUNDARIO, justify="left",
        )
        self.label_descansos.pack(anchor="w", padx=20, pady=(0, 15))

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
        except Exception:
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

    def _ver_descansos(self):
        """Abre la vista de configuracion de descansos."""
        try:
            from src.ui.config_descansos_view import ConfigDescansosView
            vista = ConfigDescansosView(self, self.usuario)
            vista.grab_set()
        except Exception:
            pass

    def _fin_jornada_click(self):
        """Maneja el click en 'Fin de jornada laboral'."""
        from src.timer.servicio_timer import servicio_timer
        import customtkinter as ctk
        
        # Diálogo de confirmación
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Fin de Jornada")
        dialogo.geometry("400x200")
        dialogo.transient(self)
        dialogo.grab_set()
        
        # Centrar
        dialogo.update_idletasks()
        x = (dialogo.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialogo.winfo_screenheight() // 2) - (200 // 2)
        dialogo.geometry(f"400x200+{x}+{y}")
        
        # Contenido
        ctk.CTkLabel(
            dialogo,
            text="¿Finalizar jornada laboral?",
            font=("JetBrains Mono", 16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialogo,
            text="Se generará un reporte con tu actividad\ny se reiniciarán todos los contadores.",
            font=("JetBrains Mono", 12),
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
                    font=("JetBrains Mono", 12),
                    text_color="#2ECC71",
                ).pack(pady=20)
                
                dialogo.after(2000, dialogo.destroy)
                self._sincronizar_con_servicio()
            else:
                ctk.CTkLabel(
                    dialogo,
                    text=f"Error: {resultado.get('error', 'Desconocido')}",
                    font=("JetBrains Mono", 12),
                    text_color=PELIGRO,
                ).pack(pady=20)
        
        ctk.CTkButton(
            botones, text="Confirmar",
            font=("JetBrains Mono", 12),
            fg_color="#27AE60", hover_color="#219A52",
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=confirmar,
            width=120,
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            botones, text="Cancelar",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=dialogo.destroy,
            width=120,
        ).pack(side="left", padx=10)

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
