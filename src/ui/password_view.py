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
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=36, corner_radius=8,
            command=self.on_volver,
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkLabel(
            header, text="🔑 Gestión de Contraseña",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        # Contenido con scroll para que todas las secciones sean accesibles
        contenido = ctk.CTkScrollableFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)

        # ── OPCIÓN A: Ver contraseña ──
        card_ver = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_ver.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_ver, text="Ver contrasena actual",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_ver,
            text="Introduce tu PIN de 6 digitos (generado al iniciar sesion).",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_ver = ctk.CTkFrame(card_ver, fg_color="transparent")
        frame_ver.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_ver = ctk.CTkEntry(
            frame_ver, placeholder_text="PIN de 6 digitos",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_ver.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_ver, text="Ver",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=80, height=38, corner_radius=8,
            command=self._ver_contraseña,
        ).pack(side="right")

        self.label_ver_resultado = ctk.CTkLabel(
            card_ver, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_ver_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN B: Contraseñas Seguras ──
        card_reg = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_reg.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_reg, text="🔄 Contraseñas Seguras",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_reg,
            text="Introduce una semilla para generar una contraseña segura con tus datos.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_reg = ctk.CTkFrame(card_reg, fg_color="transparent")
        frame_reg.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_semilla_reg = ctk.CTkEntry(
            frame_reg, placeholder_text="Ej: MiClaveSegura2024! (min 8 chars)",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_semilla_reg.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_reg, text="Generar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=90, height=38, corner_radius=8,
            command=self._regenerar,
        ).pack(side="right")

        self.label_reg_resultado = ctk.CTkLabel(
            card_reg, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_reg_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN C: Generar PIN de 6 dígitos ──
        card_pin = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_pin.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_pin, text="🔐 Generar PIN de 6 dígitos",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_pin,
            text="Genera un PIN para ver tu contraseña actual (válido solo para hoy). Solo se muestra una vez.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_pin = ctk.CTkFrame(card_pin, fg_color="transparent")
        frame_pin.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkButton(
            frame_pin, text="Generar PIN",
            font=("JetBrains Mono", 12, "bold"),
            fg_color="#9B59B6", hover_color="#8E44AD",
            text_color=TEXTO_PRINCIPAL, width=120, height=38, corner_radius=8,
            command=self._generar_pin,
        ).pack(side="left")

        # Caja que muestra el PIN generado (grande y visible)
        self.label_pin_resultado = ctk.CTkLabel(
            card_pin, text="",
            font=("JetBrains Mono", 22, "bold"),
            text_color="#9B59B6",
        )
        self.label_pin_resultado.pack(anchor="w", padx=20, pady=(8, 2))

        self.label_pin_aviso = ctk.CTkLabel(
            card_pin, text="",
            font=("JetBrains Mono", 10),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_pin_aviso.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN D: Contraseña personalizada ──
        card_custom = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_custom.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_custom, text="Contraseña personalizada",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_custom,
            text="El sistema mezcla tus caracteres para crear una contrasena fuerte.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_custom = ctk.CTkFrame(card_custom, fg_color="transparent")
        frame_custom.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_semilla_pw = ctk.CTkEntry(
            frame_custom, placeholder_text="Ej: ADEV1130$yasuo05 (min 8 chars)",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_semilla_pw.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_custom, text="Generar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=90, height=38, corner_radius=8,
            command=self._generar_personalizada,
        ).pack(side="right")

        self.label_custom_resultado = ctk.CTkLabel(
            card_custom, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_custom_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN E: Cambio manual ──
        card_manual = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_manual.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_manual, text="✏ Cambio manual",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_manual,
            text="La contrasena debe ser nivel 'Muy Fuerte' (>=80 pts). Se pedira la actual para confirmar.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        # Contraseña actual
        frame_manual_actual = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual_actual.pack(fill="x", padx=20, pady=(10, 2))

        ctk.CTkLabel(frame_manual_actual, text="Actual:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual_actual = ctk.CTkEntry(
            frame_manual_actual, placeholder_text="Contrasena actual",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8, show="•",
        )
        self.entry_manual_actual.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Nueva contraseña
        frame_manual = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual.pack(fill="x", padx=20, pady=(2, 2))

        ctk.CTkLabel(frame_manual, text="Nueva:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual = ctk.CTkEntry(
            frame_manual, placeholder_text="Nueva contrasena",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
        )
        self.entry_manual.pack(side="left", fill="x", expand=True, padx=(5, 10))

        # Repetir contraseña
        frame_manual_repetir = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual_repetir.pack(fill="x", padx=20, pady=(2, 5))

        ctk.CTkLabel(frame_manual_repetir, text="Repetir:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_manual_repetir = ctk.CTkEntry(
            frame_manual_repetir, placeholder_text="Repetir nueva contrasena",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=36, corner_radius=8,
        )
        self.entry_manual_repetir.pack(side="left", fill="x", expand=True, padx=(5, 10))

        ctk.CTkButton(
            frame_manual_repetir, text="Cambiar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_EXITO, hover_color=BOTON_EXITO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=38, corner_radius=8,
            command=self._cambiar_manual,
        ).pack(side="right")

        # Indicador de fortaleza en tiempo real
        self.label_fortaleza_tiempo = ctk.CTkLabel(
            card_manual, text="Escribe tu contrasena...",
            font=("JetBrains Mono", 10), text_color=TEXTO_SECUNDARIO,
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
            card_manual, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_manual_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN D: Exportar JSON ──
        card_export = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_export.pack(fill="x")

        ctk.CTkLabel(
            card_export, text="💾 Exportar a JSON encriptado",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_export,
            text="Genera un archivo .enc con tu contraseña (solo legible por la app).",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        ctk.CTkButton(
            card_export, text="Exportar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
            command=self._exportar,
        ).pack(anchor="w", padx=20, pady=(10, 15))

        self.label_export_resultado = ctk.CTkLabel(
            card_export, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_export_resultado.pack(anchor="w", padx=20, pady=(0, 15))

    def _generar_pin(self):
        """Genera un nuevo PIN de 6 dígitos para hoy y lo muestra UNA sola vez."""
        try:
            from src.auth.pin_diario import generar_pin_diario, eliminar_pin_diario
            uid = str(self.usuario['_id'])
            
            # Primero eliminar cualquier PIN existente para poder generar uno nuevo
            eliminar_pin_diario(uid)
            
            pin = generar_pin_diario(uid)

            if pin is not None:
                # PIN recién generado: mostrarlo en grande
                self.label_pin_resultado.configure(
                    text=pin,
                    text_color="#9B59B6",
                )
                self.label_pin_aviso.configure(
                    text="⚠ Guárdalo ahora — no se volverá a mostrar. Úsalo en 'Ver contraseña'.",
                    text_color=AVISO,
                )
            else:
                # Ya existe PIN para hoy, no recuperable
                self.label_pin_resultado.configure(
                    text="Ya tienes un PIN para hoy",
                    text_color=AVISO,
                )
                self.label_pin_aviso.configure(
                    text="El PIN se generó al iniciar sesión. Solo hay uno por día.",
                    text_color=TEXTO_SECUNDARIO,
                )
        except Exception as e:
            self.label_pin_resultado.configure(text=str(e), text_color=PELIGRO)
            self.label_pin_aviso.configure(text="", text_color=TEXTO_SECUNDARIO)

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
        except Exception:  # nosec
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
        """Genera contraseña segura usando la semilla introducida por el usuario."""
        semilla = self.entry_semilla_reg.get().strip()
        if len(semilla) < 8:
            self.label_reg_resultado.configure(
                text="Mínimo 8 caracteres en la semilla", text_color=PELIGRO
            )
            return
        
        # Confirmar antes de cambiar
        import customtkinter as ctk
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Confirmar")
        dialogo.geometry("350x150")
        dialogo.transient(self)
        dialogo.grab_set()
        
        ctk.CTkLabel(
            dialogo,
            text="¿Generar nueva contraseña segura?\nEsto modificará tu contraseña actual.",
            font=("JetBrains Mono", 12),
        ).pack(pady=20)
        
        def confirmar():
            self._guardar_contraseña_segura(semilla, dialogo)
        
        ctk.CTkButton(
            dialogo, text="Sí, generar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_PELIGRO, hover_color=BOTON_PELIGRO_HOVER,
            command=confirmar,
        ).pack(side="left", padx=20, pady=10)
        
        ctk.CTkButton(
            dialogo, text="Cancelar",
            font=("JetBrains Mono", 12),
            command=dialogo.destroy,
        ).pack(side="right", padx=20, pady=10)

    def _guardar_contraseña_segura(self, semilla, dialogo=None):
        """Guarda la contraseña segura generada."""
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

            self.label_reg_resultado.configure(
                text=f"Contraseña segura generada: {pw}", text_color=COMPLETADO,
            )
            self.entry_semilla_reg.delete(0, "end")
            if dialogo:
                dialogo.destroy()
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
            self.entry_manual_repetir.delete(0, "end")
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