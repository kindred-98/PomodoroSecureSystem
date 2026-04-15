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
        
        # Login con frase semilla
        self._login_con_frase = None
    
    def set_login_frase_callback(self, callback):
        """Para configurar callback de login con frase."""
        self._login_con_frase = callback

    def _crear_widgets(self):
        # Contenedor central (card)
        card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=420,
            height=580,
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
            font=("Comic Sans MS", 20, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 25))

        # Campo Email
        ctk.CTkLabel(
            card,
            text="Email",
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=40)

        self.entry_email = ctk.CTkEntry(
            card,
            placeholder_text="usuario@empresa.com",
            font=("Comic Sans MS", 13),
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
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=40)

        self.entry_contraseña = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            show="•",
            font=("Comic Sans MS", 13),
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
            font=("Comic Sans MS", 11),
            text_color=TEXTO_SECUNDARIO,
            fg_color=FONDO_SECUNDARIO,
            checkmark_color=TEXTO_PRINCIPAL,
            hover_color=BOTON_PRIMARIO_HOVER,
        ).pack(anchor="w", padx=40, pady=(0, 15))

        # Label de error
        self.label_error = ctk.CTkLabel(
            card,
            text="",
            font=("Comic Sans MS", 11),
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 10))

        # Botón Iniciar Sesión
        self.boton_login = ctk.CTkButton(
            card,
            text="Iniciar Sesión",
            font=("Comic Sans MS", 14, "bold"),
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
            font=("Comic Sans MS", 12),
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
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=38,
            corner_radius=8,
            command=self._recuperar_contraseña,
        ).pack(fill="x", padx=40, pady=(5, 0))

        # Footer
        ctk.CTkLabel(
            self,
            text="v1.0.0 — Dicampus",
            font=("Comic Sans MS", 9),
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
        """Recuperar cuenta con frase semilla."""
        import customtkinter as ctk
        
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("🔑 Recuperar Cuenta")
        dialogo.geometry("480x400")
        dialogo.transient(self)
        dialogo.grab_set()
        
        ctk.CTkLabel(
            dialogo,
            text="🔑 Recuperar con Frase Semilla",
            font=("Comic Sans MS", 16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)
        
        # Email
        ctk.CTkLabel(
            dialogo,
            text="Tu Email:",
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(anchor="w", padx=40)
        
        entry_email = ctk.CTkEntry(
            dialogo, placeholder_text="tu@email.com",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=40,
        )
        entry_email.pack(fill="x", padx=40, pady=(5, 15))
        
        # Frase Semilla
        ctk.CTkLabel(
            dialogo,
            text="Tu Frase Semilla (12 palabras):",
            font=("Comic Sans MS", 12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(anchor="w", padx=40)
        
        entry_frase = ctk.CTkEntry(
            dialogo, placeholder_text="palabra1 palabra2 palabra3 ...",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=40,
        )
        entry_frase.pack(fill="x", padx=40, pady=(5, 20))
        
        label_error = ctk.CTkLabel(
            dialogo, text="", font=("Comic Sans MS", 11),
            text_color=PELIGRO,
        )
        label_error.pack(pady=5)
        
        def intentar_login():
            email = entry_email.get().strip()
            frase = entry_frase.get().strip()
            
            if not email or not frase:
                label_error.configure(text="Completa todos los campos")
                return
            
            # Verificar frase
            try:
                from src.db.conexion import conexion_global
                from src.auth.frase_semilla import verificar_frase_semilla
                from src.seguridad.encriptacion import verificar_contraseña
                
                usuarios = conexion_global.obtener_coleccion('usuarios')
                usuario = usuarios.find_one({'email': email})
                
                if not usuario:
                    label_error.configure(text="Email no encontrado")
                    return
                
                # Verificar frase
                uid = str(usuario['_id'])
                if not verificar_frase_semilla(uid, frase):
                    label_error.configure(text="Frase incorrecta")
                    return
                
                # Frase correcta - hacer login con frase
                dialogo.destroy()
                if hasattr(self, '_login_con_frase') and self._login_con_frase:
                    self._login_con_frase(email, usuario)
                else:
                    self.on_login(email, "")
                
            except Exception as e:
                label_error.configure(text=f"Error: {str(e)}")
        
        ctk.CTkButton(
            dialogo,
            text="✓ Entrar",
            font=("Comic Sans MS", 14, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45,
            command=intentar_login,
        ).pack(fill="x", padx=40, pady=(10, 5))
        
        ctk.CTkButton(
            dialogo,
            text="Cancelar",
            font=("Comic Sans MS", 12),
            command=dialogo.destroy,
        ).pack(pady=10)
        self.boton_login.configure(state="normal", text="Iniciar Sesión")

