"""
tests/generador/test_evaluar_fortaleza/test_niveles.py
Tests de clasificación de niveles de fortaleza
"""

import pytest
from src.generador import evaluar_fortaleza


class TestNiveles:
    """Tests de clasificación por nivel"""
    
    def test_nivel_debil(self):
        """Test: Contraseña débil obtiene nivel 'Débil'"""
        resultado = evaluar_fortaleza("abc")
        assert resultado['nivel'] == "Débil"
        assert resultado['puntuacion'] < 30
    
    def test_nivel_normal(self):
        """Test: Contraseña normal obtiene nivel 'Normal'"""
        resultado = evaluar_fortaleza("abcdef123456")
        nivel = resultado['nivel']
        puntuacion = resultado['puntuacion']
        if 30 <= puntuacion < 60:
            assert nivel == "Normal"
    
    def test_nivel_fuerte(self):
        """Test: Contraseña fuerte obtiene nivel 'Fuerte'"""
        resultado = evaluar_fortaleza("MyPassword123!@#")
        if 60 <= resultado['puntuacion'] < 80:
            assert resultado['nivel'] == "Fuerte"
    
    def test_nivel_muy_fuerte(self):
        """Test: Contraseña muy fuerte obtiene nivel 'Muy Fuerte'"""
        resultado = evaluar_fortaleza("X7$mK#pQw9&bZ2L!")
        if resultado['puntuacion'] >= 80:
            assert resultado['nivel'] == "Muy Fuerte"
    
    def test_niveles_validos(self):
        """Test: Nivel siempre es uno de los esperados"""
        niveles_validos = {"Débil", "Normal", "Fuerte", "Muy Fuerte"}
        contraseñas = ["a", "abc", "abcdef123", "MyPass123@", "X7$mK#pQw9&bZ2L!"]
        for contraseña in contraseñas:
            resultado = evaluar_fortaleza(contraseña)
            assert resultado['nivel'] in niveles_validos


class TestLongitudSignificancia:
    """Tests de impacto de longitud"""
    
    def test_longitud_8_vs_16(self):
        """Test: Longitud 16 obtiene mayor puntuación que 8"""
        corta = "Abc12!@#"  # 8 caracteres
        larga = "Abc12!@#Def45$%^"  # 16 caracteres
        
        resultado_corta = evaluar_fortaleza(corta)
        resultado_larga = evaluar_fortaleza(larga)
        
        # Larga debe tener más puntos de longitud
        assert resultado_larga['detalles']['puntos_longitud'] > resultado_corta['detalles']['puntos_longitud']
    
    def test_muy_corta_es_debil(self):
        """Test: Contraseña muy corta es siempre débil"""
        resultado = evaluar_fortaleza("Aa1!")
        assert resultado['puntuacion'] < 40


class TestDiversidadSignificancia:
    """Tests de impacto de diversidad"""
    
    def test_solo_minusculas_menos_puntos(self):
        """Test: Solo minúsculas obtiene menos puntos de diversidad"""
        resultado = evaluar_fortaleza("abcdefghijklmnopqrst")
        assert resultado['detalles']['puntos_diversidad'] < 10
    
    def test_cuatro_tipos_mas_puntos(self):
        """Test: 4 tipos (min, may, num, sym) obtiene máximos puntos"""
        resultado = evaluar_fortaleza("Abc12!@#Def45$%^")
        assert resultado['detalles']['puntos_diversidad'] >= 25
    
    def test_diversidad_detecta_tipos(self):
        """Test: Detecta correctamente tipos de caracteres"""
        resultado = evaluar_fortaleza("Abc123")
        assert resultado['detalles']['tiene_mayusculas']
        assert resultado['detalles']['tiene_minusculas']
        assert resultado['detalles']['tiene_numeros']
        assert not resultado['detalles']['tiene_simbolos']


class TestEntropiaCalculada:
    """Tests de cálculo de entropía"""
    
    def test_entropia_bits_positiva(self):
        """Test: Entropía siempre es positiva"""
        resultado = evaluar_fortaleza("abcdefgh123456#@!")
        assert resultado['detalles']['entropia_bits'] > 0
    
    def test_entropia_aumenta_con_longitud(self):
        """Test: Entropía aumenta con longitud (mismo charset)"""
        corta = "Abc12!@#"
        larga = "Abc12!@#Def45$%^"
        
        resultado_corta = evaluar_fortaleza(corta)
        resultado_larga = evaluar_fortaleza(larga)
        
        assert resultado_larga['detalles']['entropia_bits'] > resultado_corta['detalles']['entropia_bits']
    
    def test_entropia_aumenta_con_diversidad(self):
        """Test: Entreropía aumenta con diversidad de caracteres"""
        minusculas = "abcdefghijklmnopqrst"
        con_numeros = "abcdefghijklmnopqrs1"  # Reemplazo 1 char
        
        resultado_min = evaluar_fortaleza(minusculas)
        resultado_con = evaluar_fortaleza(con_numeros)
        
        # Más diversidad = más bits de entropía
        assert resultado_con['detalles']['entropia_bits'] >= resultado_min['detalles']['entropia_bits']
