"""
Módulo: registro_resultado_view.py
Responsabilidad: Pantalla de resultado del registro (Paso 3).
"""

import customtkinter as ctk
import pyperclip
from src.ui.templates import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER, BOTON_SECUNDARIO, BOTON_SECUNDARIO_HOVER,
    TRABAJO_ACTIVO, COMPLETADO,
    crear_fuente, NORMAL, NORMAL_NEGRITA, PEQUENO, MINIMO
)
from src.ui.templates.fuentes import crear_fuente_emoji


class RegistroResultadoView(ctk.CTkFrame):
    """Pantalla de resultado del registro."""

    def __init__(self, parent, email, on_login):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.email = email
        self.on_login = on_login
        self.usuario = None
        self.contrasena = None
        self._cargar_datos()
        self._crear_widgets()

    def _cargar_datos(self):
        """Carga los datos del usuario desde BD."""
        from src.db.conexion import conexion_global
        from src.seguridad.encriptacion import descifrar

        coleccion = conexion_global.obtener_coleccion('usuarios')
        self.usuario = coleccion.find_one({'email': self.email.lower()})

        if self.usuario:
            self.contrasena = descifrar(self.usuario.get('contraseña_encriptada', ''))
        else:
            self.contrasena = "••••••••••••"

    def _crear_widgets(self):
        """Crea los widgets."""
        self.card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=500,
            height=500,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        ctk.CTkLabel(
            self.card,
            text="✅",
            font=crear_fuente_emoji(60),
            text_color=COMPLETADO,
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self.card,
            text="Registro completado",
            font=crear_fuente(24, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(0, 20))

        if self.usuario:
            frame_info = ctk.CTkFrame(self.card, fg_color="transparent")
            frame_info.pack(fill="x", padx=30, pady=10)

            def fila(label_texto, valor):
                fila = ctk.CTkFrame(frame_info, fg_color="transparent")
                fila.pack(anchor="w", pady=4)

                ctk.CTkLabel(
                    fila,
                    text=f"{label_texto}: ",
                    font=NORMAL_NEGRITA,
                    text_color=TEXTO_SECUNDARIO,
                ).pack(side="left")

                ctk.CTkLabel(
                    fila,
                    text=valor,
                    font=NORMAL,
                    text_color=COMPLETADO,
                ).pack(side="left")

            nombre = self.usuario.get('nombre', '')
            email = self.usuario.get('email', '')
            rol = self.usuario.get('rol', 'empleado')

            fila("Nombre", nombre)
            fila("Email", email)
            fila("Rol", rol)

            if self.contrasena:
                frame_pass = ctk.CTkFrame(self.card, fg_color="transparent")
                frame_pass.pack(fill="x", padx=30, pady=(15, 10))

                ctk.CTkLabel(
                    frame_pass,
                    text="Contraseña: ",
                    font=NORMAL_NEGRITA,
                    text_color=TEXTO_SECUNDARIO,
                ).pack(side="left")

                ctk.CTkLabel(
                    frame_pass,
                    text=self.contrasena,
                    font=NORMAL,
                    text_color=COMPLETADO,
                ).pack(side="left")

            ctk.CTkButton(
                self.card,
                text="📋 Copiar todo",
                font=NORMAL_NEGRITA,
                fg_color=BOTON_PRIMARIO,
                hover_color=BOTON_PRIMARIO_HOVER,
                text_color=TEXTO_PRINCIPAL,
                height=45,
                command=self._copiar_todo,
            ).pack(pady=20)

        ctk.CTkButton(
            self.card,
            text="Ir a Login",
            font=NORMAL,
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=40,
            command=self._ir_a_login,
        ).pack(pady=(0, 20))

    def _copiar_todo(self):
        """Copia toda la información."""
        if self.usuario and self.contrasena:
            texto = f"Nombre: {self.usuario.get('nombre', '')}\nEmail: {self.usuario.get('email', '')}\nContraseña: {self.contrasena}\nRol: {self.usuario.get('rol', 'empleado')}"
            pyperclip.copy(texto)

    def _ir_a_login(self):
        """Va a la pantalla de login."""
        self.on_login()