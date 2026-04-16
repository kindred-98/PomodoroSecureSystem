"""
Módulo: password_view.py
Responsabilidad: Gestión de contraseña del usuario (ver, regenerar, cambiar, exportar).
"""

import customtkinter as ctk
from src.config.colores import *


class PasswordView(ctk.CTkFrame):
    """Pantalla de gestión de contraseña."""

    def __init__(self, parent, usuario, on_volver):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_volver = on_volver
        self._crear_widgets()

    def _crear_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header, text="← Volver",
            font=("Comic Sans MS", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=36, corner_radius=8,
            command=self.on_volver,
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkLabel(
            header, text="🔑 Gestión de Contraseña",
            font=("Comic Sans MS", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        # Contenido con scroll
        contenido = ctk.CTkScrollableFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)

        # ── OPCIÓN A: Ver contraseña ──
        card_ver = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_ver.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_ver, text="👁️ Ver contraseña actual",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_ver,
            text="Introduce tu PIN de 6 digitos (generado al iniciar sesion).",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_ver = ctk.CTkFrame(card_ver, fg_color="transparent")
        frame_ver.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_ver = ctk.CTkEntry(
            frame_ver, placeholder_text="PIN de 6 digitos",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_ver.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_ver, text="🔍 Ver",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=80, height=40, corner_radius=8,
            command=self._ver_contraseña,
        ).pack(side="right")

        self.label_ver_resultado = ctk.CTkLabel(
            card_ver, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_ver_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── GENERAR PIN DE 6 DÍGITOS ──
        card_pin = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_pin.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_pin, text="🔐 Generar PIN de 6 dígitos",
            font=("Comic Sans MS", 14, "bold"), text_color="#9B59B6",
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_pin,
            text="PIN para ver contraseña. Solo 1 cada hora por seguridad.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_pin = ctk.CTkFrame(card_pin, fg_color="transparent")
        frame_pin.pack(fill="x", padx=20, pady=(10, 5))

        self.boton_generar_pin = ctk.CTkButton(
            frame_pin, text="🔑 Generar PIN",
            font=("Comic Sans MS", 12, "bold"),
            fg_color="#9B59B6", hover_color="#8E44AD",
            text_color=TEXTO_PRINCIPAL, width=130, height=40, corner_radius=8,
            command=self._generar_pin,
        )
        self.boton_generar_pin.pack(side="left", padx=(0, 10))
        
        self._verificar_bloqueo_pin()

        # Resultado + Copiar juntos
        self.label_pin_resultado = ctk.CTkLabel(
            frame_pin, text="",
            font=("Comic Sans MS", 22, "bold"),
            text_color="#9B59B6",
        )
        self.label_pin_resultado.pack(side="left", padx=(10, 0))
        
        ctk.CTkButton(
            frame_pin, text="📋 Copiar",
            font=("Comic Sans MS", 10),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=70, height=40,
            command=self._copiar_pin,
        ).pack(side="left")

        self.label_pin_aviso = ctk.CTkLabel(
            card_pin, text="",
            font=("Comic Sans MS", 10),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_pin_aviso.pack(anchor="w", padx=20, pady=(0, 15))

        # ── FRASE SEMILLA (RECUPERACIÓN) ──
        self._ultima_frase_mostrada = None
        
        card_semilla = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_semilla.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_semilla, text="🔑 Frase Semilla de Recuperación",
            font=("Comic Sans MS", 14, "bold"), text_color="#E7952B",
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_semilla,
            text="12 palabras para recuperar tu cuenta. Solo se genera cada 90 dias.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_semilla = ctk.CTkFrame(card_semilla, fg_color="transparent")
        frame_semilla.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkButton(
            frame_semilla, text="🔑 Generar Frase",
            font=("Comic Sans MS", 12, "bold"),
            fg_color="#E7952B", hover_color="#D7841B",
            text_color=TEXTO_PRINCIPAL, width=150, height=40, corner_radius=8,
            command=self._generar_frase_semilla,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_semilla, text="📋 Copiar",
            font=("Comic Sans MS", 10),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=70, height=40,
            command=self._copiar_frase,
        ).pack(side="left")

        self.label_semilla_resultado = ctk.CTkLabel(
            card_semilla, text="", font=("Comic Sans MS", 12),
            text_color="#E7952B",
        )
        self.label_semilla_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── CONTRASEÑA SEGURA ──
        card_reg = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_reg.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_reg, text="🔐 Contraseña Segura",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_reg,
            text="Genera una nueva contraseña con parámetros diferentes.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_reg = ctk.CTkFrame(card_reg, fg_color="transparent")
        frame_reg.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkButton(
            frame_reg, text="🔄 Generar",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=150, height=40, corner_radius=8,
            command=self._regenerar,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_reg, text="📋 Copiar",
            font=("Comic Sans MS", 10),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=70, height=40,
            command=self._copiar_segura,
        ).pack(side="left")

        self.label_reg_resultado = ctk.CTkLabel(
            card_reg, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_reg_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN C: Contraseña personalizada ──
        card_custom = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_custom.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_custom, text="🔧 Contraseña personalizada",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_custom,
            text="El sistema mezcla tus caracteres para crear una contrasena fuerte.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_custom = ctk.CTkFrame(card_custom, fg_color="transparent")
        frame_custom.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_semilla_pw = ctk.CTkEntry(
            frame_custom, placeholder_text="Ej: ADEV1130$yasuo05 (min 8 chars)",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_semilla_pw.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_custom, text="Generar",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=90, height=38, corner_radius=8,
            command=self._generar_personalizada,
        ).pack(side="right")

        self.label_custom_resultado = ctk.CTkLabel(
            card_custom, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_custom_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN D: Cambio manual ──
        card_manual = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_manual.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_manual, text="✏️ Cambio manual",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_manual,
            text="La contrasena debe ser nivel 'Muy Fuerte' (>=80 pts). Se pedira la actual para confirmar.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        # Contraseña actual
        frame_manual_actual = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual_actual.pack(fill="x", padx=20, pady=(10, 2))

        ctk.CTkLabel(frame_manual_actual, text="Actual:", font=("Comic Sans MS", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual_actual = ctk.CTkEntry(
            frame_manual_actual, placeholder_text="Contrasena actual",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8, show="•",
        )
        self.entry_manual_actual.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Nueva contraseña
        frame_manual = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual.pack(fill="x", padx=20, pady=(2, 5))

        ctk.CTkLabel(frame_manual, text="Nueva:", font=("Comic Sans MS", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual = ctk.CTkEntry(
            frame_manual, placeholder_text="Nueva contrasena",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
        )
        self.entry_manual.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Repetir nueva contraseña  
        frame_repetir = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_repetir.pack(fill="x", padx=20, pady=(2, 5))

        ctk.CTkLabel(frame_repetir, text="Repetir:", font=("Comic Sans MS", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual_repetir = ctk.CTkEntry(
            frame_repetir, placeholder_text="Repetir nueva contrasena",
            font=("Comic Sans MS", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
        )
        self.entry_manual_repetir.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Botón cambiar debajo
        ctk.CTkButton(
            card_manual, text="✓ Cambiar Contraseña",
            font=("Comic Sans MS", 12, "bold"),
            fg_color="#10B981", hover_color="#059669",
            text_color=TEXTO_PRINCIPAL, width=180, height=40, corner_radius=8,
            command=self._cambiar_manual,
        ).pack(anchor="w", padx=20, pady=(10, 5))

        # Indicador de fortaleza en tiempo real
        self.label_fortaleza_tiempo = ctk.CTkLabel(
            card_manual, text="Escribe tu contrasena...",
            font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO,
        )
        self.label_fortaleza_tiempo.pack(anchor="w", padx=20)

        self.barra_fortaleza = ctk.CTkProgressBar(
            card_manual,
            fg_color=FONDO_SECUNDARIO,
            progress_color=TEXTO_SECUNDARIO,
            height=6, corner_radius=3,
        )
        self.barra_fortaleza.pack(fill="x", padx=20, pady=(2, 10))
        self.barra_fortaleza.set(0)

        self.entry_manual.bind("<KeyRelease>", self._actualizar_fortaleza_tiempo)

        self.label_manual_resultado = ctk.CTkLabel(
            card_manual, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_manual_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── EXPORTAR A TXT/JSON (SIN ENCRIPTAR) ──
        card_export = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_export.pack(fill="x")

        ctk.CTkLabel(
            card_export, text="💾 Exportar (sin encriptar)",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_export,
            text="Archivo legible con tu email, contraseña y frase semilla.",
            font=("Comic Sans MS", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_export = ctk.CTkFrame(card_export, fg_color="transparent")
        frame_export.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkButton(
            frame_export, text="Exportar TXT",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
            command=self._exportar_txt,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_export, text="Exportar JSON",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
            command=self._exportar_json,
        ).pack(side="left")

        self.label_export_resultado = ctk.CTkLabel(
            card_export, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_export_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkButton(
            card_export, text="Exportar",
            font=("Comic Sans MS", 12, "bold"),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
            command=self._exportar,
        ).pack(anchor="w", padx=20, pady=(10, 15))

        self.label_export_resultado = ctk.CTkLabel(
            card_export, text="", font=("Comic Sans MS", 12),
            text_color=COMPLETADO,
        )
        self.label_export_resultado.pack(anchor="w", padx=20, pady=(0, 15))

    def _ver_contraseña(self):
        pin = self.entry_ver.get().strip()
        if not pin:
            self.label_ver_resultado.configure(text="Introduce tu PIN", text_color=PELIGRO)
            return
        try:
            from src.auth.pin_diario import verificar_pin_diario
            uid = str(self.usuario['_id'])

            if not verificar_pin_diario(uid, pin):
                self.label_ver_resultado.configure(text="PIN incorrecto", text_color=PELIGRO)
                return

            # PIN correcto, desencriptar contraseña
            from src.db.conexion import conexion_global
            from src.seguridad.encriptacion import descifrar

            coleccion = conexion_global.obtener_coleccion('usuarios')
            usuario = coleccion.find_one({'_id': self.usuario['_id']})
            enc = usuario.get('contraseña_encriptada', '')

            if not enc:
                self.label_ver_resultado.configure(
                    text="No hay contrasena encriptada", text_color=PELIGRO
                )
                return

            pw = descifrar(enc)
            self.label_ver_resultado.configure(
                text=f"Tu contrasena: {pw}", text_color=COMPLETADO
            )
        except Exception as e:
            self.label_ver_resultado.configure(text=str(e), text_color=PELIGRO)

    def _actualizar_fortaleza_tiempo(self, event=None):
        """Actualiza el indicador de fortaleza en cada keystroke."""
        pw = self.entry_manual.get()
        if not pw:
            self.label_fortaleza_tiempo.configure(text="Escribe tu contrasena...", text_color=TEXTO_SECUNDARIO)
            self.barra_fortaleza.set(0)
            self.barra_fortaleza.configure(progress_color=TEXTO_SECUNDARIO)
            return

        try:
            from src.generador import evaluar_fortaleza
            resultado = evaluar_fortaleza(pw)
            puntuacion = resultado.get('puntuacion', 0)
            nivel = resultado.get('nivel', 'Muy Debil')

            self.label_fortaleza_tiempo.configure(
                text=f"{nivel} ({puntuacion}/100)",
                text_color=self._color_fortaleza(puntuacion),
            )
            self.barra_fortaleza.set(puntuacion / 100)
            self.barra_fortaleza.configure(progress_color=self._color_fortaleza(puntuacion))
        except Exception:  # nosec B110
            pass

    @staticmethod
    def _color_fortaleza(puntuacion):
        """Retorna el color segun la puntuacion."""
        if puntuacion >= 80:
            return COMPLETADO
        elif puntuacion >= 60:
            return AVISO
        elif puntuacion >= 40:
            return INFORMACION
        else:
            return PELIGRO

    def _regenerar(self):
        try:
            from src.auth import regenerar_contraseña
            params = self.usuario.get('parametros_contraseña', {
                "longitud": 20, "usar_mayusculas": True,
                "usar_numeros": True, "usar_simbolos": True,
                "excluir_ambiguos": False,
            })
            resultado = regenerar_contraseña(str(self.usuario['_id']), params)
            self.label_reg_resultado.configure(
                text=f"Nueva contraseña: {resultado['nueva_contraseña']}",
                text_color=COMPLETADO,
            )
        except Exception as e:
            self.label_reg_resultado.configure(text=str(e), text_color=PELIGRO)

    def _generar_personalizada(self):
        """Genera contraseña usando los caracteres del usuario."""
        semilla = self.entry_semilla_pw.get().strip()
        if len(semilla) < 8:
            self.label_custom_resultado.configure(
                text="Minimo 8 caracteres", text_color=PELIGRO
            )
            return
        try:
            from src.generador import generar_contraseña_personalizada
            from src.seguridad.encriptacion import hashear_contraseña, cifrar
            from src.db.conexion import conexion_global

            pw = generar_contraseña_personalizada(semilla)
            nuevo_hash = hashear_contraseña(pw)
            nueva_enc = cifrar(pw)

            coleccion = conexion_global.obtener_coleccion('usuarios')
            coleccion.update_one(
                {'_id': self.usuario['_id']},
                {'$set': {
                    'contraseña_hash': nuevo_hash,
                    'contraseña_encriptada': nueva_enc,
                }}
            )

            self.label_custom_resultado.configure(
                text=f"Tu contrasena: {pw}", text_color=COMPLETADO
            )
        except Exception as e:
            self.label_custom_resultado.configure(text=str(e), text_color=PELIGRO)

    def _cambiar_manual(self):
        pw_actual = self.entry_manual_actual.get()
        pw_nueva = self.entry_manual.get()
        pw_repetir = self.entry_manual_repetir.get()

        if not pw_actual or not pw_nueva or not pw_repetir:
            self.label_manual_resultado.configure(
                text="Todos los campos son obligatorios", text_color=PELIGRO
            )
            return

        if pw_nueva != pw_repetir:
            self.label_manual_resultado.configure(
                text="Las contraseñas no coinciden", text_color=PELIGRO
            )
            return

        try:
            # Verificar contraseña actual
            from src.seguridad.encriptacion import verificar_contraseña
            from src.db.conexion import conexion_global

            coleccion = conexion_global.obtener_coleccion('usuarios')
            usuario = coleccion.find_one({'_id': self.usuario['_id']})

            if not verificar_contraseña(pw_actual, usuario.get('contraseña_hash', '')):
                self.label_manual_resultado.configure(
                    text="Contrasena actual incorrecta", text_color=PELIGRO
                )
                return

            # Contraseña actual correcta, cambiar a la nueva
            from src.auth import cambiar_contraseña
            resultado = cambiar_contraseña(str(self.usuario['_id']), pw_nueva)
            self.label_manual_resultado.configure(
                text=resultado['mensaje'], text_color=COMPLETADO
            )
            self.entry_manual_actual.delete(0, "end")
            self.entry_manual.delete(0, "end")
        except Exception as e:
            self.label_manual_resultado.configure(text=str(e), text_color=PELIGRO)

    def _exportar(self):
        try:
            from src.auth import exportar_contraseña
            from tkinter import filedialog
            ruta = filedialog.asksaveasfilename(
                defaultextension=".enc",
                filetypes=[("Encriptado", "*.enc")],
                title="Guardar contraseña",
            )
            if ruta:
                exportar_contraseña(str(self.usuario['_id']), ruta)
                self.label_export_resultado.configure(
                    text=f"Exportado: {ruta}", text_color=COMPLETADO
                )
        except Exception as e:
            self.label_export_resultado.configure(text=str(e), text_color=PELIGRO)

    def _exportar_txt(self):
        try:
            from src.auth import obtener_contraseña
            from tkinter import filedialog
            from datetime import datetime
            from src.auth.frase_semilla import obtener_ultima_frase
            
            ruta = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto plano", "*.txt")],
                title="Exportar datos",
            )
            if not ruta:
                return
            
            pw = obtener_contraseña(str(self.usuario['_id']))
            email = self.usuario.get('email', 'N/A')
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
            
# Frase semilla - siempre mostrar si existe
            frase_info = ""
            try:
                from src.auth.frase_semilla import obtener_ultima_frase
                from src.seguridad.encriptacion import descifrar
                from src.db.conexion import conexion_global
                
                # Fecha de la frase
                ult = obtener_ultima_frase(str(self.usuario['_id']))
                if ult:
                    desde = ult.get('generada_en')
                    if desde:
                        fecha_frase = desde.strftime('%Y-%m-%d %H:%M')
                        
                        # Palabras (si están guardadas)
                        usuarios = conexion_global.obtener_coleccion('usuarios')
                        usuario = usuarios.find_one({'_id': self.usuario['_id']})
                        enc = usuario.get('frase_semilla_encriptada', '')
                        palabras = descifrar(enc) if enc else ""
                        
                        # Si hay palabras o la frase reciente
                        if palabras:
                            frase_info = f"Generada: {fecha_frase}\n{palabras}"
                        elif hasattr(self, '_ultima_frase_mostrada') and self._ultima_frase_mostrada:
                            frase_info = f"Generada: {fecha_frase}\n{self._ultima_frase_mostrada}"
                        else:
                            frase_info = f"Generada: {fecha_frase}"
            except Exception as e:
                frase_info = ""
            
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(f"Usuario: {email}\n")
                f.write(f"Fecha exportacion: {fecha}\n")
                f.write(f"Contrasena: {pw}\n")
                if frase_info:
                    f.write(f"Frase Semilla: {frase_info}\n")
            
            self.label_export_resultado.configure(
                text=f"✓ Exportado: {ruta}", text_color=COMPLETADO
            )
        except Exception as e:
            self.label_export_resultado.configure(text=str(e), text_color=PELIGRO)

    def _exportar_json(self):
        try:
            from src.auth import obtener_contraseña
            from tkinter import filedialog
            from datetime import datetime
            import json
            from src.auth.frase_semilla import obtener_ultima_frase
            
            ruta = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json")],
                title="Exportar datos",
            )
            if not ruta:
                return
            
            pw = obtener_contraseña(str(self.usuario['_id']))
            email = self.usuario.get('email', 'N/A')
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            data = {
                "usuario": email,
                "fecha_exportacion": fecha,
                "contrasena": pw,
            }
            
            # Frase semilla - siempre mostrar si existe
            try:
                from src.auth.frase_semilla import obtener_ultima_frase
                from src.seguridad.encriptacion import descifrar
                from src.db.conexion import conexion_global
                
                ult = obtener_ultima_frase(str(self.usuario['_id']))
                if ult:
                    desde = ult.get('generada_en')
                    if desde:
                        fecha_frase = desde.strftime('%Y-%m-%d %H:%M')
                        
                        usuarios = conexion_global.obtener_coleccion('usuarios')
                        usuario = usuarios.find_one({'_id': self.usuario['_id']})
                        enc = usuario.get('frase_semilla_encriptada', '')
                        palabras = descifrar(enc) if enc else ""
                        
                        if palabras:
                            data["frase_semilla"] = {"generada": fecha_frase, "palabras": palabras}
                        elif hasattr(self, '_ultima_frase_mostrada') and self._ultima_frase_mostrada:
                            data["frase_semilla"] = {"generada": fecha_frase, "palabras": self._ultima_frase_mostrada}
                        else:
                            data["frase_semilla"] = {"generada": fecha_frase}
            except Exception as e:  # nosec B110
                pass
            
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.label_export_resultado.configure(
                text=f"✓ Exportado: {ruta}", text_color=COMPLETADO
            )
        except Exception as e:
            self.label_export_resultado.configure(text=str(e), text_color=PELIGRO)

    def _generar_pin(self):
        """Genera nuevo PIN de 6 dígitos (1 cada hora)."""
        try:
            from src.auth.pin_diario import generar_pin_diario, eliminar_pin_diario, obtener_ultimo_pin
            from datetime import datetime, timezone, timedelta
            uid = str(self.usuario['_id'])
            
            ultimo = obtener_ultimo_pin(uid)
            if ultimo:
                desde = ultimo.get('ultimo_intento')
                if desde:
                    desde = desde.replace(tzinfo=timezone.utc) if desde.tzinfo is None else desde
                    limite = datetime.now(timezone.utc) - timedelta(hours=1)
                    if desde > limite:
                        minutos = int((datetime.now(timezone.utc) - desde).total_seconds() // 60)
                        self.label_pin_resultado.configure(
                            text=f"⚠ Espera {60-minutos} min", text_color=PELIGRO
                        )
                        self.label_pin_aviso.configure(text="Debes esperar 1 hora")
                        return
            
            eliminar_pin_diario(uid)
            pin = generar_pin_diario(uid)

            if pin:
                self.boton_generar_pin.configure(state="disabled")
                self.after(3600000, self._desbloquear_pin)
                
                self.label_pin_resultado.configure(text=pin, text_color="#9B59B6")
                self.label_pin_aviso.configure(
                    text="✓ Copialo ahora. Nuevo en 1 hora.", text_color=COMPLETADO
                )
            else:
                self.label_pin_resultado.configure(text="Error", text_color=PELIGRO)
        except Exception as e:
            self.label_pin_resultado.configure(text=str(e), text_color=PELIGRO)

    def _generar_frase_semilla(self):
        """Genera frase semilla de recuperación (cada 90 dias)."""
        try:
            from src.auth.frase_semilla import generar_frase_usuario, obtener_ultima_frase
            from datetime import datetime, timezone, timedelta
            uid = str(self.usuario['_id'])
            
            ultima = obtener_ultima_frase(uid)
            if ultima:
                desde = ultima.get('generada_en')
                if desde:
                    desde = desde.replace(tzinfo=timezone.utc) if desde.tzinfo is None else desde
                    limite = datetime.now(timezone.utc) - timedelta(days=90)
                    if desde > limite:
                        dias = 90 - int((datetime.now(timezone.utc) - desde).days)
                        self.label_semilla_resultado.configure(
                            text=f"⚠ Espera {dias} dias", text_color=PELIGRO
                        )
                        return
            
            frase = generar_frase_usuario(uid)
            if frase:
                self._ultima_frase_mostrada = frase
                self.label_semilla_resultado.configure(
                    text=f"📝 {frase}", text_color="#E7952B"
                )
            else:
                self.label_semilla_resultado.configure(
                    text="Error al generar", text_color=PELIGRO
                )
        except Exception as e:
            self.label_semilla_resultado.configure(text=str(e), text_color=PELIGRO)

    def _copiar_frase(self):
        if self._ultima_frase_mostrada:
            self.clipboard_clear()
            self.clipboard_append(self._ultima_frase_mostrada)
            self.label_semilla_resultado.configure(text="✓ Copiado!", text_color=COMPLETADO)

    def _desbloquear_pin(self):
        if hasattr(self, 'boton_generar_pin'):
            self.boton_generar_pin.configure(state="normal")
    
    def _verificar_bloqueo_pin(self):
        try:
            from src.auth.pin_diario import obtener_ultimo_pin
            from datetime import datetime, timezone, timedelta
            uid = str(self.usuario['_id'])
            ultimo = obtener_ultimo_pin(uid)
            if ultimo:
                desde = ultimo.get('ultimo_intento')
                if desde:
                    desde = desde.replace(tzinfo=timezone.utc) if desde.tzinfo is None else desde
                    limite = datetime.now(timezone.utc) - timedelta(hours=1)
                    if desde > limite:
                        self.boton_generar_pin.configure(state="disabled")
                        self.after(3600000, self._desbloquear_pin)
        except Exception:  # nosec B110
            pass

    def _copiar_pin(self):
        texto = self.label_pin_resultado.cget("text")
        if texto and texto != "⚠ Espera" and texto != "Error":
            self.clipboard_clear()
            self.clipboard_append(texto)
            self.label_pin_aviso.configure(text="✓ Copiado!", text_color=COMPLETADO)

    def _copiar_segura(self):
        """Copia la contraseña segura generada."""
        texto = self.label_reg_resultado.cget("text")
        if texto and "contraseña:" in texto.lower():
            pw = texto.split("contraseña:")[-1].strip()
            self.clipboard_clear()
            self.clipboard_append(pw)
            self.label_reg_resultado.configure(text="✓ Copiado!", text_color=COMPLETADO)

