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
        self._crear_widgets()

    def _crear_widgets(self):
        # Card central
        self.card = ctk.CTkFrame(
            self,
            fg_color=FONDO_CARD,
            corner_radius=16,
            width=500,
            height=620,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Header con pasos
        self.header = ctk.CTkFrame(self.card, fg_color="transparent")
        self.header.pack(fill="x", padx=30, pady=(25, 10))

        self.label_paso = ctk.CTkLabel(
            self.header,
            text="Paso 1 de 4 — Datos personales",
            font=("Comic Sans MS", 16, "bold"),
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

        # Contenedor del paso (scrollable)
        self.contenido = ctk.CTkScrollableFrame(
            self.card, 
            fg_color="transparent",
            scrollbar_button_color=FONDO_SECUNDARIO,
            scrollbar_button_hover_color=BOTON_PRIMARIO,
        )
        self.contenido.pack(fill="both", expand=True, padx=30, pady=10)

        # Label de error
        self.label_error = ctk.CTkLabel(
            self.card,
            text="",
            font=("Comic Sans MS", 11),
            text_color=PELIGRO,
        )
        self.label_error.pack(pady=(0, 5))

        # Botonera inferior
        botones = ctk.CTkFrame(self.card, fg_color="transparent")
        botones.pack(fill="x", padx=30, pady=(0, 20))

        self.boton_atras = ctk.CTkButton(
            botones,
            text="← Atrás",
            font=("Comic Sans MS", 12),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            width=100,
            height=38,
            corner_radius=8,
            command=self._atras,
        )
        self.boton_atras.pack(side="left")

        self.boton_siguiente = ctk.CTkButton(
            botones,
            text="Siguiente →",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO,
            hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            width=140,
            height=38,
            corner_radius=8,
            command=self._siguiente,
        )
        self.boton_siguiente.pack(side="right")

        # Link login
        link = ctk.CTkLabel(
            self.card,
            text="¿Ya tienes cuenta? Inicia sesión",
            font=("Comic Sans MS", 11, "underline"),
            text_color=INFORMACION,
            cursor="hand2",
        )
        link.pack(pady=(0, 15))
        link.bind("<Button-1>", lambda e: self.on_ir_login())

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
            try:
                widget.destroy()
            except:
                pass

    def _mostrar_paso_1(self):
        """Paso 1: Datos personales."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 1 de 4 — Datos personales")
        self.progreso.set(0.25)
        self.boton_atras.configure(state="disabled")
        self.boton_siguiente.configure(text="Siguiente →")

        ctk.CTkLabel(
            self.contenido, text="Nombre completo",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(10, 0))

        self.entry_nombre = ctk.CTkEntry(
            self.contenido, placeholder_text="Tu nombre",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_nombre.pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(
            self.contenido, text="Email",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entry_email = ctk.CTkEntry(
            self.contenido, placeholder_text="usuario@empresa.com",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_email.pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(
            self.contenido, text="Rol",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        # Determinar opciones según si hay usuarios en BD
        es_primer_usuario = self._verificar_primer_usuario()

        if es_primer_usuario:
            # Primer usuario: puede elegir cualquier rol (incluido supervisor)
            roles_disponibles = ["supervisor", "encargado", "empleado"]
            ctk.CTkLabel(
                self.contenido,
                text="✅ Eres el primer usuario. Elige tu rol de administrador.",
                font=("Comic Sans MS", 10), text_color=COMPLETADO,
            ).pack(anchor="w", pady=(3, 5))
        else:
            # Ya hay usuarios: solo empleado por defecto
            roles_disponibles = ["empleado"]
            ctk.CTkLabel(
                self.contenido,
                text="Solo puedes registrarte como empleado.\n"
                     "Un supervisor puede cambiarte el rol después.",
                font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(3, 5))

        self.combo_rol = ctk.CTkComboBox(
            self.contenido,
            values=roles_disponibles,
            font=("Comic Sans MS", 13),
            fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL,
            button_color=BOTON_PRIMARIO,
            button_hover_color=BOTON_PRIMARIO_HOVER,
            dropdown_fg_color=FONDO_SECUNDARIO,
            height=38,
            corner_radius=8,
        )
        self.combo_rol.pack(fill="x", pady=(3, 10))
        self.combo_rol.set(roles_disponibles[0])

    def _mostrar_paso_2(self):
        """Paso 2: Parámetros de contraseña."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 2 de 4 — Parámetros de contraseña")
        self.progreso.set(0.5)
        self.boton_atras.configure(state="normal")
        self.boton_siguiente.configure(text="Generar →")

        ctk.CTkLabel(
            self.contenido,
            text="Configuraremos tu contraseña segura",
            font=("Comic Sans MS", 13),
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(10, 15))

        # Slider longitud
        ctk.CTkLabel(
            self.contenido, text="Longitud de la contraseña",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
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
            font=("Comic Sans MS", 12), text_color=TRABAJO_ACTIVO,
        )
        self.label_longitud.pack(anchor="e")

        # Slider se configura al final para evitar callbacks prematuros
        self.slider_longitud.set(20)
        self.slider_longitud.configure(command=self._actualizar_longitud)

        # Toggles
        self.var_mayus = ctk.BooleanVar(value=True)
        self.var_num = ctk.BooleanVar(value=True)
        self.var_simb = ctk.BooleanVar(value=True)
        self.var_ambig = ctk.BooleanVar(value=False)

        for texto, var in [
            ("Incluir mayúsculas (A-Z)", self.var_mayus),
            ("Incluir números (0-9)", self.var_num),
            ("Incluir símbolos (!@#$...)", self.var_simb),
            ("Excluir caracteres ambiguos (0,O,l,I,1)", self.var_ambig),
        ]:
            ctk.CTkCheckBox(
                self.contenido, text=texto, variable=var,
                font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
                fg_color=FONDO_SECUNDARIO, checkmark_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", pady=(8, 0))

        # Opcion contrasena personalizada
        ctk.CTkFrame(self.contenido, fg_color=BORDE, height=1).pack(fill="x", pady=(15, 10))

        self.tipo_contraseña = ctk.StringVar(value="sistema")

        ctk.CTkRadioButton(
            self.contenido, text="Generada por el sistema (recomendado)",
            variable=self.tipo_contraseña, value="sistema",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
            fg_color=TRABAJO_ACTIVO, hover_color=BOTON_PRIMARIO_HOVER,
            command=self._toggle_tipo_contraseña,
        ).pack(anchor="w")

        ctk.CTkRadioButton(
            self.contenido, text="Personalizada (tu decides los caracteres)",
            variable=self.tipo_contraseña, value="personalizada",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
            fg_color=TRABAJO_ACTIVO, hover_color=BOTON_PRIMARIO_HOVER,
            command=self._toggle_tipo_contraseña,
        ).pack(anchor="w", pady=(2, 5))

        self.frame_semilla = ctk.CTkFrame(self.contenido, fg_color="transparent")
        self.frame_semilla.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            self.frame_semilla, text="Tus caracteres:",
            font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entry_semilla = ctk.CTkEntry(
            self.frame_semilla,
            placeholder_text="Ej: ADEV1130$yasuo05",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
        )
        self.entry_semilla.pack(fill="x")

        ctk.CTkLabel(
            self.frame_semilla,
            text="Min 8 caracteres. El sistema los mezclara para crear tu contrasena.",
            font=("Comic Sans MS", 9), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(2, 0))

        self.frame_semilla.pack_forget()  # Oculto por defecto

        # Preview fortaleza
        self.label_preview = ctk.CTkLabel(
            self.contenido,
            text="Fortaleza estimada: calculando...",
            font=("Comic Sans MS", 11),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_preview.pack(anchor="w", pady=(15, 0))

    def _mostrar_paso_3(self):
        """Paso 3: Contraseña generada."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 3 de 4 — Tu contraseña")
        self.progreso.set(0.75)
        self.boton_siguiente.configure(text="Continuar →")

        ctk.CTkLabel(
            self.contenido,
            text="⚠️ Esta es la única vez que la verás así.\nGuárdala en un lugar seguro.",
            font=("Comic Sans MS", 12),
            text_color=AVISO,
            justify="center",
        ).pack(pady=(20, 15))

        # Contraseña generada
        self.label_contraseña = ctk.CTkLabel(
            self.contenido,
            text=self.resultado_registro.get('contraseña_generada', ''),
            font=("Comic Sans MS", 18, "bold"),
            text_color=COMPLETADO,
        )
        self.label_contraseña.pack(pady=10)

        # Fortaleza
        ctk.CTkLabel(
            self.contenido,
            text="✅ Muy fuerte — 99%",
            font=("Comic Sans MS", 14),
            text_color=COMPLETADO,
        ).pack()

        # Botón copiar
        ctk.CTkButton(
            self.contenido,
            text="📋 Copiar al portapapeles",
            font=("Comic Sans MS", 12),
            fg_color=BOTON_SECUNDARIO,
            hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL,
            height=38,
            corner_radius=8,
            command=self._copiar_contraseña,
        ).pack(pady=15)

    def _mostrar_paso_4(self):
        """Paso 4: Confirmación."""
        self._limpiar_contenido()
        self.label_paso.configure(text="Paso 4 de 4 — Completado")
        self.progreso.set(1.0)
        self.boton_siguiente.configure(text="Ir al Login →")

        ctk.CTkLabel(
            self.contenido,
            text="✅",
            font=("Segoe UI Emoji", 64),
            text_color=COMPLETADO,
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self.contenido,
            text="Registro completado",
            font=("Comic Sans MS", 22, "bold"),
            text_color=TEXTO_PRINCIPAL,
        ).pack()

        ctk.CTkLabel(
            self.contenido,
            text="Ya puedes iniciar sesión con tu email y contraseña",
            font=("Comic Sans MS", 13),
            text_color=TEXTO_SECUNDARIO,
        ).pack(pady=10)

        # Info del usuario
        if self.resultado_registro:
            usuario = self.resultado_registro.get('usuario', {})
            ctk.CTkLabel(
                self.contenido,
                text=f"Email: {usuario.get('email', '')}\nRol: {usuario.get('rol', '')}",
                font=("Comic Sans MS", 12),
                text_color=TEXTO_SECUNDARIO,
                justify="center",
            ).pack(pady=10)

    def _actualizar_longitud(self, valor):
        if hasattr(self, 'label_longitud') and self.label_longitud.winfo_exists():
            self.label_longitud.configure(text=f"{int(valor)} caracteres")

    def _copiar_contraseña(self):
        if self.resultado_registro:
            self.clipboard_clear()
            self.clipboard_append(self.resultado_registro['contraseña_generada'])

    def _toggle_tipo_contraseña(self):
        """Muestra/oculta el campo de semilla personalizada."""
        if self.tipo_contraseña.get() == "personalizada":
            self.frame_semilla.pack(fill="x", pady=(0, 5))
        else:
            self.frame_semilla.pack_forget()

    def _validar_paso_1(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        if not nombre:
            self.label_error.configure(text="El nombre es obligatorio")
            return False
        if not email:
            self.label_error.configure(text="El email es obligatorio")
            return False
        self.label_error.configure(text="")
        return True

    def _siguiente(self):
        if self.paso_actual == 1:
            if not self._validar_paso_1():
                return
            # Registrar usuario con parámetros por defecto (se ajustan en paso 2)
            try:
                from src.auth import registrar_usuario
                parametros_defecto = {
                    "longitud": 20,
                    "usar_mayusculas": True,
                    "usar_numeros": True,
                    "usar_simbolos": True,
                    "excluir_ambiguos": False,
                }
                self.resultado_registro = registrar_usuario(
                    self.entry_email.get().strip(),
                    self.entry_nombre.get().strip(),
                    self.combo_rol.get(),
                    parametros_defecto,
                )
                self.paso_actual = 2
                self._mostrar_paso_2()
            except Exception as e:
                self.label_error.configure(text=str(e))
                return

        elif self.paso_actual == 2:
            try:
                uid = str(self.resultado_registro['usuario']['_id'])

                if hasattr(self, 'tipo_contraseña') and self.tipo_contraseña.get() == "personalizada":
                    # Contrasena personalizada con semilla
                    semilla = self.entry_semilla.get().strip()
                    if len(semilla) < 8:
                        self.label_error.configure(text="La semilla debe tener minimo 8 caracteres")
                        return
                    from src.generador import generar_contraseña_personalizada
                    from src.seguridad.encriptacion import hashear_contraseña, cifrar
                    from src.db.conexion import conexion_global

                    pw = generar_contraseña_personalizada(semilla)
                    nuevo_hash = hashear_contraseña(pw)
                    nueva_enc = cifrar(pw)

                    coleccion = conexion_global.obtener_coleccion('usuarios')
                    coleccion.update_one(
                        {'_id': self.resultado_registro['usuario']['_id']},
                        {'$set': {
                            'contraseña_hash': nuevo_hash,
                            'contraseña_encriptada': nueva_enc,
                        }}
                    )
                    self.resultado_registro['contraseña_generada'] = pw
                else:
                    # Contrasena generada por el sistema
                    if hasattr(self, 'slider_longitud'):
                        from src.auth import regenerar_contraseña
                        nuevos_params = {
                            "longitud": int(self.slider_longitud.get()),
                            "usar_mayusculas": self.var_mayus.get(),
                            "usar_numeros": self.var_num.get(),
                            "usar_simbolos": self.var_simb.get(),
                            "excluir_ambiguos": self.var_ambig.get(),
                        }
                        self.resultado_registro = regenerar_contraseña(uid, nuevos_params)
                        self.resultado_registro['usuario'] = self.resultado_registro.get('usuario', {})
                        if 'nueva_contraseña' in self.resultado_registro:
                            self.resultado_registro['contraseña_generada'] = self.resultado_registro['nueva_contraseña']

                self.paso_actual = 3
                self._mostrar_paso_3()
            except Exception as e:
                self.label_error.configure(text=str(e))
                return

        elif self.paso_actual == 3:
            self.paso_actual = 4
            self._mostrar_paso_4()

        elif self.paso_actual == 4:
            self.on_ir_login()

    def _atras(self):
        if self.paso_actual > 1:
            self.paso_actual -= 1
            if self.paso_actual == 1:
                self._mostrar_paso_1()
            elif self.paso_actual == 2:
                self._mostrar_paso_2()
            elif self.paso_actual == 3:
                self._mostrar_paso_3()
        else:
            # Volver al login
            self.on_ir_login()

    def limpiar(self):
        """Resetea la vista de registro."""
        self.paso_actual = 1
        self.resultado_registro = None
        self._mostrar_paso_1()

