"""Tests para generar_contraseña_personalizada."""

import pytest


class TestGenerarContraseñaPersonalizada:
    """Tests para función generar_contraseña_personalizada."""

    def test_tipo_invalido(self):
        """Tipo inválido lanza TypeError."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        with pytest.raises(TypeError):
            generar_contraseña_personalizada(123)
        
        with pytest.raises(TypeError):
            generar_contraseña_personalizada(None)
        
        with pytest.raises(TypeError):
            generar_contraseña_personalizada(['abc'])

    def test_vacia(self):
        """Semilla vacía lanza ValueError."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        with pytest.raises(ValueError):
            generar_contraseña_personalizada("")

    def test_muy_corta(self):
        """Semilla muy corta lanza ValueError."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        with pytest.raises(ValueError):
            generar_contraseña_personalizada("abc")

    def test_pocos_unicos(self):
        """Semilla con pocos únicos lanza ValueError."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        with pytest.raises(ValueError):
            generar_contraseña_personalizada("aaaa")

    def test_longitud_personalizada(self):
        """Longitud personalizada."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        resultado = generar_contraseña_personalizada("abcd1234efgh5678", longitud=20)
        assert len(resultado) == 20

    def test_solo_usa_caracteres_semilla(self):
        """Solo usa caracteres de la semilla."""
        from src.generador.generar_contraseña import generar_contraseña_personalizada
        
        semilla = "abcd1234"  # 4 letras + 4 números únicos mínimos
        resultado = generar_contraseña_personalizada(semilla)
        
        for char in resultado:
            assert char in semilla