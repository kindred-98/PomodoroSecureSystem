"""Tests para generar_contraseña_personalizada."""

import pytest

from src.generador.generar_contrasena import generar_contrasena_personalizada


class TestGenerarContrasenaPersonalizada:
    """Tests para función generar_contraseña_personalizada."""

    @pytest.mark.parametrize("semilla", [123, None, ['abc']])
    def test_tipo_invalido(self, semilla):
        """Tipo inválido lanza TypeError."""
        with pytest.raises(TypeError):
            generar_contrasena_personalizada(semilla)

    def test_vacia(self):
        """Semilla vacía lanza ValueError."""
        from src.generador.generar_contrasena import generar_contrasena_personalizada
        
        with pytest.raises(ValueError):
            generar_contrasena_personalizada("")

    def test_muy_corta(self):
        """Semilla muy corta lanza ValueError."""
        from src.generador.generar_contrasena import generar_contrasena_personalizada
        
        with pytest.raises(ValueError):
            generar_contrasena_personalizada("abc")

    def test_pocos_unicos(self):
        """Semilla con pocos únicos lanza ValueError."""
        from src.generador.generar_contrasena import generar_contrasena_personalizada
        
        with pytest.raises(ValueError):
            generar_contrasena_personalizada("aaaa")

    def test_longitud_personalizada(self):
        """Longitud personalizada."""
        from src.generador.generar_contrasena import generar_contrasena_personalizada
        
        resultado = generar_contrasena_personalizada("abcd1234efgh5678", longitud=20)
        assert len(resultado) == 20

    def test_solo_usa_caracteres_semilla(self):
        """Solo usa caracteres de la semilla."""
        from src.generador.generar_contrasena import generar_contrasena_personalizada
        
        semilla = "abcd1234"  # 4 letras + 4 números únicos mínimos
        resultado = generar_contrasena_personalizada(semilla)
        
        for char in resultado:
            assert char in semilla