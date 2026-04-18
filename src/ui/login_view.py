"""
Módulo: login_view.py
Responsabilidad: Pantalla de login con email y contraseña.
"""

import customtkinter as ctk
from src.ui.templates import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER, BOTON_SECUNDARIO, BOTON_SECUNDARIO_HOVER,
    crear_fuente, NORMAL_NEGRITA, PEQUENO, MINIMO
)


class LoginView(ctk.CTkFrame):
    """Pantalla de login."""

    # ============================================
    # INICIALIZACIÓN
    # ============================================

    def __init__(self, parent, on_login, on_ir_registro):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.on_login = on_login
        self.on_ir_registro = on_ir_registro
        self._login_con_frase = None
        self._crear_widgets()

    def set_login_frase_callback(self, callback):
        """Configura callback de login con frase."""
        self._login_con_frase = callback

    # ============================================
    # CREACIÓN DE WIDGETS
    # ============================================

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        self._crear_card()
        self._crear_logo()
        self._crear_campos()
        self._crear_checkbox()
        self._crear_label_error()
        self._crear_botones()
        self._crear_footer()

    # --------------------------------------------
    # Card central
    # --------------------------------------------

    def _crear_card(self):
        """Crea el card central."""
        self.card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=660,
            height=760,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

    # --------------------------------------------
    # Logo y título
    # --------------------------------------------

    def _crear_logo(self):
        """Crea el logo y título de la app."""
        # Emoji logo
        ctk.CTkLabel(
            self.card,
            text="🍅🔐",
            font=("Segoe UI Emoji", 56),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(35, 5))

        # Título
        ctk.CTkLabel(
            self.card,
            text="PomodoroSecure",
            font=crear_fuente(26, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 30))

    # --------------------------------------------
    # Campos de entrada
    # --------------------------------------------

    def _crear_campos(self):
        """Crea los campos de email y contraseña."""
        # Email
        self._crear_campo_email()
        # Contraseña
        self._crear_campo_contraseña()

    def _crear_campo_email(self):
        """Crea el campo de email."""
        ctk.CTkLabel(
            self.card,
            text="Email",
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=45)

        self.entry_email = ctk.CTkEntry(
            self.card,
            placeholder_text="TuCorreo@empresa.com",
            font=crear_fuente(15),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=48,
            corner_radius=8,
        )
        self.entry_email.pack(fill="x", padx=45, pady=(5, 15))

    def _crear_campo_contraseña(self):
        """Crea el campo de contraseña."""
        ctk.CTkLabel(
            self.card,
            text="Contraseña",
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=45)

        self.entry_contraseña = ctk.CTkEntry(
            self.card,
            placeholder_text="••••••••",
            show="•",
            font=crear_fuente(15),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=48,
            corner_radius=8,
        )
        self.entry_contraseña.pack(fill="x", padx=45, pady=(5, 5))

    # --------------------------------------------
    # Checkbox mostrar contraseña
    # --------------------------------------------

    def _crear_checkbox(self):
        """Crea el checkbox para mostrar contraseña."""
        self.mostrar_pw = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self.card,
            text="Mostrar contraseña",
            variable=self.mostrar_pw,
            command=self._toggle_contraseña,
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            fg_color=FONDO_SECUNDARIO,
            checkmark_color=TEXTO_PRINCIPAL,
            hover_color=BOTON_PRIMARIO_HOVER,
        ).pack(anchor="w", padx=45, pady=(0, 15))

    # --------------------------------------------
    # Label de error
    # --------------------------------------------

    def _crear_label_error(self):
        """Crea el label para mensajes de error."""
        self.label_error = ctk.CTkLabel(
            self.card,
            text="",
            font=PEQUENO,
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 10))

    # --------------------------------------------
    # Botones de acción
    # --------------------------------------------

    def _crear_botones(self):
        """Crea los botones de acción."""
        footer = ctk.CTkFrame(self.card, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=45, pady=(0, 25))

        # Botón Iniciar Sesión
        self.boton_login = ctk.CTkButton(
            footer,
            text="Iniciar Sesión",
            font=NORMAL_NEGRITA,
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=52,
            corner_radius=10,
            command=self._on_login_click,
        )
        self.boton_login.pack(fill="x", pady=(0, 10))

        # Botón Registro
        ctk.CTkButton(
            footer,
            text="¿Primera vez? Regístrate",
            font=NORMAL_NEGRITA,
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=INFORMACION,
            height=45,
            corner_radius=8,
            command=self.on_ir_registro,
        ).pack(fill="x", pady=(0, 10))

        # Botón Recuperar
        ctk.CTkButton(
            footer,
            text="¿Olvidaste tu contraseña? Usa Frase Semilla",
            font=crear_fuente(14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            corner_radius=8,
            command=self._recuperar_contraseña,
        ).pack(fill="x")

    # --------------------------------------------
    # Footer versión
    # --------------------------------------------

    def _crear_footer(self):
        """Crea el pie de página."""
        ctk.CTkLabel(
            self,
            text="v1.0.0 — Dicampus",
            font=MINIMO,
            text_color=TEXTO_SECUNDARIO,
        ).place(relx=0.5, rely=0.95, anchor="center")

    # ============================================
    # EVENTOS
    # ============================================

    def _toggle_contraseña(self):
        """Alterna mostrar/ocultar contraseña."""
        self.entry_contraseña.configure(
            show="" if self.mostrar_pw.get() else "•"
        )

    def _on_login_click(self):
        """Procesa el intento de login."""
        email = self.entry_email.get().strip()
        contraseña = self.entry_contraseña.get()

        # Validaciones
        if not email:
            self._mostrar_error("El email es obligatorio")
            return

        if not contraseña:
            self._mostrar_error("La contraseña es obligatoria")
            return

        if len(email) > 64:
            self._mostrar_error("El email debe tener máximo 64 caracteres")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            self._mostrar_error("El formato del email es inválido")
            return

        # Login
        self.label_error.configure(text="")
        self.boton_login.configure(state="disabled", text="Verificando...")

        try:
            self.on_login(email, contraseña)
        except Exception as e:
            self._mostrar_error(str(e))

    def _mostrar_error(self, mensaje):
        """Muestra mensaje de error y resetea botón."""
        self.label_error.configure(text=mensaje)
        self.boton_login.configure(state="normal", text="Iniciar Sesión")

    # ============================================
    # RECUPERACIÓN DE CONTRASEÑA
    # ============================================

    def _recuperar_contraseña(self):
        """Abre diálogo de recuperación con frase semilla."""
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("🔑 Recuperar Cuenta")
        dialogo.geometry("480x400")
        dialogo.transient(self)
        dialogo.grab_set()
        
        self._crear_dialogo_recuperacion(dialogo)
        
        dialogo.bind("<Destroy>", lambda e: self.boton_login.configure(state="normal", text="Iniciar Sesión"))

    def _crear_dialogo_recuperacion(self, dialogo):
        """Crea el contenido del diálogo de recuperación."""
        # Título
        ctk.CTkLabel(
            dialogo,
            text="🔑 Recuperar con Frase Semilla",
            font=crear_fuente(16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)
        
        # Email
        ctk.CTkLabel(
            dialogo,
            text="Tu Email:",
            font=crear_fuente(12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(anchor="w", padx=40)
        
        entry_email = ctk.CTkEntry(
            dialogo, placeholder_text="tu@email.com",
            font=crear_fuente(13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=40,
        )
        entry_email.pack(fill="x", padx=40, pady=(5, 15))
        
        # Frase Semilla
        ctk.CTkLabel(
            dialogo,
            text="Tu Frase Semilla (12 palabras):",
            font=crear_fuente(12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(anchor="w", padx=40)
        
        entry_frase = ctk.CTkEntry(
            dialogo, placeholder_text="palabra1 palabra2 palabra3 ...",
            font=crear_fuente(13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=40,
        )
        entry_frase.pack(fill="x", padx=40, pady=(5, 20))
        
        label_error = ctk.CTkLabel(
            dialogo, text="", font=crear_fuente(11),
            text_color=PELIGRO,
        )
        label_error.pack(pady=5)
        
        # Botón entrar
        ctk.CTkButton(
            dialogo,
            text="✓ Entrar",
            font=crear_fuente(14, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=45,
            command=lambda: self._intentar_login_frase(entry_email, entry_frase, label_error, dialogo),
        ).pack(fill="x", padx=40, pady=(10, 5))
        
        # Botón cancelar
        ctk.CTkButton(
            dialogo,
            text="Cancelar",
            font=crear_fuente(12),
            command=dialogo.destroy,
        ).pack(pady=10)

    def _intentar_login_frase(self, entry_email, entry_frase, label_error, dialogo):
        """Intenta login con frase semilla."""
        email = entry_email.get().strip()
        frase = entry_frase.get().strip()
        
        if not email or not frase:
            label_error.configure(text="Completa todos los campos")
            return
        
        try:
            from src.db.conexion import conexion_global
            from src.auth.frase_semilla import verificar_frase_semilla
            
            usuarios = conexion_global.obtener_coleccion('usuarios')
            usuario = usuarios.find_one({'email': email})
            
            if not usuario:
                label_error.configure(text="Email no encontrado")
                return
            
            uid = str(usuario['_id'])
            if not verificar_frase_semilla(uid, frase):
                label_error.configure(text="Frase incorrecta")
                return
            
            # Frase correcta - hacer login
            dialogo.destroy()
            if self._login_con_frase:
                self._login_con_frase(email, usuario)
            else:
                self.on_login(email, "")
                
        except Exception as e:
            label_error.configure(text=f"Error: {str(e)}")

    # ============================================
    # MÉTODOS PÚBLICOS
    # ============================================

    def mostrar_error(self, mensaje):
        """Muestra mensaje de error en pantalla."""
        self.label_error.configure(text=mensaje)
        self.boton_login.configure(state="normal", text="Iniciar Sesión")

    def limpiar(self):
        """Limpia los campos del formulario."""
        self.entry_email.delete(0, "end")
        self.entry_contraseña.delete(0, "end")
        self.label_error.configure(text="")