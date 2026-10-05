"""
Módulo: login_view.py
Responsabilidad: Pantalla de login con email y contraseña.
"""

import importlib
import customtkinter as ctk
from src.ui.templates.theme import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER, BOTON_SECUNDARIO,
    BOTON_SECUNDARIO_HOVER,
    COMPLETADO,
    crear_fuente, NORMAL_NEGRITA, PEQUENO, MINIMO
)
from src.ui.templates.fuentes import crear_fuente_emoji

# Texto del botón principal de login
_TXT_INICIAR_SESION = "Iniciar Sesión"


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
            font=crear_fuente_emoji(56),
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
            text=_TXT_INICIAR_SESION,
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
            font=NORMAL_NEGRITA,
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            corner_radius=8,
            command=self._recuperar_contraseña,
        ).pack(fill="x", pady=(0, 10))

        # Botón Verificar Email
        ctk.CTkButton(
            footer,
            text="¿No recibiste el código? Verifica tu email",
            font=NORMAL_NEGRITA,
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=INFORMACION,
            height=45,
            corner_radius=8,
            command=self._reenviar_codigo_verificacion,
        ).pack(fill="x")

    # --------------------------------------------
    # Footer versión
    # --------------------------------------------

    def _crear_footer(self):
        """Crea el pie de página."""
        frame_tema = ctk.CTkFrame(self, fg_color="transparent")
        frame_tema.place(relx=0.5, rely=0.92, anchor="center")

        from dotenv import load_dotenv
        load_dotenv()
        import os
        self.tema_actual = os.getenv("TEMA", "dark")
        self.btn_tema = ctk.CTkButton(
            frame_tema,
            text="☀️" if self.tema_actual == "light" else "🌙",
            font=PEQUENO,
            fg_color="transparent",
            hover_color=FONDO_SECUNDARIO,
            text_color=TEXTO_SECUNDARIO,
            width=40,
            height=30,
            command=self._cambiar_tema,
        )
        self.btn_tema.pack()

        ctk.CTkLabel(
            self,
            text="v1.0.0 — Dicampus",
            font=MINIMO,
            text_color=TEXTO_SECUNDARIO,
        ).place(relx=0.5, rely=0.97, anchor="center")

    def _cambiar_tema(self):
        """Cambia el tema y reinicia la app."""
        import customtkinter as ctk
        import sys
        import os
        import subprocess
        import time

        # Alternar tema
        nuevo_tema = "light" if self.tema_actual == "dark" else "dark"

        # Guardar en .env
        from dotenv import set_key, load_dotenv
        set_key(".env", "TEMA", nuevo_tema)

        # Forzar reload del .env en este proceso
        load_dotenv(override=True)
        os.environ["TEMA"] = nuevo_tema

        # Actualizar CustomTkinter
        ctk.set_appearance_mode(nuevo_tema)

        # Pequeño delay para asegurar que .env se guardó
        time.sleep(0.2)

        # Cerrar esta ventana
        self.master.destroy()

        # Iniciar nuevo proceso
        python = sys.executable
        args = [python, "main.py"]
        subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, cwd=os.getcwd())
        sys.exit(0)

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
        contrasena = self.entry_contraseña.get()

        # Validaciones
        if not email:
            self._mostrar_error("El email es obligatorio")
            return

        if not contrasena:
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
            self.on_login(email, contrasena)
        except Exception as e:
            self._mostrar_error(str(e))

    def _mostrar_error(self, mensaje):
        """Muestra mensaje de error y resetea botón."""
        self.label_error.configure(text=mensaje)
        self.boton_login.configure(state="normal", text=_TXT_INICIAR_SESION)

    # ============================================
    # REENVÍO DE CÓDIGO DE VERIFICACIÓN
    # ============================================

    def _reenviar_codigo_verificacion(self):
        """Abre diálogo para reenviar código de verificación."""
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("📧 Reenviar Código")
        dialogo.geometry("480x350")
        dialogo.transient(self)
        dialogo.grab_set()

        self._crear_dialogo_verificacion(dialogo)

        dialogo.bind("<Destroy>", lambda e: self.boton_login.configure(state="normal", text=_TXT_INICIAR_SESION))

    @staticmethod
    def _enviar_codigo(email, entry_codigo, frame_codigo, btn_enviar,
                       comando_verificar, label_error):
        """Genera y envía el código de verificación, mostrando el campo para introducirlo."""
        from src.auth.verificacion_email import (
            crear_o_actualizar_verificacion,
            enviar_token_por_email,
        )

        token = crear_o_actualizar_verificacion(email.lower())
        enviar_token_por_email(email.lower(), token)

        label_error.configure(
            text="📧 Código enviado. Revisa tu email/consola.", text_color=COMPLETADO
        )
        entry_codigo.delete(0, "end")
        frame_codigo.pack(fill="x", padx=30, pady=(10, 15))
        entry_codigo.focus()
        btn_enviar.configure(text="✓ Verificar Código", command=comando_verificar)

    @staticmethod
    def _crear_fila_resumen(frame_info, etiqueta, valor):
        """Crea una fila etiqueta/valor del resumen tras verificar el email."""
        fila = ctk.CTkFrame(frame_info, fg_color="transparent")
        fila.pack(anchor="w", pady=4)
        ctk.CTkLabel(
            fila, text=f"{etiqueta}: ", font=NORMAL_NEGRITA,
            text_color=TEXTO_SECUNDARIO,
        ).pack(side="left")
        ctk.CTkLabel(
            fila, text=valor, font=crear_fuente(14), text_color=COMPLETADO,
        ).pack(side="left")

    @classmethod
    def _crear_panel_datos_verificados(cls, dialogo, usuario, contrasena_real):
        """Muestra los datos del usuario recién verificado con opción de copiarlos."""
        frame_info = ctk.CTkFrame(dialogo, fg_color="transparent")
        frame_info.pack(fill="x", padx=30, pady=15)

        cls._crear_fila_resumen(frame_info, "Nombre", usuario.get('nombre', ''))
        cls._crear_fila_resumen(frame_info, "Email", usuario.get('email', ''))
        cls._crear_fila_resumen(frame_info, "Rol", usuario.get('rol', 'empleado'))
        cls._crear_fila_resumen(frame_info, "Contraseña", contrasena_real)

        label_copiar = ctk.CTkLabel(dialogo, text="", font=crear_fuente(12))
        label_copiar.pack()

        def copiar():
            import pyperclip
            texto = (
                f"Nombre: {usuario.get('nombre', '')}\n"
                f"Email: {usuario.get('email', '')}\n"
                f"Contraseña: {contrasena_real}\n"
                f"Rol: {usuario.get('rol', 'empleado')}"
            )
            pyperclip.copy(texto)
            label_copiar.configure(text="✅ Copiado", text_color=COMPLETADO)

        ctk.CTkButton(
            dialogo,
            text="📋 Copiar todo",
            font=crear_fuente(14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            command=copiar,
        ).pack(fill="x", padx=30, pady=(10, 15))

    @classmethod
    def _cargar_datos_verificados(cls, dialogo, email):
        """Busca el usuario y monta el resumen; si falla, se omite sin romper el diálogo."""
        from src.db.conexion import conexion_global
        from src.seguridad.encriptacion import descifrar

        usuarios = conexion_global.obtener_coleccion('usuarios')
        usuario = usuarios.find_one({'email': email.lower()})

        if not usuario:
            return

        contrasena_real = descifrar(usuario.get('contraseña_encriptada', ''))
        cls._crear_panel_datos_verificados(dialogo, usuario, contrasena_real)

    @classmethod
    def _mostrar_resumen_verificacion(cls, dialogo, email):
        """Muestra la pantalla de éxito e intenta cargar los datos del usuario."""
        ctk.CTkLabel(
            dialogo,
            text="✅",
            font=crear_fuente_emoji(50),
            text_color=COMPLETADO,
        ).pack(pady=20)

        ctk.CTkLabel(
            dialogo,
            text="Email verificado",
            font=crear_fuente(18, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 10))

        try:
            cls._cargar_datos_verificados(dialogo, email)
        except Exception:  # nosec - el resumen es opcional
            pass

    @staticmethod
    def _crear_widgets_verificacion(dialogo):
        """Construye los widgets del diálogo y devuelve los que se necesitan después."""
        entry_email = ctk.CTkEntry(
            dialogo,
            placeholder_text="tu@email.com",
            font=crear_fuente(14),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            height=44,
        )
        entry_email.pack(fill="x", padx=30, pady=(5, 15))

        label_error = ctk.CTkLabel(
            dialogo,
            text="",
            font=crear_fuente(12),
            text_color=PELIGRO,
        )
        label_error.pack(pady=(0, 10))

        frame_codigo = ctk.CTkFrame(dialogo, fg_color="transparent")
        frame_codigo.pack(fill="x", padx=30, pady=(10, 15))
        frame_codigo.pack_forget()

        entry_codigo = ctk.CTkEntry(
            frame_codigo,
            placeholder_text="123456",
            font=crear_fuente(20),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            height=44,
            justify="center",
        )
        entry_codigo.pack(fill="x")

        ctk.CTkLabel(
            dialogo,
            text="",
            font=crear_fuente(14, "bold"),
            text_color=COMPLETADO,
        ).pack(pady=(0, 10))

        btn_enviar = ctk.CTkButton(
            dialogo,
            text="📧 Enviar Código",
            font=crear_fuente(14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=44,
        )
        btn_enviar.pack(fill="x", padx=30, pady=(10, 15))

        return entry_email, label_error, frame_codigo, entry_codigo, btn_enviar

    @staticmethod
    def _crear_boton_ir_a_login(dialogo):
        """Botón de cierre del diálogo una vez verificado el email."""
        ctk.CTkButton(
            dialogo,
            text="Ir a Login",
            font=crear_fuente(14),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            command=dialogo.destroy,
        ).pack(fill="x", padx=30, pady=20)

    def _validar_codigo_dialogo(self, dialogo, widgets):
        """Comprueba el código introducido y, si es válido, muestra el resumen."""
        entry_email, label_error, _, entry_codigo, _ = widgets
        email = entry_email.get().strip()
        codigo = entry_codigo.get().strip()

        if not email or not codigo:
            label_error.configure(text="Completa todos los campos")
            return

        try:
            from src.auth.verificacion_email import verificar_token_db

            resultado = verificar_token_db(email.lower(), codigo)

            if not resultado['valido']:
                label_error.configure(text=resultado['mensaje'])
                return

            for widget in dialogo.winfo_children():
                widget.destroy()

            self._mostrar_resumen_verificacion(dialogo, email)
            self._crear_boton_ir_a_login(dialogo)

        except Exception as e:
            label_error.configure(text=f"Error: {str(e)}")

    def _enviar_codigo_dialogo(self, dialogo, widgets):
        """Valida el email del diálogo y solicita el envío del código de verificación."""
        entry_email, label_error, frame_codigo, entry_codigo, btn_enviar = widgets
        email = entry_email.get().strip()

        if not email:
            label_error.configure(text="El email es obligatorio")
            return

        try:
            usuario = self._buscar_usuario_por_email(email)

            if not usuario:
                label_error.configure(text="Email no registrado")
                return

            if usuario.get('email_verificado', False):
                label_error.configure(text="✅ Este email ya está verificado. Ve a Login.", text_color=COMPLETADO)
                return

            self._enviar_codigo(
                email, entry_codigo, frame_codigo, btn_enviar,
                lambda: self._validar_codigo_dialogo(dialogo, widgets), label_error,
            )
        except Exception as e:
            label_error.configure(text=f"Error: {str(e)}")

    @staticmethod
    def _buscar_usuario_por_email(email):
        """Busca un usuario por email sin distinguir mayúsculas."""
        from src.db.conexion import conexion_global

        usuarios = conexion_global.obtener_coleccion('usuarios')
        return usuarios.find_one(
            {'email': {'$regex': f'^{email.lower()}$', '$options': 'i'}}
        )

    def _crear_dialogo_verificacion(self, dialogo):
        """Crea el contenido del diálogo de verificación."""
        dialogo.geometry("480x420")

        ctk.CTkLabel(
            dialogo,
            text="📧 Verificar tu Email",
            font=crear_fuente(16, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)

        ctk.CTkLabel(
            dialogo,
            text="Tu Email:",
            font=crear_fuente(12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(fill="x", padx=30)

        widgets = self._crear_widgets_verificacion(dialogo)
        _, _, _, entry_codigo, btn_enviar = widgets

        btn_enviar.configure(
            command=lambda: self._enviar_codigo_dialogo(dialogo, widgets)
        )
        entry_codigo.bind(
            "<Return>",
            lambda _e: self._validar_codigo_dialogo(dialogo, widgets),
        )

        ctk.CTkButton(
            dialogo,
            text="Cancelar",
            font=crear_fuente(12),
            fg_color="transparent",
            text_color=TEXTO_SECUNDARIO,
            height=35,
            command=dialogo.destroy,
        ).pack(pady=(0, 20))

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
        
        dialogo.bind("<Destroy>", lambda e: self.boton_login.configure(state="normal", text=_TXT_INICIAR_SESION))

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
        self.boton_login.configure(state="normal", text=_TXT_INICIAR_SESION)

    def limpiar(self):
        """Limpia los campos del formulario."""
        self.entry_email.delete(0, "end")
        self.entry_contraseña.delete(0, "end")
        self.label_error.configure(text="")