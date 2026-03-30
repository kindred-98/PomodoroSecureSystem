"""
tests/generador/test_detectar_patrones/test_secuencias.py
Tests de detección de secuencias débiles
"""

import pytest
from src.generador import detectar_patrones


class TestSecuenciaConsecutiva:
    """Tests de detección de secuencias consecutivas"""
    
    def test_detecta_abc(self):
        """Test: Detecta secuencia 'abc'"""
        resultado = detectar_patrones("abcdef12345")
        assert resultado['tiene_secuencias_consecutivas']
        assert 'abc' in resultado['secuencias_encontradas']
    
    def test_detecta_123(self):
        """Test: Detecta secuencia '123'"""
        resultado = detectar_patrones("abc123xyz")
        assert resultado['tiene_secuencias_consecutivas']
        assert '123' in resultado['secuencias_encontradas']
    
    def test_detecta_ABC(self):
        """Test: Detecta secuencia 'ABC' en mayúsculas"""
        resultado = detectar_patrones("ABCXYZ")
        assert resultado['tiene_secuencias_consecutivas']
        assert 'ABC' in resultado['secuencias_encontradas']
    
    def test_no_detecta_sin_secuencias(self):
        """Test: No detecta sin secuencias"""
        resultado = detectar_patrones("aXbY1Z2")
        assert not resultado['tiene_secuencias_consecutivas']
    
    def test_contraseña_fuerte_sin_secuencias(self):
        """Test: Contraseña fuerte obtiene alta fortaleza"""
        resultado = detectar_patrones("Xy9!Zw8@Vb7#")
        assert resultado['fortaleza_patron'] >= 0.9


class TestRepeticiones:
    """Tests de detección de caracteres repetidos"""
    
    def test_detecta_aaa(self):
        """Test: Detecta repetición 'aaa'"""
        resultado = detectar_patrones("aaabcd")
        assert resultado['tiene_repeticiones']
        assert 'aaa' in resultado['repeticiones_encontradas']
    
    def test_detecta_111(self):
        """Test: Detecta repetición '111'"""
        resultado = detectar_patrones("abc111xyz")
        assert resultado['tiene_repeticiones']
        assert '111' in resultado['repeticiones_encontradas']
    
    def test_no_detecta_aa(self):
        """Test: No detecta dos repeticiones (necesita 3)"""
        resultado = detectar_patrones("aabbc")
        assert not resultado['tiene_repeticiones']
    
    def test_detecta_multiples_repeticiones(self):
        """Test: Detecta múltiples repeticiones en una contraseña"""
        resultado = detectar_patrones("aaa111bbb")
        assert resultado['tiene_repeticiones']
        assert len(resultado['repeticiones_encontradas']) >= 2


class TestPatronesCrecientes:
    """Tests de detención de patrones crecientes"""
    
    def test_detecta_abcd(self):
        """Test: Detecta patrón creciente 'abcd'"""
        resultado = detectar_patrones("xyzabcdqwe")
        assert resultado['tiene_patrones_crecientes']
        assert 'abcd' in resultado['patrones_crecientes']
    
    def test_detecta_1234(self):
        """Test: Detecta patrón creciente '1234'"""
        resultado = detectar_patrones("aa1234zz")
        assert resultado['tiene_patrones_crecientes']
        assert '1234' in resultado['patrones_crecientes']
    
    def test_no_detecta_sin_crecientes(self):
        """Test: No detecta sin patrones crecientes"""
        resultado = detectar_patrones("Xy9!ZaBc")
        assert not resultado['tiene_patrones_crecientes']


class TestPatronesInvertidos:
    """Tests de detección de patrones invertidos"""
    
    def test_detecta_dcba(self):
        """Test: Detecta patrón invertido 'dcba'"""
        resultado = detectar_patrones("abcdcbaxyz")
        assert resultado['tiene_patrones_invertidos']
        assert 'dcba' in resultado['patrones_invertidos']
    
    def test_detecta_4321(self):
        """Test: Detecta patrón invertido '4321'"""
        resultado = detectar_patrones("aa4321zz")
        assert resultado['tiene_patrones_invertidos']
        assert '4321' in resultado['patrones_invertidos']
    
    def test_no_detecta_sin_invertidos(self):
        """Test: No detecta sin patrones invertidos"""
        resultado = detectar_patrones("Xy9!ZaBc")
        assert not resultado['tiene_patrones_invertidos']
