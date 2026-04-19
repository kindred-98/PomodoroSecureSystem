"""
Módulo: verificar_email_view.py
Responsabilidad: Pantalla de verificación de email con token.
"""

import customtkinter as ctk
from src.ui.templates import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER, BOTON_SECUNDARIO, BOTON_SECUNDARIO_HOVER,
    TRABAJO_ACTIVO, COMPLETADO,
    crear_fuente, NORMAL, NORMAL_NEGRITA, PEQUENO, MINIMO
)


class VerificarEmailView(ctk.CTkFrame):
    """Pantalla para verificar email con token."""

    def __init__(self, parent, email, on_verificado, on_volver):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.email = email
        self.on_verificado = on_verificado
        self.on_volver = on_volver
        self.segundos_cooldown = 60
        self._crear_widgets()
        self._enviar_token()

    def _crear_widgets(self):
        """Crea los widgets de la interfaz."""
        # Card central
        self.card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=500,
            height=450,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            self.card,
            text="📧 Verifica tu Email",
            font=crear_fuente(24, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack(pady=(30, 10))

        # Email
        ctk.CTkLabel(
            self.card,
            text=f"Enviamos un código a:",
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
        ).pack()
        
        ctk.CTkLabel(
            self.card,
            text=self.email,
            font=NORMAL_NEGRITA,
            text_color=INFORMACION,
        ).pack(pady=(0, 20))

        # Campo token
        ctk.CTkLabel(
            self.card,
            text="Código de verificación:",
            font=PEQUENO,
            text_color=TEXTO_SECUNDARIO,
            anchor="w",
        ).pack(anchor="w", padx=40)

        self.entry_token = ctk.CTkEntry(
            self.card,
            placeholder_text="123456",
            font=crear_fuente(20),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            placeholder_text_color=TEXTO_SECUNDARIO,
            height=50,
            corner_radius=8,
            justify="center",
        )
        self.entry_token.pack(fill="x", padx=40, pady=(5, 15))
        self.entry_token.bind("<Return>", lambda e: self._on_verificar_click())

        # Label de estado/error
        self.label_estado = ctk.CTkLabel(
            self.card,
            text="",
            font=PEQUENO,
            text_color=PELIGRO,
            wraplength=350,
        )
        self.label_estado.pack(pady=(0, 10))

        # Botón verificar
        self.btn_verificar = ctk.CTkButton(
            self.card,
            text="✓ Verificar",
            font=NORMAL_NEGRITA,
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=48,
            corner_radius=8,
            command=self._on_verificar_click,
        )
        self.btn_verificar.pack(fill="x", padx=40, pady=(0, 10))

        # Botón reenviar
        self.btn_reenviar = ctk.CTkButton(
            self.card,
            text="Reenviar código",
            font=NORMAL,
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=40,
            corner_radius=8,
            command=self._on_reenviar_click,
            state="disabled",
        )
        self.btn_reenviar.pack(fill="x", padx=40, pady=(0, 10))

        # Botón volver
        ctk.CTkButton(
            self.card,
            text="← Volver al login",
            font=PEQUENO,
            fg_color="transparent",
            hover_color=FONDO_SECUNDARIO,
            text_color=TEXTO_SECUNDARIO,
            height=35,
            command=self.on_volver,
        ).pack(pady=(10, 20))

    def _enviar_token(self):
        """Envía el token al email del usuario."""
        try:
            from src.auth.verificacion_email import (
                crear_o_actualizar_verificacion,
                enviar_token_por_email
            )
            
            # Crear token
            token = crear_o_actualizar_verificacion(self.email)
            
            # Enviar por email
            result = enviar_token_por_email(self.email, token)
            
            self.label_estado.configure(
                text="✓ Código enviado. Revisa tu email o consola.",
                text_color=COMPLETADO
            )
            
            # Iniciar contador
            self._iniciar_contador()
            
        except Exception as e:
            self.label_estado.configure(
                text=f"Error al enviar código: {str(e)}",
                text_color=PELIGRO
            )

    def _on_verificar_click(self):
        """Procesa la verificación del token."""
        token = self.entry_token.get().strip()
        
        if not token:
            self.label_estado.configure(
                text="Introduce el código de verificación",
                text_color=PELIGRO
            )
            return
        
        if len(token) != 6 or not token.isdigit():
            self.label_estado.configure(
                text="El código debe tener 6 dígitos",
                text_color=PELIGRO
            )
            return
        
        self.btn_verificar.configure(state="disabled", text="Verificando...")
        
        try:
            from src.auth.verificacion_email import verificar_token_db
            
            resultado = verificar_token_db(self.email, token)
            
            if resultado['valido']:
                self.label_estado.configure(
                    text="✓ Email verificado correctamente",
                    text_color=COMPLETADO
                )
                self.after(1500, self.on_verificado)
            else:
                self.label_estado.configure(
                    text=resultado['mensaje'],
                    text_color=PELIGRO
                )
                self.btn_verificar.configure(state="normal", text="✓ Verificar")
                self.entry_token.delete(0, "end")
                
        except Exception as e:
            self.label_estado.configure(
                text=f"Error: {str(e)}",
                text_color=PELIGRO
            )
            self.btn_verificar.configure(state="normal", text="✓ Verificar")

    def _on_reenviar_click(self):
        """Reenvía el token."""
        self._enviar_token()

    def _iniciar_contador(self):
        """Inicia el contador para reenviar código."""
        self.segundos_cooldown = 60
        self.btn_reenviar.configure(state="disabled")
        
        def tick():
            if self.segundos_cooldown > 0:
                self.btn_reenviar.configure(
                    text=f"Reenviar código ({self.segundos_cooldown}s)"
                )
                self.segundos_cooldown -= 1
                self.after(1000, tick)
            else:
                self.btn_reenviar.configure(
                    text="Reenviar código",
                    state="normal"
                )
        
        tick()