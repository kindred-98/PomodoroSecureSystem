"""
Módulo: login_view.py
Responsabilidad: Pantalla de login con email y contraseña.
"""

import customtkinter as ctk
from src.config.colores import *


class LoginView(ctk.CTkFrame):
    """Pantalla de login."""

    def __init__(self, parent, on_login, on_ir_registro):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.on_login = on_login
        self.on_ir_registro = on_ir_registro
        self._crear_widgets()

    def _crear_widgets(self):
        # Contenedor central (card)
        card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=400,
            height=480,
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Logo
        ctk.CTkLabel(
            card,
            text="🍅🔐",
            font=("Segoe UI Emoji", 40),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            card,
            text="PomodoroSecure",
            font=("JetBrains Mono", 20, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 25))

        # Campo Email
        ctk.CTkLabel(
            card,
            text="Email",
            font=("JetBrains Mono", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=40)

        self.entry_email = ctk.CTkEntry(
            card,
            placeholder_text="usuario@empresa.com",
            font=("JetBrains Mono", 13),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=40,
            corner_radius=8,
        )
        self.entry_email.pack(fill="x", padx=40, pady=(5, 15))

        # Campo Contraseña
        ctk.CTkLabel(
            card,
            text="Contraseña",
            font=("JetBrains Mono", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=40)

        self.entry_contraseña = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            show="•",
            font=("JetBrains Mono", 13),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=40,
            corner_radius=8,
        )
        self.entry_contraseña.pack(fill="x", padx=40, pady=(5, 5))

        # Toggle mostrar contraseña
        self.mostrar_pw = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            card,
            text="Mostrar contraseña",
            variable=self.mostrar_pw,
            command=self._toggle_contraseña,
            font=("JetBrains Mono", 11),
            text_color=TEXTO_SECUNDARIO,
            fg_color=FONDO_SECUNDARIO,
            checkmark_color=TEXTO_PRINCIPAL,
            hover_color=BOTON_PRIMARIO_HOVER,
        ).pack(anchor="w", padx=40, pady=(0, 15))

        # Label de error
        self.label_error = ctk.CTkLabel(
            card,
            text="",
            font=("JetBrains Mono", 11),
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 10))

        # Botón Iniciar Sesión
        self.boton_login = ctk.CTkButton(
            card,
            text="Iniciar Sesión",
            font=("JetBrains Mono", 14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            corner_radius=10,
            command=self._on_login_click,
        )
        self.boton_login.pack(fill="x", padx=40, pady=(0, 15))

        # Botón Registro
        ctk.CTkButton(
            card,
            text="¿Primera vez? Regístrate",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=INFORMACION,
            height=36,
            corner_radius=8,
            command=self.on_ir_registro,
        ).pack(fill="x", padx=40, pady=(0, 5))

        # Olvidé mi contraseña
        ctk.CTkButton(
            card,
            text="¿Olvidaste tu contraseña? Usa Frase Semilla",
            font=("JetBrains Mono", 11),
            fg_color="transparent",
            text_color=TEXTO_SECUNDARIO,
            height=30,
            corner_radius=8,
            command=self._recuperar_contraseña,
        ).pack(pady=(5, 0))

        # Footer
        ctk.CTkLabel(
            self,
            text="v1.0.0 — Dicampus",
            font=("JetBrains Mono", 9),
            text_color=TEXTO_SECUNDARIO,
        ).place(relx=0.5, rely=0.95, anchor="center")

    def _toggle_contraseña(self):
        self.entry_contraseña.configure(
            show="" if self.mostrar_pw.get() else "•"
        )

    def _on_login_click(self):
        email = self.entry_email.get().strip()
        contraseña = self.entry_contraseña.get()

        if not email or not contraseña:
            self.label_error.configure(text="Todos los campos son obligatorios")
            return

        self.label_error.configure(text="")
        self.boton_login.configure(state="disabled", text="Verificando...")

        try:
            self.on_login(email, contraseña)
        except Exception as e:
            self.label_error.configure(text=str(e))
            self.boton_login.configure(state="normal", text="Iniciar Sesión")

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en la pantalla de login."""
        self.label_error.configure(text=mensaje)
        self.boton_login.configure(state="normal", text="Iniciar Sesión")

    def limpiar(self):
        """Limpia los campos del formulario."""
        self.entry_email.delete(0, "end")
        self.entry_contraseña.delete(0, "end")
        self.label_error.configure(text="")

    def _recuperar_contraseña(self):
        """Muestra info sobre recuperacion con frase semilla."""
        import customtkinter as ctk
        
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Recuperar Cuenta")
        dialogo.geometry("450x250")
        dialogo.transient(self)
        dialogo.grab_set()
        
        ctk.CTkLabel(
            dialogo,
            text="🔑 Recuperar mi Cuenta",
            font=("JetBrains Mono", 16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialogo,
            text="Si perdiste tu contraseña, usa tu Frase Semilla.\n\n"
            "La generaste en: Cambiar contraseña → Frase Semilla.\n"
            "Guárdala en un lugar seguro.",
            font=("JetBrains Mono", 12),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=10)
        
        ctk.CTkButton(
            dialogo,
            text="Cerrar",
            font=("JetBrains Mono", 12),
            command=dialogo.destroy,
        ).pack(pady=15)
        self.boton_login.configure(state="normal", text="Iniciar Sesión")
