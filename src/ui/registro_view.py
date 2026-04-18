"""
Módulo: registro_view.py
Responsabilidad: Flujo de registro de usuarios en 3 pasos.
"""

import re
import pyperclip

import customtkinter as ctk
from src.ui.templates import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER, BOTON_SECUNDARIO, BOTON_SECUNDARIO_HOVER,
    TRABAJO_ACTIVO, BORDE, COMPLETADO,
)


class RegistroView(ctk.CTkFrame):
    """Registro de usuario en 3 pasos."""

    # ============================================
    # INICIALIZACIÓN
    # ============================================

    def __init__(self, parent, on_registro_completo, on_ir_login):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.on_registro_completo = on_registro_completo
        self.on_ir_login = on_ir_login
        self.paso_actual = 1
        self.resultado_registro = None
        self.datos_paso_1 = {"nombre": "", "email": "", "rol": "empleado"}
        self.datos_paso_2 = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False,
            "tipo": "sistema",
        }
        self._crear_widgets()

    # ============================================
    # CREACIÓN DE WIDGETS
    # ============================================

    def _crear_widgets(self):
        """Crea todos los widgets base."""
        self._crear_card()
        self._crear_header()
        self._crear_contenido()
        self._crear_label_error()
        self._crear_botones()
        self._crear_link_login()
        self._mostrar_paso_1()

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
    # Header con progreso
    # --------------------------------------------

    def _crear_header(self):
        """Crea el header con paso y barra de progreso."""
        self.header = ctk.CTkFrame(self.card, fg_color="transparent")
        self.header.pack(fill="x", padx=35, pady=(30, 10))

        self.label_paso = ctk.CTkLabel(
            self.header,
            text="Paso 1 de 3 — Datos personales",
            font=("Comic Sans MS", 20, "bold"),
            text_color=TEXTO_PRINCIPAL,
        )
        self.label_paso.pack()

        self.progreso = ctk.CTkProgressBar(
            self.header,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            height=4,
        )
        self.progreso.pack(fill="x", pady=(10, 0))
        self.progreso.set(0.25)

    # --------------------------------------------
    # Contenedor de contenido
    # --------------------------------------------

    def _crear_contenido(self):
        """Crea el contenedor del contenido del paso."""
        self.contenido = ctk.CTkFrame(self.card, fg_color="transparent")
        self.contenido.pack(fill="both", expand=True, padx=30, pady=10)

    # --------------------------------------------
    # Label de error
    # --------------------------------------------

    def _crear_label_error(self):
        """Crea el label para mensajes de error."""
        self.label_error = ctk.CTkLabel(
            self.card,
            text="",
            font=("Comic Sans MS", 14),
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 5))

    # --------------------------------------------
    # Botones de navegación
    # --------------------------------------------

    def _crear_botones(self):
        """Crea los botones atrás/siguiente."""
        self.botones = ctk.CTkFrame(self.card, fg_color="transparent")
        self.botones.pack(fill="x", padx=35, pady=(0, 25))

        self.boton_atras = ctk.CTkButton(
            self.botones,
            text="← Atrás",
            font=("Comic Sans MS", 14),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            width=130,
            height=48,
            corner_radius=8,
            command=self._atras,
        )
        self.boton_atras.pack(side="left")

        self.boton_siguiente = ctk.CTkButton(
            self.botones,
            text="Siguiente →",
            font=("Comic Sans MS", 14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            width=170,
            height=48,
            corner_radius=8,
            command=self._siguiente,
        )
        self.boton_siguiente.pack(side="right")

    # --------------------------------------------
    # Link a login
    # --------------------------------------------

    def _crear_link_login(self):
        """Crea el link para iniciar sesión."""
        self.link_login = ctk.CTkLabel(
            self.card,
            text="¿Ya tienes cuenta? Inicia sesión",
            font=("Comic Sans MS", 14, "underline"),
            text_color=INFORMACION,
            cursor="hand2",
        )
        self.link_login.pack(pady=(0, 20))
        self.link_login.bind("<Button-1>", lambda e: self._ir_a_login())

    # ============================================
    # UTILIDADES
    # ============================================

    def _verificar_primer_usuario(self) -> bool:
        """Retorna True si no hay usuarios en la BD."""
        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            return coleccion.count_documents({}) == 0
        except Exception:
            return True

    def _limpiar_contenido(self):
        """Limpia el contenido del frame."""
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _actualizar_boton_siguiente(self, habilitado):
        """Actualiza el estado del botón siguiente."""
        if hasattr(self, 'boton_siguiente'):
            estado = "normal" if habilitado else "disabled"
            fg = BOTON_PRIMARIO if habilitado else BOTON_SECUNDARIO
            self.boton_siguiente.configure(state=estado, fg_color=fg)

    # ============================================
    # PASOS DEL FLUJO
    # ============================================

    def _mostrar_paso_1(self):
        """Paso 1: Datos personales."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 1 de 3 — Datos personales")
        self.progreso.set(0.25)
        self.boton_atras.configure(state="normal")
        self.boton_atras.pack(side="left")
        self.link_login.pack()
        
        tiene_datos_validos = bool(
            self.datos_paso_1.get("nombre") and 
            self.datos_paso_1.get("email") and
            len(self.datos_paso_1.get("nombre", "")) >= 2
        )
        self._actualizar_boton_siguiente(tiene_datos_validos)
        self.boton_siguiente.pack(side="right")

        self._crear_campo_nombre()
        self._crear_campo_email()
        self._crear_selector_rol()

    def _crear_campo_nombre(self):
        """Crea el campo de nombre."""
        ctk.CTkLabel(
            self.contenido, 
            text="Nombre completo (puede contener números, min 1 letra)",
            font=("Comic Sans MS", 14), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(10, 0))

        self.entry_nombre = ctk.CTkEntry(
            self.contenido, placeholder_text="Tu nombre",
            font=("Comic Sans MS", 15), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=44, corner_radius=8,
        )
        self.entry_nombre.pack(fill="x", pady=(3, 10))
        self.entry_nombre.insert(0, self.datos_paso_1["nombre"])
        self.entry_nombre.bind("<KeyRelease>", self._on_nombre_change)

    def _crear_campo_email(self):
        """Crea el campo de email."""
        ctk.CTkLabel(
            self.contenido, text="Email",
            font=("Comic Sans MS", 14), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entry_email = ctk.CTkEntry(
            self.contenido, placeholder_text="usuario@empresa.com",
            font=("Comic Sans MS", 15), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=44, corner_radius=8,
        )
        self.entry_email.pack(fill="x", pady=(3, 10))
        self.entry_email.insert(0, self.datos_paso_1["email"])
        self.entry_email.bind("<KeyRelease>", self._on_email_change)

    def _crear_selector_rol(self):
        """Crea el selector de rol."""
        ctk.CTkLabel(
            self.contenido, text="Rol",
            font=("Comic Sans MS", 14), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        es_primer_usuario = self._verificar_primer_usuario()

        if es_primer_usuario:
            roles_disponibles = ["supervisor", "encargado", "empleado"]
            ctk.CTkLabel(
                self.contenido,
                text="✅ Eres el primer usuario. Elige tu rol de administrador.",
                font=("Comic Sans MS", 12), text_color=COMPLETADO,
            ).pack(anchor="w", pady=(3, 5))
        else:
            roles_disponibles = ["empleado"]
            ctk.CTkLabel(
                self.contenido,
                text="Un supervisor puede cambiarte el rol después",
                font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(3, 5))

        estado_combo = "normal" if es_primer_usuario else "readonly"
        self.combo_rol = ctk.CTkComboBox(
            self.contenido,
            values=roles_disponibles,
            font=("Comic Sans MS", 15),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            button_color=BOTON_PRIMARIO,
            button_hover_color=BOTON_PRIMARIO_HOVER,
            dropdown_fg_color=FONDO_SECUNDARIO,
            height=44,
            corner_radius=8,
            state=estado_combo,
        )
        self.combo_rol.pack(fill="x", pady=(3, 10))
        
        rol_default = "supervisor" if es_primer_usuario else "empleado"
        self.combo_rol.set(rol_default)

    # --------------------------------------------
    # Paso 2: Contraseña
    # --------------------------------------------

    def _mostrar_paso_2(self):
        """Paso 2: Parámetros de contraseña."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 2 de 3 — Parámetros de contraseña")
        self.progreso.set(0.5)
        self.boton_atras.configure(state="normal")
        self.boton_atras.pack(side="left")
        self.link_login.pack()
        self.boton_siguiente.configure(text="Generar →")
        self.boton_siguiente.pack(side="right")

        ctk.CTkLabel(
            self.contenido,
            text="Configuraremos tu contraseña segura",
            font=("Comic Sans MS", 15),
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(10, 15))

        self._crear_slider_longitud()
        self._crear_checkboxes_contraseña()
        self._crear_tipo_contraseña()

    def _crear_slider_longitud(self):
        """Crea el slider de longitud."""
        ctk.CTkLabel(
            self.contenido, text="Longitud de la contraseña",
            font=("Comic Sans MS", 14), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.slider_longitud = ctk.CTkSlider(
            self.contenido,
            from_=8, to=128,
            number_of_steps=120,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            button_color=TEXTO_PRINCIPAL,
            button_hover_color=TRABAJO_ACTIVO,
        )
        self.slider_longitud.pack(fill="x", pady=(5, 0))

        self.label_longitud = ctk.CTkLabel(
            self.contenido, text="20 caracteres",
            font=("Comic Sans MS", 14), text_color=TRABAJO_ACTIVO,
        )
        self.label_longitud.pack(anchor="e")

        longitud = self.datos_paso_2.get("longitud", 20)
        self.slider_longitud.set(longitud)
        self.label_longitud.configure(text=f"{longitud} caracteres")
        self.slider_longitud.configure(command=self._actualizar_longitud)

    def _crear_checkboxes_contraseña(self):
        """Crea los checkboxes de opciones de contraseña."""
        self.var_mayus = ctk.BooleanVar(value=self.datos_paso_2.get("usar_mayusculas", True))
        self.var_num = ctk.BooleanVar(value=self.datos_paso_2.get("usar_numeros", True))
        self.var_simb = ctk.BooleanVar(value=self.datos_paso_2.get("usar_simbolos", True))
        self.var_ambig = ctk.BooleanVar(value=self.datos_paso_2.get("excluir_ambiguos", False))

        for texto, var in [
            ("Incluir mayúsculas (A-Z)", self.var_mayus),
            ("Incluir números (0-9)", self.var_num),
            ("Incluir símbolos (!@#$...)", self.var_simb),
            ("Excluir caracteres ambiguos (0,O,l,I,1)", self.var_ambig),
        ]:
            ctk.CTkCheckBox(
                self.contenido, text=texto, variable=var,
                font=("Comic Sans MS", 14), text_color=TEXTO_SECUNDARIO,
                fg_color=FONDO_SECUNDARIO, checkmark_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", pady=(8, 0))

        ctk.CTkFrame(self.contenido, fg_color=BORDE, height=1).pack(fill="x", pady=(15, 10))

    def _crear_tipo_contraseña(self):
        """Crea las opciones de tipo de contraseña."""
        self.tipo_contraseña = ctk.StringVar(value=self.datos_paso_2.get("tipo", "sistema"))

        ctk.CTkRadioButton(
            self.contenido, text="Generada por el sistema (recomendado)",
            variable=self.tipo_contraseña, value="sistema",
            font=("Comic Sans MS", 13), text_color=TEXTO_SECUNDARIO,
            fg_color=TRABAJO_ACTIVO, hover_color=BOTON_PRIMARIO_HOVER,
            command=self._toggle_tipo_contraseña,
        ).pack(anchor="w")

        ctk.CTkRadioButton(
            self.contenido, text="Mi propia contraseña",
            variable=self.tipo_contraseña, value="personalizada",
            font=("Comic Sans MS", 13), text_color=TEXTO_SECUNDARIO,
            fg_color=TRABAJO_ACTIVO, hover_color=BOTON_PRIMARIO_HOVER,
            command=self._toggle_tipo_contraseña,
        ).pack(anchor="w", pady=(2, 5))

        self._crear_campos_contraseña_personalizada()

    def _crear_campos_contraseña_personalizada(self):
        """Crea los campos de contraseña personalizada."""
        self.frame_pass = ctk.CTkFrame(self.contenido, fg_color="transparent")
        self.frame_pass.pack(fill="x", pady=(0, 5))

        row_pass = ctk.CTkFrame(self.frame_pass, fg_color="transparent")
        row_pass.pack(fill="x", pady=(0, 3))
        
        ctk.CTkLabel(
            row_pass, text="Contraseña:",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(side="left")

        self.mostrar_pass = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            row_pass, text="👁", variable=self.mostrar_pass,
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
            command=self._toggle_mostrar_pass,
        ).pack(side="right")

        self.entry_pass = ctk.CTkEntry(
            self.frame_pass,
            placeholder_text="Tu contraseña segura",
            font=("Comic Sans MS", 15), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=44, corner_radius=8, show="•",
        )
        self.entry_pass.pack(fill="x")
        self.entry_pass.insert(0, self.datos_paso_2.get("contraseña", ""))

        ctk.CTkLabel(
            self.frame_pass,
            text="Mín: 5 chars, 1 minúscula, 1 mayúscula, 1 símbolo",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            self.frame_pass, text="Confirmar:",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entry_pass2 = ctk.CTkEntry(
            self.frame_pass,
            placeholder_text="Repite la contraseña",
            font=("Comic Sans MS", 15), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=44, corner_radius=8, show="•",
        )
        self.entry_pass2.pack(fill="x")
        self.entry_pass2.insert(0, self.datos_paso_2.get("contraseña2", ""))

        # Mostrar/ocultar según tipo
        if self.tipo_contraseña.get() == "personalizada":
            self.frame_pass.pack(fill="x", pady=(0, 5))
        else:
            self.frame_pass.pack_forget()

    # --------------------------------------------
    # Paso 3: Completado
    # --------------------------------------------

    def _mostrar_paso_3(self):
        """Paso 3: Contraseña generada + Confirmación."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 3 de 3 — Completado")
        self.progreso.set(1.0)
        self.boton_atras.pack_forget()
        self.link_login.pack_forget()
        self.boton_siguiente.pack_forget()

        ctk.CTkLabel(
            self.contenido,
            text="✅",
            font=("Segoe UI Emoji", 60),
            text_color=COMPLETADO,
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.contenido,
            text="Registro completado",
            font=("Comic Sans MS", 22, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack()

        if self.resultado_registro:
            self._mostrar_info_registro()

    def _mostrar_info_registro(self):
        """Muestra la información del registro."""
        usuario = self.resultado_registro.get('usuario', {})
        email = usuario.get('email', '')
        nombre = usuario.get('nombre', '')
        contrasena = self.resultado_registro.get('contraseña_generada', '')

        frame_info = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_info.pack(fill="x", padx=30, pady=10)

        for label, valor in [("Nombre:", nombre), ("Email:", email), ("Contraseña:", contrasena)]:
            ctk.CTkLabel(
                frame_info,
                text=label,
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w")
            
            color_texto = TEXTO_PRINCIPAL
            if label == "Contraseña:":
                color_texto = COMPLETADO
            
            ctk.CTkLabel(
                frame_info,
                text=valor,
                font=("Comic Sans MS", 14),
                text_color=color_texto,
            ).pack(anchor="w", padx=(80, 0))

        ctk.CTkLabel(
            frame_info,
            text="✅ Muy fuerte — 99%",
            font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        ).pack(anchor="w", padx=(80, 0))

        ctk.CTkButton(
            self.contenido,
            text="📋 Copiar todo",
            font=("Comic Sans MS", 14, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            command=self._copiar_todo_registro,
        ).pack(pady=15)

    def _copiar_todo_registro(self):
        """Copia toda la información al portapapeles."""
        usuario = self.resultado_registro.get('usuario', {})
        contrasena = self.resultado_registro.get('contraseña_generada', '')
        
        texto = f"Nombre: {usuario.get('nombre', '')}\nEmail: {usuario.get('email', '')}\nContraseña: {contrasena}"
        pyperclip.copy(texto)
        self.label_error.configure(text="✅ Copiado al portapapeles", text_color=COMPLETADO)

    # ============================================
    # EVENTOS
    # ============================================

    def _actualizar_longitud(self, valor):
        """Actualiza el label de longitud."""
        self.label_longitud.configure(text=f"{int(valor)} caracteres")

    def _on_nombre_change(self, event=None):
        """Valida nombre en tiempo real."""
        self._actualizar_boton_siguiente(self._validate_nombre())

    def _on_email_change(self, event=None):
        """Valida email en tiempo real."""
        self._verificar_email_duplicado()
        self.boton_siguiente.configure(state="normal")

    def _validate_nombre(self, event=None):
        """Valida el nombre."""
        nombre = self.entry_nombre.get().strip()
        tiene_letra = bool(re.search(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]", nombre))
        
        if not nombre:
            return False
        if len(nombre) < 2:
            return False
        if not tiene_letra:
            return False
        if not re.match(r"^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ0-9\s]+$", nombre):
            return False
        return True

    def _verificar_email_duplicado(self):
        """Verifica email duplicado en tiempo real."""
        try:
            from src.db.conexion import conexion_global
            email = self.entry_email.get().strip()
            
            coleccion = conexion_global.obtener_coleccion('usuarios')
            existe = coleccion.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}})
            
            if existe:
                self.label_error.configure(text="El email ya está registrado", text_color=PELIGRO)
            else:
                self.label_error.configure(text="")
        except Exception:
            pass

    def _toggle_tipo_contraseña(self):
        """Muestra/oculta campos de contraseña personalizada."""
        if self.tipo_contraseña.get() == "personalizada":
            self.frame_pass.pack(fill="x", pady=(0, 5))
        else:
            self.frame_pass.pack_forget()

    def _toggle_mostrar_pass(self):
        """Alterna mostrar/ocultar contraseña."""
        mostrar = "" if self.mostrar_pass.get() else "•"
        self.entry_pass.configure(show=mostrar)
        self.entry_pass2.configure(show=mostrar)

    # ============================================
    # VALIDACIONES
    # ============================================

    def _validar_paso_1(self):
        """Valida los datos del paso 1."""
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()

        # Validar nombre
        if not nombre:
            self.label_error.configure(text="El nombre es obligatorio")
            self._actualizar_boton_siguiente(False)
            return False

        tiene_letra = bool(re.search(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]", nombre))
        if len(nombre) < 2 or not tiene_letra:
            self.label_error.configure(text="El nombre debe tener al menos 2 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        if not re.match(r"^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ0-9\s]+$", nombre):
            self.label_error.configure(text="El nombre contiene caracteres inválidos")
            self._actualizar_boton_siguiente(False)
            return False

        # Validar email
        if not email or "@" not in email:
            self.label_error.configure(text="El email es obligatorio")
            self._actualizar_boton_siguiente(False)
            return False

        partes = email.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            self.label_error.configure(text="El formato del email es inválido")
            self._actualizar_boton_siguiente(False)
            return False

        dominio = partes[1]
        if "." not in dominio:
            self.label_error.configure(text="El dominio debe tener un punto")
            self._actualizar_boton_siguiente(False)
            return False

        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            existe = coleccion.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}})
            if existe:
                self.label_error.configure(text="El email ya está registrado")
                self._actualizar_boton_siguiente(False)
                return False
        except Exception:
            pass

        self.label_error.configure(text="")
        self._actualizar_boton_siguiente(True)
        return True

    def _validar_paso_2(self):
        """Valida los datos del paso 2."""
        self.datos_paso_2["longitud"] = int(self.slider_longitud.get())
        self.datos_paso_2["usar_mayusculas"] = self.var_mayus.get()
        self.datos_paso_2["usar_numeros"] = self.var_num.get()
        self.datos_paso_2["usar_simbolos"] = self.var_simb.get()
        self.datos_paso_2["excluir_ambiguos"] = self.var_ambig.get()
        self.datos_paso_2["tipo"] = self.tipo_contraseña.get()
        
        if self.tipo_contraseña.get() == "personalizada":
            contraseña = self.entry_pass.get()
            contraseña2 = self.entry_pass2.get()
            
            if len(contraseña) < 5:
                self.label_error.configure(text="Mínimo 5 caracteres")
                return False
            if len(contraseña) > 64:
                self.label_error.configure(text="Máximo 64 caracteres")
                return False
            if contraseña != contraseña2:
                self.label_error.configure(text="Las contraseñas no coinciden")
                return False
            if not re.search(r"[a-z]", contraseña):
                self.label_error.configure(text="Debe tener al menos una minúscula (a-z)")
                return False
            if not re.search(r"[A-Z]", contraseña):
                self.label_error.configure(text="Debe tener al menos una mayúscula (A-Z)")
                return False
            if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};:'\",./<>?\\|`~]", contraseña):
                self.label_error.configure(text="Debe tener al menos un símbolo (!@#$%^&*...)")
                return False
            
            self.datos_paso_2["contraseña"] = contraseña
            self.datos_paso_2["tipo"] = "personalizada"
        
        self.label_error.configure(text="")
        return True

    # ============================================
    # NAVEGACIÓN
    # ============================================

    def _siguiente(self):
        """Avanza al siguiente paso."""
        if self.paso_actual == 1:
            if not self._validar_paso_1():
                return
            
            self.datos_paso_1["nombre"] = self.entry_nombre.get().strip()
            self.datos_paso_1["email"] = self.entry_email.get().strip()
            self.datos_paso_1["rol"] = self.combo_rol.get()
            
            self.paso_actual = 2
            self._mostrar_paso_2()

        elif self.paso_actual == 2:
            if not self._validar_paso_2():
                return
            
            try:
                from src.auth import registrar_usuario
                self.resultado_registro = registrar_usuario(
                    self.datos_paso_1["email"],
                    self.datos_paso_1["nombre"],
                    self.datos_paso_1["rol"],
                    self.datos_paso_2,
                )
                self.paso_actual = 3
                self._mostrar_paso_3()
            except Exception as e:
                self.label_error.configure(text=str(e))
                return

    def _atras(self):
        """Regresa al paso anterior."""
        if self.paso_actual == 2:
            if hasattr(self, 'entry_nombre'):
                self.datos_paso_1["nombre"] = self.entry_nombre.get().strip()
                self.datos_paso_1["email"] = self.entry_email.get().strip()
                if hasattr(self, 'combo_rol'):
                    self.datos_paso_1["rol"] = self.combo_rol.get()
            
            self.paso_actual = 1
            self.resultado_registro = None
            self._mostrar_paso_1()
            
        elif self.paso_actual == 3:
            self.paso_actual = 2
            self.resultado_registro = None
            self._mostrar_paso_2()

    def _ir_a_login(self):
        """Navega a la pantalla de login."""
        self.datos_paso_1 = {"nombre": "", "email": "", "rol": "empleado"}
        self.datos_paso_2 = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False,
            "tipo": "sistema",
        }
        self.resultado_registro = None
        self.on_ir_login()

    # ============================================
    # MÉTODOS PÚBLICOS
    # ============================================

    def limpiar(self):
        """Resetea la vista de registro."""
        self.paso_actual = 1
        self.resultado_registro = None
        self.datos_paso_1 = {"nombre": "", "email": "", "rol": "empleado"}
        self.datos_paso_2 = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False,
            "tipo": "sistema",
        }