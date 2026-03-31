"""
Módulo: dashboard_empleado.py
Responsabilidad: Dashboard principal del empleado con timer Pomodoro.
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
        self.ciclo_activo = False
        self.estado_timer = "INACTIVO"
        self.segundos_restantes = 0
        self._job_timer = None
        self._crear_widgets()

    def _crear_widgets(self):
        # ── HEADER ──
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🍅 PomodoroSecure",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        nombre = self.usuario.get('nombre', 'Usuario')
        rol = self.usuario.get('rol', 'empleado')
        ctk.CTkLabel(
            header, text=f"{nombre} | {rol.title()}",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="right", padx=20)

        # ── BODY (panel lateral + central) ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # Panel lateral izquierdo
        lateral = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=220, corner_radius=12)
        lateral.pack(side="left", fill="y", padx=(0, 15))
        lateral.pack_propagate(False)

        ctk.CTkLabel(
            lateral, text="📊 Hoy",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.label_ciclos = ctk.CTkLabel(
            lateral, text="Ciclos: 0/∞",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_ciclos.pack(anchor="w", padx=15)

        self.label_trabajado = ctk.CTkLabel(
            lateral, text="Trabajado: 0h 0m",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_trabajado.pack(anchor="w", padx=15, pady=(3, 0))

        # Separador
        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            lateral, text="⏸ Pausas",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15)

        self.label_pausas = ctk.CTkLabel(
            lateral, text="○ ○  (0 usadas)",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_pausas.pack(anchor="w", padx=15, pady=(5, 0))

        # Separador
        ctk.CTkFrame(lateral, fg_color=BORDE, height=1).pack(fill="x", padx=15, pady=15)

        # Botones laterales
        ctk.CTkButton(
            lateral, text="🔑 Contraseña",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
            command=self.on_ver_contraseña,
        ).pack(fill="x", padx=15, pady=3)

        ctk.CTkButton(
            lateral, text="🚪 Cerrar Sesión",
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
            timer_card, text="🍅 INACTIVO",
            font=("JetBrains Mono", 18, "bold"), text_color=TEXTO_SECUNDARIO,
        )
        self.label_estado.pack(pady=(25, 5))

        self.label_countdown = ctk.CTkLabel(
            timer_card, text="25:00",
            font=("JetBrains Mono", 56, "bold"), text_color=TEXTO_PRINCIPAL,
        )
        self.label_countdown.pack()

        # Barra de progreso del pomodoro
        self.progreso_pomodoro = ctk.CTkProgressBar(
            timer_card,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            height=8,
            corner_radius=4,
        )
        self.progreso_pomodoro.pack(fill="x", padx=40, pady=(5, 15))
        self.progreso_pomodoro.set(0)

        # Botones de control
        botones_control = ctk.CTkFrame(timer_card, fg_color="transparent")
        botones_control.pack(pady=(0, 25))

        self.boton_iniciar = ctk.CTkButton(
            botones_control, text="▶ Iniciar Jornada",
            font=("JetBrains Mono", 14, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45, width=180, corner_radius=10,
            command=self._iniciar_ciclo,
        )
        self.boton_iniciar.pack(side="left", padx=5)

        self.boton_pausar = ctk.CTkButton(
            botones_control, text="⏸ Pausar",
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
            descansos_card, text="Próximos descansos",
            font=("JetBrains Mono", 13, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.label_descansos = ctk.CTkLabel(
            descansos_card,
            text="Corto 1: 5 min\nCorto 2: 5 min\nCorto 3: 5 min\nCorto 4: 5 min\nLargo: 30 min",
            font=("JetBrains Mono", 11),
            text_color=TEXTO_SECUNDARIO,
            justify="left",
        )
        self.label_descansos.pack(anchor="w", padx=20, pady=(0, 15))

    def _iniciar_ciclo(self):
        """Inicia un ciclo Pomodoro."""
        try:
            from src.timer import iniciar_ciclo
            resultado = iniciar_ciclo(str(self.usuario['_id']))
            self.ciclo_activo = True
            self.estado_timer = "TRABAJANDO"
            config = resultado.get('configuracion', {})
            self.segundos_restantes = config.get('pomodoro_min', 25) * 60

            self.boton_iniciar.configure(state="disabled")
            self.boton_pausar.configure(state="normal")
            self.label_estado.configure(text="🍅 TRABAJANDO", text_color=TRABAJO_ACTIVO)

            self._actualizar_countdown()
        except Exception as e:
            self.label_estado.configure(text=f"Error: {e}", text_color=PELIGRO)

    def _pausar_reanudar(self):
        """Pausa o reanuda el timer."""
        try:
            from src.pausas import iniciar_pausa, finalizar_pausa
            uid = str(self.usuario['_id'])

            if self.estado_timer == "PAUSADO":
                finalizar_pausa(uid)
                self.estado_timer = "TRABAJANDO"
                self.boton_pausar.configure(text="⏸ Pausar")
                self.label_estado.configure(text="🍅 TRABAJANDO", text_color=TRABAJO_ACTIVO)
                self._actualizar_countdown()
            else:
                iniciar_pausa(uid)
                self.estado_timer = "PAUSADO"
                self.boton_pausar.configure(text="▶ Reanudar")
                self.label_estado.configure(text="⏸ PAUSADO", text_color=TIMER_PAUSADO)
                if self._job_timer:
                    self.after_cancel(self._job_timer)
        except Exception as e:
            self.label_estado.configure(text=str(e), text_color=PELIGRO)

    def _actualizar_countdown(self):
        """Actualiza el countdown cada segundo."""
        if self.estado_timer == "PAUSADO":
            return

        if self.segundos_restantes > 0:
            self.segundos_restantes -= 1
            minutos = self.segundos_restantes // 60
            segundos = self.segundos_restantes % 60
            self.label_countdown.configure(text=f"{minutos:02d}:{segundos:02d}")

            # Actualizar progreso
            total = 25 * 60
            progreso = 1 - (self.segundos_restantes / total)
            self.progreso_pomodoro.set(progreso)

            self._job_timer = self.after(1000, self._actualizar_countdown)
        else:
            # Pomodoro completado
            self.label_countdown.configure(text="00:00")
            self.progreso_pomodoro.set(1)
            self._manejar_pomodoro_completado()

    def _manejar_pomodoro_completado(self):
        """Maneja la finalización de un pomodoro."""
        try:
            from src.timer import manejar_evento_timer
            uid = str(self.usuario['_id'])
            resultado = manejar_evento_timer(uid, "pomodoro_completado")

            accion = resultado.get('accion', '')
            duracion = resultado.get('datos_extra', {}).get('duracion_min', 5)

            if 'descanso' in accion:
                self.estado_timer = "DESCANSO"
                self.segundos_restantes = duracion * 60
                self.label_estado.configure(
                    text=f"☕ DESCANSO ({duracion} min)",
                    text_color=TIMER_DESCANSO_CORTO if 'corto' in accion else TIMER_DESCANSO_LARGO,
                )
                self._actualizar_countdown()
        except Exception:
            self.estado_timer = "INACTIVO"
            self.boton_iniciar.configure(state="normal")
            self.boton_pausar.configure(state="disabled")

    def _on_logout_click(self):
        if self._job_timer:
            self.after_cancel(self._job_timer)
        self.on_logout()

    def actualizar_pausas(self, usadas):
        """Actualiza el indicador de pausas."""
        estados = []
        for i in range(2):
            estados.append("●" if i < usadas else "○")
        self.label_pausas.configure(text=f"{' '.join(estados)}  ({usadas} usadas)")

    def limpiar(self):
        """Resetea el dashboard."""
        if self._job_timer:
            self.after_cancel(self._job_timer)
        self.ciclo_activo = False
        self.estado_timer = "INACTIVO"
        self.label_estado.configure(text="🍅 INACTIVO", text_color=TEXTO_SECUNDARIO)
        self.label_countdown.configure(text="25:00")
        self.progreso_pomodoro.set(0)
        self.boton_iniciar.configure(state="normal")
        self.boton_pausar.configure(state="disabled", text="⏸ Pausar")
