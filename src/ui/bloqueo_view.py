"""
Módulo: bloqueo_view.py
Responsabilidad: Pantalla de bloqueo fullscreen durante descansos.
Integración con OTP y bloqueo de Windows.
"""

import customtkinter as ctk
from src.config.colores import *


class BloqueoView(ctk.CTkToplevel):
    """Pantalla fullscreen topmost durante descansos."""

    def __init__(self, parent, tipo_descanso="corto", duracion_min=5, on_verificado=None):
        super().__init__(parent)
        self.tipo_descanso = tipo_descanso
        self.duracion_seg = duracion_min * 60
        self.on_verificado = on_verificado
        self._job_timer = None

        self._configurar_ventana()
        self._crear_widgets()
        self._iniciar_countdown()

    def _configurar_ventana(self):
        self.title("PomodoroSecure — Descanso")
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.configure(fg_color=self._color_fondo())
        self.protocol("WM_DELETE_WINDOW", lambda: None)  # No se puede cerrar

    def _color_fondo(self):
        return {
            "corto": BLOQUEO_CORTO,
            "largo": BLOQUEO_LARGO,
            "fijo": BLOQUEO_FIJO,
        }.get(self.tipo_descanso, BLOQUEO_CORTO)

    def _crear_widgets(self):
        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.place(relx=0.5, rely=0.45, anchor="center")

        emoji = {"corto": "☕", "largo": "🌴", "fijo": "🍽️"}
        ctk.CTkLabel(
            centro,
            text=emoji.get(self.tipo_descanso, "☕"),
            font=("Segoe UI Emoji", 72),
            text_color=TEXTO_PRINCIPAL,
        ).pack()

        ctk.CTkLabel(
            centro,
            text=f"DESCANSO {self.tipo_descanso.upper()}",
            font=("Comic Sans MS", 28, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(10, 5))

        self.label_countdown = ctk.CTkLabel(
            centro,
            text=self._formatear_tiempo(self.duracion_seg),
            font=("Comic Sans MS", 72, "bold"),
            text_color=TEXTO_PRINCIPAL,
        )
        self.label_countdown.pack(pady=10)

        ctk.CTkLabel(
            centro,
            text="tiempo de descanso restante",
            font=("Comic Sans MS", 14),
            text_color=TEXTO_SECUNDARIO,
        ).pack()

        # Mensaje motivacional
        ctk.CTkLabel(
            centro,
            text="Aprovecha para estirarte,\nhidratarte y descansar la vista.",
            font=("Comic Sans MS", 13),
            text_color=TEXTO_SECUNDARIO,
            justify="center",
        ).pack(pady=(25, 20))

        # Frame OTP (aparece cuando termina el descanso)
        self.frame_otp = ctk.CTkFrame(centro, fg_color="transparent")
        self.frame_otp.pack_forget()

        ctk.CTkLabel(
            self.frame_otp,
            text="Introduce tu código de retorno:",
            font=("Comic Sans MS", 14),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 5))

        self.entry_otp = ctk.CTkEntry(
            self.frame_otp,
            placeholder_text="_ _ _ _ _ _",
            font=("Comic Sans MS", 24),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=50,
            width=200,
            corner_radius=10,
            justify="center",
        )
        self.entry_otp.pack()

        self.label_otp_estado = ctk.CTkLabel(
            self.frame_otp,
            text="",
            font=("Comic Sans MS", 12),
            text_color=PELIGRO,
        )
        self.label_otp_estado.pack(pady=(5, 0))

        self.boton_verificar = ctk.CTkButton(
            self.frame_otp,
            text="Confirmar",
            font=("Comic Sans MS", 14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            width=180,
            corner_radius=10,
            command=self._verificar_otp,
        )
        self.boton_verificar.pack(pady=10)

    def _iniciar_countdown(self):
        if self.duracion_seg > 0:
            self.duracion_seg -= 1
            self.label_countdown.configure(text=self._formatear_tiempo(self.duracion_seg))
            self._job_timer = self.after(1000, self._iniciar_countdown)
        else:
            # Descanso terminado — solicitar OTP
            self._mostrar_campo_otp()

    def _mostrar_campo_otp(self):
        self.label_countdown.configure(text="00:00", text_color=AVISO)
        self.frame_otp.pack(pady=(15, 0))
        self.entry_otp.focus()

    def _verificar_otp(self):
        codigo = self.entry_otp.get().strip()
        if not codigo or len(codigo) != 6:
            self.label_otp_estado.configure(text="El código debe tener 6 dígitos")
            return

        try:
            from src.otp import verificar_otp
            usuario_id = str(self.master.usuario_actual['_id'])
            resultado = verificar_otp(usuario_id, codigo)

            if resultado['correcto']:
                self.label_otp_estado.configure(text="✅ Correcto", text_color=COMPLETADO)
                self.after(800, self._cerrar_y_continuar)
            elif resultado['requiere_credenciales']:
                self.label_otp_estado.configure(
                    text="3 intentos fallidos. Introduce tus credenciales.",
                    text_color=PELIGRO,
                )
            else:
                restantes = resultado['intentos_restantes']
                self.label_otp_estado.configure(
                    text=f"Incorrecto. Quedan {restantes} intento(s).",
                    text_color=PELIGRO,
                )
                self.entry_otp.delete(0, "end")
        except Exception as e:
            self.label_otp_estado.configure(text=str(e))

    def _cerrar_y_continuar(self):
        if self._job_timer:
            self.after_cancel(self._job_timer)
        if self.on_verificado:
            self.on_verificado()
        self.destroy()

    @staticmethod
    def _formatear_tiempo(segundos):
        m = segundos // 60
        s = segundos % 60
        return f"{m:02d}:{s:02d}"

