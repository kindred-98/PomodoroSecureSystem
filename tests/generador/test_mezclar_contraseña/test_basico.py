"""
tests/generador/test_mezclar_contraseña/test_basico.py
Tests básicos de funcionalidad de mezclar_contraseña
"""

import pytest
from src.generador import mezclar_contraseña, mezclar_preservando_estructura


class TestMezclarContraseña:
    """Tests de funcionalidad básica de mezclar"""
    
    def test_contiene_mismos_caracteres(self):
        """Test: Contraseña mezclada tiene mismos caracteres"""
        original = "abcdef123"
        mezclada = mezclar_contraseña(original)
        assert sorted(original) == sorted(mezclada)
    
    def test_misma_longitud(self):
        """Test: Longitud se mantiene tras mezclar"""
        original = "abcdefghij123456"
        mezclada = mezclar_contraseña(original)
        assert len(original) == len(mezclada)
    
    def test_retorna_string(self):
        """Test: Retorna un string"""
        resultado = mezclar_contraseña("abcdef")
        assert isinstance(resultado, str)
    
    def test_probablemente_diferente(self):
        """Test: Probablemente el resultado sea diferente (con 99% probabilidad)"""
        original = "abcdefghij123456"
        resultados = set()
        for _ in range(10):
            resultados.add(mezclar_contraseña(original))
        # Con 10 iteraciones, debería tener al menos 2 diferentes
        assert len(resultados) >= 2
    
    def test_un_caracter(self):
        """Test: Mezcla de 1 carácter retorna el mismo"""
        resultado = mezclar_contraseña("a")
        assert resultado == "a"
    
    def test_dos_caracteres(self):
        """Test: Mezcla de 2 caracteres es válida"""
        original = "ab"
        resultado = mezclar_contraseña(original)
        assert len(resultado) == 2
        assert sorted(original) == sorted(resultado)


class TestMezclarPreservandoEstructura:
    """Tests de mezcla preservando estructura"""
    
    def test_preserva_primer_caracter(self):
        """Test: Primer carácter se preserva"""
        resultado = mezclar_preservando_estructura("abcdef123", preservar_inicio=True)
        assert resultado[0] == 'a'
    
    def test_cambia_resto(self):
        """Test: Resto de caracteres pueden cambiar"""
        original = "abcdefghij"
        mezclada = mezclar_preservando_estructura(original, preservar_inicio=True)
        # Primer carácter igual, pero posiblemente distinto orden del resto
        assert mezclada[0] == original[0]
        # Resto tiene mismos caracteres
        assert sorted(original[1:]) == sorted(mezclada[1:])
    
    def test_preservar_false_es_normal(self):
        """Test: preservar_inicio=False es equivalente a mezclar_contraseña"""
        original = "abcdefgh"
        resultado1 = mezclar_contraseña(original)
        resultado2 = mezclar_preservando_estructura(original, preservar_inicio=False)
        # Ambas pueden cambiar cualquier carácter
        assert len(resultado1) == len(resultado2)
        assert sorted(original) == sorted(resultado2)
    
    def test_falla_con_un_caracter_preservando(self):
        """Test: ValueError si intenta preservar con 1 carácter"""
        with pytest.raises(ValueError, match="al menos 2"):
            mezclar_preservando_estructura("a", preservar_inicio=True)
    
    def test_mantiene_conjunto_caracteres(self):
        """Test: El conjunto de caracteres se mantiene al preservar"""
        original = "Xy123!@#"
        resultado = mezclar_preservando_estructura(original, preservar_inicio=True)
        assert sorted(original) == sorted(resultado)
        assert resultado[0] == 'X'
