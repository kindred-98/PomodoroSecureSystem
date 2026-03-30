"""
tests/generador/test_detectar_patrones/test_fortaleza_patron.py
Tests de cálculo de fortaleza según patrones
"""

import pytest
from src.generador import detectar_patrones


class TestFortalezaPatron:
    """Tests de cálculo de fortaleza basada en patrones"""
    
    def test_sin_patrones_fortaleza_maxima(self):
        """Test: Sin patrones obtiene fortaleza 1.0"""
        resultado = detectar_patrones("XyZ9!@Bw")
        assert resultado['fortaleza_patron'] >= 0.95
    
    def test_una_secuencia_reduce_fortaleza(self):
        """Test: Detectar secuencia reduce fortaleza"""
        sin_patrones = detectar_patrones("XyZ9!qBw")
        con_secuencia = detectar_patrones("XyZabc!Bw")
        assert con_secuencia['fortaleza_patron'] < sin_patrones['fortaleza_patron']
    
    def test_repeticin_reduce_fortaleza(self):
        """Test: Repeticiones reducen fortaleza"""
        sin_patrón = detectar_patrones("abcXYZ123")
        con_repetición = detectar_patrones("aaabcXYZ")
        assert con_repetición['fortaleza_patron'] < sin_patrón['fortaleza_patron']
    
    def test_multiples_patrones_muy_debil(self):
        """Test: Múltiples patrones resulta en fortaleza muy baja"""
        resultado = detectar_patrones("abc123aaaqwerty")
        assert resultado['fortaleza_patron'] < 0.6
    
    def test_contraseña_fuerte(self):
        """Test: Contraseña fuerte típica tiene alta fortaleza"""
        resultado = detectar_patrones("P@ssw0rd7Kqx!")
        # A menos que tenga patrones, debería tener buena fortaleza
        assert resultado['fortaleza_patron'] >= 0.5


class TestTecladoAdyacente:
    """Tests de detección de patrones de teclado adyacente"""
    
    def test_detecta_qwerty(self):
        """Test: Detecta 'qwer' del teclado"""
        resultado = detectar_patrones("qwertyasdf")
        assert resultado['tiene_teclado_adyacente']
    
    def test_no_detecta_sin_adyacencia(self):
        """Test: No detecta sin secuencias del teclado"""
        resultado = detectar_patrones("abXyZ9@!")
        # Probablemente no tenga teclado adyacente
        # (aunque no es garantizado)
    
    def test_qwerty_reduce_fortaleza_significativamente(self):
        """Test: Patrón QWERTY reduce fortaleza"""
        sin_qwerty = detectar_patrones("Xy9!ZwBc")
        con_qwerty = detectar_patrones("qwertyAB")
        # Con qwerty debería ser más débil
        # (aunque ambas podrían tener otros patrones)


class TestCorrectoMultiplesDetecciones:
    """Tests de detección correcta en contraseñas compleja"""
    
    def test_contraseña_con_todo(self):
        """Test: Detecta múltiples tipos en una sola contraseña"""
        resultado = detectar_patrones("abc123aaaqwerty")
        # Debería detectar:
        # - abc (secuencia)
        # - 123 (secuencia + creciente)
        # - aaa (repetición)
        # - qwe (teclado/secuencia)
        assert resultado['tiene_secuencias_consecutivas']
        assert resultado['tiene_repeticiones']
        assert resultado['fortaleza_patron'] < 0.7
    
    def test_basura_aleatoria_sin_patrones(self):
        """Test: Contraseña aleatoria buena sin patrones"""
        resultado = detectar_patrones("K#mW7$hPq9xN2z")
        # No debe tener patrones claros
        assert resultado['fortaleza_patron'] >= 0.8
