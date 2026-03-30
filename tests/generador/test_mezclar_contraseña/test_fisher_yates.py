"""
tests/generador/test_mezclar_contraseña/test_fisher_yates.py
Tests del algoritmo Fisher-Yates shuffle
"""

import pytest
from src.generador import mezclar_contraseña


class TestFisherYatesShuffle:
    """Tests de implementación del algoritmo Fisher-Yates"""
    
    def test_shuffle_produce_permutacion_valida(self):
        """Test: El shuffle produce una permutación válida"""
        original = "abcdefghij"
        for _ in range(10):
            mezclada = mezclar_contraseña(original)
            assert sorted(original) == sorted(mezclada)
            assert len(original) == len(mezclada)
    
    def test_puede_mover_primer_elemento(self):
        """Test: No fija el primer elemento"""
        original = "aaaaabbbbb"
        resultados = set()
        for _ in range(50):
            resultado = mezclar_contraseña(original)
            resultados.add(resultado)
        # Con 50 iteraciones, probablemente vea cambios
        assert len(resultados) > 1
    
    def test_puede_mover_ultimo_elemento(self):
        """Test: No fija el último elemento"""
        original = "abcdefghij"
        ultimos = []
        for _ in range(30):
            resultado = mezclar_contraseña(original)
            ultimos.append(resultado[-1])
        # El último elemento no siempre debe ser 'j'
        assert 'j' not in ultimos or len(set(ultimos)) > 1


class TestCaracteresUnicos:
    """Tests con caracteres únicos y repetidos"""
    
    def test_todos_unicos(self):
        """Test: Shuffle de caracteres únicos"""
        original = "abcdefghij"
        resultado = mezclar_contraseña(original)
        assert len(set(resultado)) == len(set(original))
    
    def test_algunos_repetidos(self):
        """Test: Shuffle conserva repeticiones"""
        original = "aaabbbcccddd"
        resultado = mezclar_contraseña(original)
        assert resultado.count('a') == 3
        assert resultado.count('b') == 3
        assert resultado.count('c') == 3
        assert resultado.count('d') == 3
    
    def test_todos_iguales(self):
        """Test: Shuffle de todos caracteres iguales retorna lo mismo"""
        original = "aaaaaaaaaa"
        resultado = mezclar_contraseña(original)
        assert resultado == original


class TestLargoDelResultado:
    """Tests de largo de contraseña tras mezclar"""
    
    @pytest.mark.parametrize("longitud", [1, 5, 10, 50, 100, 128])
    def test_longitud_conservada(self, longitud):
        """Test: Longitud se conserva para diferentes tamaños"""
        original = "a" * longitud
        resultado = mezclar_contraseña(original)
        assert len(resultado) == longitud
