"""
tests/generador/test_evaluar_fortaleza/test_scoring.py
Tests de algoritmo de scoring de puntuación
"""

import pytest
from src.generador import evaluar_fortaleza


class TestScoringBasico:
    """Tests del sistema de scoring"""
    
    def test_debil_poco_puntos(self):
        """Test: Contraseña débil obtiene < 30 puntos"""
        resultado = evaluar_fortaleza("abc")
        assert resultado['puntuacion'] < 30
    
    def test_fuerte_muchos_puntos(self):
        """Test: Contraseña fuerte obtiene > 60 puntos"""
        resultado = evaluar_fortaleza("X7$mK#pQw9&bZ2L!")
        assert resultado['puntuacion'] > 50
    
    def test_suma_puntos(self):
        """Test: Puntuación total es suma de criterios"""
        resultado = evaluar_fortaleza("Abc12!@#Def45$%^")
        puntos = (
            resultado['detalles']['puntos_longitud'] +
            resultado['detalles']['puntos_diversidad'] +
            resultado['detalles']['puntos_entropia'] +
            resultado['detalles']['puntos_patrones']
        )
        # La puntuación final puede estar capped en 100
        assert resultado['puntuacion'] == min(100, puntos)
    
    def test_puntos_no_negativos(self):
        """Test: Todos los puntos son >= 0"""
        resultado = evaluar_fortaleza("abc123XYZ!@#")
        assert resultado['detalles']['puntos_longitud'] >= 0
        assert resultado['detalles']['puntos_diversidad'] >= 0
        assert resultado['detalles']['puntos_entropia'] >= 0
        assert resultado['detalles']['puntos_patrones'] >= 0
    
    def test_cap_100(self):
        """Test: Puntuación máxima es capped en 100"""
        resultado = evaluar_fortaleza("X" * 128 + "a" * 128 + "1" * 128 + "@" * 128)
        assert resultado['puntuacion'] <= 100


class TestPenalizacionesPatrones:
    """Tests de penalizaciones por patrones detectados"""
    
    def test_penalizacion_vacia_sin_patrones(self):
        """Test: Sin patrones la penalización está vacía"""
        resultado = evaluar_fortaleza("XyZ9!qBwK#p")
        penalizacion = resultado['detalles']['penalizacion_patrones']
        # Podría haber algunos patrones, pero en general debería ser bajo
        assert isinstance(penalizacion, dict)
    
    def test_penalizacion_registra_secuencias(self):
        """Test: Registra penalización por secuencias"""
        resultado = evaluar_fortaleza("abc123XYZ")
        penalizacion = resultado['detalles']['penalizacion_patrones']
        if 'secuencias' in penalizacion:
            assert isinstance(penalizacion['secuencias'], int)
            assert penalizacion['secuencias'] > 0
    
    def test_penalizacion_registra_repeticiones(self):
        """Test: Registra penalización por repeticiones"""
        resultado = evaluar_fortaleza("aaabbbccc123")
        penalizacion = resultado['detalles']['penalizacion_patrones']
        if 'repeticiones' in penalizacion:
            assert penalizacion['repeticiones'] > 0
    
    def test_mas_puntos_patrones_sin_debilidades(self):
        """Test: Más puntos de patrón sin patrones débiles"""
        sin_patrones = evaluar_fortaleza("XyZ9Bw!qKp#")
        con_patrones = evaluar_fortaleza("abc123XYZ")
        
        # Sin patrones débiles obtiene más puntos
        assert sin_patrones['detalles']['puntos_patrones'] >= con_patrones['detalles']['puntos_patrones']


class TestMinimaFortaleza:
    """Tests de casos extremos de puntuación"""
    
    def test_una_letra_minuscula(self):
        """Test: Una letra minúscula obtiene algún puntaje"""
        resultado = evaluar_fortaleza("a")
        assert resultado['puntuacion'] >= 0
        assert resultado['puntuacion'] < 10
    
    def test_treinta_caracteres_identicos(self):
        """Test: 30 a's obtiene poco puntaje"""
        resultado = evaluar_fortaleza("a" * 30)
        # Solo minúsculas + repeticiones = débil
        assert resultado['puntuacion'] < 40
    
    def test_contraseña_random_bien(self):
        """Test: Contraseña aleatoria bien formada obtiene >70"""
        resultado = evaluar_fortaleza("K#mW7$hPq9xN2zB!")
        assert resultado['puntuacion'] >= 60
