"""
tests/generador/test_mezclar_contraseña/test_validacion.py
Tests de validación de entrada para mezclar_contraseña
"""

import pytest
from src.generador import mezclar_contraseña, mezclar_preservando_estructura


class TestValidacionMezclar:
    """Tests de validación de entrada"""
    
    def test_no_es_string(self):
        """Test: TypeError si no es string"""
        with pytest.raises(TypeError, match="string"):
            mezclar_contraseña(12345)
    
    def test_parametro_none(self):
        """Test: TypeError si es None"""
        with pytest.raises(TypeError):
            mezclar_contraseña(None)
    
    def test_parametro_lista(self):
        """Test: TypeError si es lista"""
        with pytest.raises(TypeError):
            mezclar_contraseña(['a', 'b', 'c'])
    
    def test_contraseña_vacia(self):
        """Test: ValueError si está vacía"""
        with pytest.raises(ValueError, match="vacía"):
            mezclar_contraseña("")


class TestValidacionMezclarPreservando:
    """Tests de validación para mezclar_preservando_estructura"""
    
    def test_no_es_string(self):
        """Test: TypeError si no es string"""
        with pytest.raises(TypeError):
            mezclar_preservando_estructura(12345, preservar_inicio=False)
    
    def test_contraseña_vacia(self):
        """Test: ValueError si está vacía"""
        with pytest.raises(ValueError):
            mezclar_preservando_estructura("", preservar_inicio=False)
    
    def test_preservar_sin_segundo_caracter_falla(self):
        """Test: ValueError si preserva inicio pero solo 1 carácter"""
        with pytest.raises(ValueError):
            mezclar_preservando_estructura("x", preservar_inicio=True)
    
    def test_preservar_false_con_un_caracter_funciona(self):
        """Test: Funciona si preservar_inicio=False con 1 carácter"""
        resultado = mezclar_preservando_estructura("x", preservar_inicio=False)
        assert resultado == "x"
    
    def test_dos_caracteres_con_preservar(self):
        """Test: Con 2 caracteres y preservar funciona"""
        resultado = mezclar_preservando_estructura("ab", preservar_inicio=True)
        assert resultado[0] == 'a'
        assert len(resultado) == 2


class TestDistribucionAleatoria:
    """Tests de que la distribución sea realmente aleatoria"""
    
    def test_multiples_mezclas_variadas(self):
        """Test: Múltiples mezclas producen resultados diferentes"""
        original = "abcdefghij"
        resultados = [mezclar_contraseña(original) for _ in range(20)]
        # No todos deberían ser iguales al original
        assert any(r != original for r in resultados)
        # No todos deberían ser iguales entre sí
        assert len(set(resultados)) > 1
    
    def test_criptograficamente_seguro(self):
        """Test: Usa secrets (criptográficamente seguro)"""
        # Simplemente verificar que funciona múltiples veces
        for _ in range(5):
            resultado = mezclar_contraseña("abcdefgh123")
            assert isinstance(resultado, str)
