"""
Módulo: registro_view.py
Responsabilidad: Flujo de registro de 4 pasos.
"""

import customtkinter as ctk
from src.config.colores import *


class RegistroView(ctk.CTkFrame):
    """Registro de usuario en 4 pasos."""

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
            "semilla": ""
        }
        self._crear_widgets()

    def _crear_widgets(self):
        # Card central
        self.card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=660,
            height=760,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Header con pasos
        self.header = ctk.CTkFrame(self.card, fg_color="transparent")
        self.header.pack(fill="x", padx=35, pady=(30, 10))

        self.label_paso = ctk.CTkLabel(
            self.header,
            text="Paso 1 de 3 — Datos personales",
            font=("Comic Sans MS", 20, "bold"),
            text_color=TEXTO_PRINCIPAL,
        )
        self.label_paso.pack()

        # Indicador de progreso
        self.progreso = ctk.CTkProgressBar(
            self.header,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TRABAJO_ACTIVO,
            height=4,
        )
        self.progreso.pack(fill="x", pady=(10, 0))
        self.progreso.set(0.25)

        # Contenedor del paso
        self.contenido = ctk.CTkFrame(self.card, fg_color="transparent")
        self.contenido.pack(fill="both", expand=True, padx=30, pady=10)

        # Label de error
        self.label_error = ctk.CTkLabel(
            self.card,
            text="",
            font=("Comic Sans MS", 14),
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 5))

        # Botonera inferior
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

        # Link login
        self.link_login = ctk.CTkLabel(
            self.card,
            text="¿Ya tienes cuenta? Inicia sesión",
            font=("Comic Sans MS", 14, "underline"),
            text_color=INFORMACION,
            cursor="hand2",
        )
        self.link_login.pack(pady=(0, 20))
        self.link_login.bind("<Button-1>", lambda e: self._ir_a_login())

        self._mostrar_paso_1()

    def _verificar_primer_usuario(self) -> bool:
        """Retorna True si no hay usuarios en la BD (primer registro)."""
        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            return coleccion.count_documents({}) == 0
        except Exception:
            return True

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

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
        
        if tiene_datos_validos:
            self.boton_siguiente.configure(text="Siguiente →", state="normal", fg_color=BOTON_PRIMARIO)
        else:
            self.boton_siguiente.configure(text="Siguiente →", state="disabled", fg_color=BOTON_SECUNDARIO)
        self.boton_siguiente.pack(side="right")

        ctk.CTkLabel(
            self.contenido, text="Nombre completo (puede contener números, min 1 letra)",
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

        if self.tipo_contraseña.get() == "personalizada":
            self.frame_semilla.pack(fill="x", pady=(0, 5))
        else:
            self.frame_semilla.pack_forget()

        self.label_preview = ctk.CTkLabel(
            self.contenido,
            text="Fortaleza estimada: calculando...",
            font=("Comic Sans MS", 13),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_preview.pack(anchor="w", pady=(15, 0))

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
            usuario = self.resultado_registro.get('usuario', {})
            email = usuario.get('email', '')
            nombre = usuario.get('nombre', '')
            rol = usuario.get('rol', '')
            contrasena = self.resultado_registro.get('contraseña_generada', '')

            frame_info = ctk.CTkFrame(self.contenido, fg_color="transparent")
            frame_info.pack(fill="x", padx=30, pady=10)

            ctk.CTkLabel(
                frame_info,
                text="Nombre: ",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                frame_info,
                text=nombre,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", padx=(80, 0))

            ctk.CTkLabel(
                frame_info,
                text="Email: ",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(8, 0))
            
            ctk.CTkLabel(
                frame_info,
                text=email,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", padx=(80, 0))

            ctk.CTkLabel(
                frame_info,
                text="Contraseña: ",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(8, 0))
            
            ctk.CTkLabel(
                frame_info,
                text=contrasena,
                font=("Comic Sans MS", 16, "bold"),
                text_color=COMPLETADO,
            ).pack(anchor="w", padx=(80, 0))

            ctk.CTkLabel(
                frame_info,
                text="✅ Muy fuerte — 99%",
                font=("Comic Sans MS", 12),
                text_color=COMPLETADO,
            ).pack(anchor="w", padx=(80, 0))

            ctk.CTkLabel(
                frame_info,
                text="Rol: ",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(8, 0))
            
            ctk.CTkLabel(
                frame_info,
                text=rol,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", padx=(80, 0))

        btn_frame = ctk.CTkFrame(self.contenido, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame,
            text="📋 Copiar Todo",
            font=("Comic Sans MS", 14),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=45,
            corner_radius=8,
            command=lambda: self._copiar_todo_registro(),
        ).pack(pady=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Ir al Login →",
            font=("Comic Sans MS", 16, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=52,
            corner_radius=10,
            command=self.on_ir_login,
        ).pack()

    def _copiar_todo_registro(self):
        if self.resultado_registro:
            usuario = self.resultado_registro.get('usuario', {})
            email = usuario.get('email', '')
            nombre = usuario.get('nombre', '')
            rol = usuario.get('rol', '')
            contrasena = self.resultado_registro.get('contraseña_generada', '')
            texto = f"Nombre: {nombre}\nEmail: {email}\nContraseña: {contrasena}\nRol: {rol}"
            self.clipboard_clear()
            self.clipboard_append(texto)

    def _mostrar_paso_4(self):
        """Placeholder - ya no se usa, ahora es paso 3"""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 4 de 4 — Completado")
        self.progreso.set(1.0)
        self.boton_atras.pack_forget()
        self.link_login.pack_forget()
        self.boton_siguiente.configure(text="Ir al Login →")
        
        ctk.CTkLabel(
            self.contenido,
            text="✅",
            font=("Segoe UI Emoji", 80),
            text_color=COMPLETADO,
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.contenido,
            text="Registro completado",
            font=("Comic Sans MS", 26, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack()

        ctk.CTkLabel(
            self.contenido,
            text="Ya puedes iniciar sesión con tu email y contraseña",
            font=("Comic Sans MS", 15),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=(5, 15))

        if self.resultado_registro:
            usuario = self.resultado_registro.get('usuario', {})
            email = usuario.get('email', '')
            rol = usuario.get('rol', '')
            nombre = usuario.get('nombre', '')

            frame_info = ctk.CTkFrame(self.contenido, fg_color="transparent")
            frame_info.pack(pady=5)

            ctk.CTkLabel(
                frame_info,
                text="Nombre:",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack()

            ctk.CTkLabel(
                frame_info,
                text=nombre,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack()

            ctk.CTkLabel(
                frame_info,
                text="Email:",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(pady=(10, 0))

            ctk.CTkLabel(
                frame_info,
                text=email,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack()

            ctk.CTkLabel(
                frame_info,
                text="Rol:",
                font=("Comic Sans MS", 14, "bold"),
                text_color=TEXTO_SECUNDARIO,
            ).pack(pady=(10, 0))

            ctk.CTkLabel(
                frame_info,
                text=rol,
                font=("Comic Sans MS", 14),
                text_color=TEXTO_PRINCIPAL,
            ).pack()

            ctk.CTkButton(
                frame_info,
                text="📋 Copiar Email y Rol",
                font=("Comic Sans MS", 14),
                fg_color=BOTON_SECUNDARIO,
                hover_color=BOTON_SECUNDARIO_HOVER,
                text_color=TEXTO_PRINCIPAL,
                height=40,
                corner_radius=8,
                command=lambda: self._copiar_al_portapapeles(f"Email: {email}\nRol: {rol}"),
            ).pack(pady=15)

        ctk.CTkButton(
            self.contenido,
            text="Ir al Login →",
            font=("Comic Sans MS", 16, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=52,
            corner_radius=10,
            command=self.on_ir_login,
        ).pack(pady=15)

    def _copiar_al_portapapeles(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto)

    def _actualizar_longitud(self, valor):
        if hasattr(self, 'label_longitud') and self.label_longitud.winfo_exists():
            self.label_longitud.configure(text=f"{int(valor)} caracteres")

    def _copiar_contraseña(self):
        if self.resultado_registro:
            self.clipboard_clear()
            self.clipboard_append(self.resultado_registro['contraseña_generada'])

    def _validate_nombre(self, event=None):
        texto = self.entry_nombre.get()
        texto_filtrado = ""
        for c in texto:
            if c.isalpha() or c.isdigit() or c in "áéíóúüÁÉÍÓÚÜñÑ ":
                texto_filtrado += c
        if len(texto_filtrado) > 50:
            texto_filtrado = texto_filtrado[:50]
        if texto != texto_filtrado:
            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, texto_filtrado)
        
        tiene_letra = bool(any(c.isalpha() or c in "áéíóúüÁÉÍÓÚÜñÑ" for c in texto_filtrado))
        
        if len(texto_filtrado) < 2 and len(texto_filtrado) > 0:
            self.label_error.configure(text="El nombre debe tener al menos 2 caracteres")
        elif len(texto_filtrado) >= 2 and not tiene_letra:
            self.label_error.configure(text="El nombre debe contener al menos una letra")
        elif len(texto_filtrado) >= 2 and tiene_letra:
            self.label_error.configure(text="")

    def _on_nombre_change(self, event=None):
        self.datos_paso_1["nombre"] = self.entry_nombre.get()
        self._validate_nombre(event)
        self._verificar_duplicados_tiempo_real()

    def _on_email_change(self, event=None):
        self.datos_paso_1["email"] = self.entry_email.get()
        self._validate_email(event)
        self._verificar_duplicados_tiempo_real()

    def _verificar_duplicados_tiempo_real(self):
        import re
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        
        self.label_error.configure(text="")
        
        tiene_letra_nombre = bool(re.search(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]", nombre))
        nombre_valido = len(nombre) >= 2 and tiene_letra_nombre and re.match(r"^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ0-9\s]+$", nombre)
        
        if nombre_valido:
            try:
                from src.db.conexion import conexion_global
                coleccion = conexion_global.obtener_coleccion('usuarios')
                existe_nombre = coleccion.find_one({'nombre': {'$regex': f'^{re.escape(nombre)}$', '$options': 'i'}})
                if existe_nombre:
                    self.label_error.configure(text="El nombre ya está en uso")
                    self._actualizar_boton_siguiente(False)
                    return
            except Exception:
                pass
        
        partes_email = email.split("@") if "@" in email else []
        email_valido = False
        if len(partes_email) == 2 and partes_email[1]:
            dominio = partes_email[1]
            if "." in dominio:
                tld = dominio.rsplit(".", 1)[-1]
                if tld and len(tld) >= 2 and tld.isalpha() and len(tld) <= 10:
                    email_valido = True
                    try:
                        from src.db.conexion import conexion_global
                        coleccion = conexion_global.obtener_coleccion('usuarios')
                        existe_email = coleccion.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}})
                        if existe_email:
                            self.label_error.configure(text="El email ya está registrado")
                            self._actualizar_boton_siguiente(False)
                            return
                    except Exception:
                        pass
        
        if nombre_valido and email_valido:
            self._actualizar_boton_siguiente(True)
        else:
            self._actualizar_boton_siguiente(False)

    def _validate_email(self, event=None):
        texto = self.entry_email.get()
        if len(texto) > 64:
            texto = texto[:64]
            self.entry_email.delete(0, "end")
            self.entry_email.insert(0, texto)

    def _toggle_tipo_contraseña(self):
        """Muestra/oculta el campo de contraseña personalizada."""
        if self.tipo_contraseña.get() == "personalizada":
            self.frame_pass.pack(fill="x", pady=(0, 5))
        else:
            self.frame_pass.pack_forget()

    def _toggle_mostrar_pass(self):
        """Alterna mostrar/ocultar contraseña."""
        mostrar = "" if self.mostrar_pass.get() else "•"
        self.entry_pass.configure(show=mostrar)
        self.entry_pass2.configure(show=mostrar)

    def _validar_paso_1(self):
        import re
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()

        if not nombre:
            self.label_error.configure(text="El nombre es obligatorio")
            self._actualizar_boton_siguiente(False)
            return False

        if len(nombre) < 2:
            self.label_error.configure(text="El nombre debe tener al menos 2 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        if len(nombre) > 50:
            self.label_error.configure(text="El nombre debe tener máximo 50 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        tiene_letra = bool(re.search(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]", nombre))
        tiene_numero = bool(re.search(r"[0-9]", nombre))
        
        if not tiene_letra:
            self.label_error.configure(text="El nombre debe contener al menos una letra")
            self._actualizar_boton_siguiente(False)
            return False
        
        if not re.match(r"^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ0-9\s]+$", nombre):
            self.label_error.configure(text="El nombre contiene caracteres inválidos")
            self._actualizar_boton_siguiente(False)
            return False

        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            
            existe_nombre = coleccion.find_one({'nombre': {'$regex': f'^{re.escape(nombre)}$', '$options': 'i'}})
            if existe_nombre:
                self.label_error.configure(text="El nombre ya está en uso")
                self._actualizar_boton_siguiente(False)
                return False
        except Exception:
            pass

        if not email:
            self.label_error.configure(text="El email es obligatorio")
            self._actualizar_boton_siguiente(False)
            return False

        if len(email) > 64:
            self.label_error.configure(text="El email debe tener máximo 64 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        if "@" not in email:
            self.label_error.configure(text="El email debe contener @")
            self._actualizar_boton_siguiente(False)
            return False

        partes = email.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            self.label_error.configure(text="El formato del email es inválido")
            self._actualizar_boton_siguiente(False)
            return False

        local = partes[0]
        dominio = partes[1]

        if local.startswith(".") or local.endswith("."):
            self.label_error.configure(text="El email no puede empezar o terminar con punto")
            self._actualizar_boton_siguiente(False)
            return False

        if ".." in local:
            self.label_error.configure(text="El email no puede tener puntos consecutivos")
            self._actualizar_boton_siguiente(False)
            return False

        if not re.match(r"^[a-zA-Z0-9._+-]+$", local):
            self.label_error.configure(text="El email contiene caracteres inválidos")
            self._actualizar_boton_siguiente(False)
            return False

        if "." not in dominio:
            self.label_error.configure(text="El dominio debe tener un punto")
            self._actualizar_boton_siguiente(False)
            return False

        dominio_partes = dominio.rsplit(".", 1)
        if len(dominio_partes) != 2:
            self.label_error.configure(text="El dominio debe tener un TLD válido")
            self._actualizar_boton_siguiente(False)
            return False

        tld = dominio_partes[1]
        if len(tld) < 2:
            self.label_error.configure(text="El TLD debe tener mínimo 2 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        if len(tld) > 10:
            self.label_error.configure(text="El TLD debe tener máximo 10 caracteres")
            self._actualizar_boton_siguiente(False)
            return False

        if not tld.isalpha():
            self.label_error.configure(text="El TLD solo puede contener letras")
            self._actualizar_boton_siguiente(False)
            return False

        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            
            existe_email = coleccion.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}})
            if existe_email:
                self.label_error.configure(text="El email ya está registrado")
                self._actualizar_boton_siguiente(False)
                return False
        except Exception:
            pass

        self.label_error.configure(text="")
        self._actualizar_boton_siguiente(True)
        return True

    def _actualizar_boton_siguiente(self, habilitado):
        if hasattr(self, 'boton_siguiente'):
            if habilitado:
                self.boton_siguiente.configure(state="normal", fg_color=BOTON_PRIMARIO)
            else:
                self.boton_siguiente.configure(state="disabled", fg_color=BOTON_SECUNDARIO)

    def _siguiente(self):
        if self.paso_actual == 1:
            if not self._validar_paso_1():
                return
            
            self.datos_paso_1["nombre"] = self.entry_nombre.get().strip()
            self.datos_paso_1["email"] = self.entry_email.get().strip()
            self.datos_paso_1["rol"] = self.combo_rol.get()
            
            self.paso_actual = 2
            self._mostrar_paso_2()

        elif self.paso_actual == 2:
            self.datos_paso_2["longitud"] = int(self.slider_longitud.get())
            self.datos_paso_2["usar_mayusculas"] = self.var_mayus.get()
            self.datos_paso_2["usar_numeros"] = self.var_num.get()
            self.datos_paso_2["usar_simbolos"] = self.var_simb.get()
            self.datos_paso_2["excluir_ambiguos"] = self.var_ambig.get()
            self.datos_paso_2["tipo"] = self.tipo_contraseña.get()
            
            if hasattr(self, 'entry_pass') and hasattr(self.entry_pass, 'winfo_exists') and self.entry_pass.winfo_exists():
                contraseña = self.entry_pass.get()
                contraseña2 = self.entry_pass2.get()
                
                if self.tipo_contraseña.get() == "personalizada":
                    if len(contraseña) < 5:
                        self.label_error.configure(text="Mínimo 5 caracteres")
                        return
                    if len(contraseña) > 64:
                        self.label_error.configure(text="Máximo 64 caracteres")
                        return
                    if contraseña != contraseña2:
                        self.label_error.configure(text="Las contraseñas no coinciden")
                        return
                    
                    import re
                    if not re.search(r"[a-z]", contraseña):
                        self.label_error.configure(text="Debe tener al menos una minúscula (a-z)")
                        return
                    if not re.search(r"[A-Z]", contraseña):
                        self.label_error.configure(text="Debe tener al menos una mayúscula (A-Z)")
                        return
                    if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};:'\",./<>?\\|`~]", contraseña):
                        self.label_error.configure(text="Debe tener al menos un símbolo (!@#$%^&*...)")
                        return
                    
                    self.datos_paso_2["contraseña"] = contraseña
                    self.datos_paso_2["tipo"] = "personalizada"
                    self.label_error.configure(text="")
            
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
        if self.paso_actual == 2:
            if hasattr(self, 'entry_nombre') and self.entry_nombre.winfo_exists():
                self.datos_paso_1["nombre"] = self.entry_nombre.get().strip()
                self.datos_paso_1["email"] = self.entry_email.get().strip()
                if hasattr(self, 'combo_rol'):
                    self.datos_paso_1["rol"] = self.combo_rol.get()
            
            self.paso_actual = 1
            self.resultado_registro = None
            self._mostrar_paso_1()
            
        elif self.paso_actual == 3:
            if hasattr(self, 'slider_longitud') and self.slider_longitud.winfo_exists():
                self.datos_paso_2["longitud"] = int(self.slider_longitud.get())
                self.datos_paso_2["usar_mayusculas"] = self.var_mayus.get()
                self.datos_paso_2["usar_numeros"] = self.var_num.get()
                self.datos_paso_2["usar_simbolos"] = self.var_simb.get()
                self.datos_paso_2["excluir_ambiguos"] = self.var_ambig.get()
                self.datos_paso_2["tipo"] = self.tipo_contraseña.get()
                if hasattr(self, 'entry_semilla') and self.entry_semilla.winfo_exists():
                    self.datos_paso_2["semilla"] = self.entry_semilla.get().strip()
            
            self.paso_actual = 2
            self.resultado_registro = None
            self._mostrar_paso_2()
            
        elif self.paso_actual == 1:
            self.datos_paso_1 = {"nombre": "", "email": "", "rol": "empleado"}
            self.datos_paso_2 = {
                "longitud": 20,
                "usar_mayusculas": True,
                "usar_numeros": True,
                "usar_simbolos": True,
                "excluir_ambiguos": False,
                "tipo": "sistema",
                "semilla": ""
            }
            self.resultado_registro = None
            self.on_ir_login()

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
            "semilla": ""
        }
        self._mostrar_paso_1()

    def _ir_a_login(self):
        """Ir al login y limpiar datos."""
        self.datos_paso_1 = {"nombre": "", "email": "", "rol": "empleado"}
        self.datos_paso_2 = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False,
            "tipo": "sistema",
            "semilla": ""
        }
        self.on_ir_login()

