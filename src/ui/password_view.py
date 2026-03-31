"""
Módulo: password_view.py
Responsabilidad: Gestión de contraseña del usuario (ver, regenerar, cambiar, exportar).
"""

import customtkinter as ctk
from ..config.colores import *


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

        # Contenido
        contenido = ctk.CTkFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)

        # ── OPCIÓN A: Ver contraseña ──
        card_ver = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_ver.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_ver, text="👁 Ver contraseña actual",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_ver,
            text="Introduce tu contraseña de login para verificar tu identidad.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_ver = ctk.CTkFrame(card_ver, fg_color="transparent")
        frame_ver.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_ver = ctk.CTkEntry(
            frame_ver, placeholder_text="Contraseña de login", show="•",
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

        # ── OPCIÓN B: Regenerar contraseña ──
        card_reg = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_reg.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_reg, text="🔄 Regenerar contraseña",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_reg,
            text="Genera una nueva contraseña con parámetros diferentes.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        ctk.CTkButton(
            card_reg, text="Regenerar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
            command=self._regenerar,
        ).pack(anchor="w", padx=20, pady=(10, 15))

        self.label_reg_resultado = ctk.CTkLabel(
            card_reg, text="", font=("JetBrains Mono", 12),
            text_color=COMPLETADO,
        )
        self.label_reg_resultado.pack(anchor="w", padx=20, pady=(0, 15))

        # ── OPCIÓN C: Cambio manual ──
        card_manual = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        card_manual.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            card_manual, text="✏ Cambio manual",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card_manual,
            text="La contraseña debe ser nivel 'Muy Fuerte' (≥80 puntos).",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        frame_manual = ctk.CTkFrame(card_manual, fg_color="transparent")
        frame_manual.pack(fill="x", padx=20, pady=(10, 15))

        self.entry_manual = ctk.CTkEntry(
            frame_manual, placeholder_text="Nueva contraseña",
            font=("JetBrains Mono", 13), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, height=38, corner_radius=8,
        )
        self.entry_manual.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            frame_manual, text="Cambiar",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_EXITO, hover_color=BOTON_EXITO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=38, corner_radius=8,
            command=self._cambiar_manual,
        ).pack(side="right")

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

    def _ver_contraseña(self):
        pw = self.entry_ver.get()
        if not pw:
            self.label_ver_resultado.configure(text="Introduce tu contraseña", text_color=PELIGRO)
            return
        try:
            from ..auth import ver_contraseña
            resultado = ver_contraseña(str(self.usuario['_id']), pw)
            self.label_ver_resultado.configure(
                text=f"Tu contraseña: {resultado}", text_color=COMPLETADO
            )
        except Exception as e:
            self.label_ver_resultado.configure(text=str(e), text_color=PELIGRO)

    def _regenerar(self):
        try:
            from ..auth import regenerar_contraseña
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

    def _cambiar_manual(self):
        pw = self.entry_manual.get()
        if not pw:
            self.label_manual_resultado.configure(
                text="Introduce una contraseña", text_color=PELIGRO
            )
            return
        try:
            from ..auth import cambiar_contraseña
            resultado = cambiar_contraseña(str(self.usuario['_id']), pw)
            self.label_manual_resultado.configure(
                text=resultado['mensaje'], text_color=COMPLETADO
            )
        except Exception as e:
            self.label_manual_resultado.configure(text=str(e), text_color=PELIGRO)

    def _exportar(self):
        try:
            from ..auth import exportar_contraseña
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
