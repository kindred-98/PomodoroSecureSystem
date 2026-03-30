"""
tests/generador/test_generador_completo.py
Tests completos para el módulo de generación de contraseñas
Cobertura: generar_contraseña(), asegurar_tipos_caracteres()
"""

import pytest
from src.generador import generar_contraseña, asegurar_tipos_caracteres


# ====================
# TESTS - generar_contraseña
# ====================

class TestGenerarContraseña:
    """Tests para la función generar_contraseña"""
    
    def test_genera_con_longitud_correcta(self, parametros_generador_defecto):
        """Test: La contraseña generada tiene la longitud especificada"""
        contraseña = generar_contraseña(parametros_generador_defecto)
        assert len(contraseña) == parametros_generador_defecto["longitud"]
    
    def test_genera_con_longitud_8(self):
        """Test: Genera contraseña con longitud mínima (8)"""
        parametros = {
            "longitud": 8,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 8
    
    def test_genera_con_longitud_128(self):
        """Test: Genera contraseña con longitud máxima (128)"""
        parametros = {
            "longitud": 128,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 128
    
    def test_rechaza_longitud_menor_8(self):
        """Test: Rechaza longitud menor a 8"""
        parametros = {
            "longitud": 7,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_mayor_128(self):
        """Test: Rechaza longitud mayor a 128"""
        parametros = {
            "longitud": 129,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_genera_con_mayusculas(self):
        """Test: Incluye mayúsculas cuando se especifica"""
        parametros = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isupper() for c in contraseña)
    
    def test_genera_con_numeros(self):
        """Test: Incluye números cuando se especifica"""
        parametros = {
            "longitud": 20,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isdigit() for c in contraseña)
    
    def test_genera_con_simbolos(self):
        """Test: Incluye símbolos cuando se especifica"""
        parametros = {
            "longitud": 30,
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        import string
        simbolos = set(string.punctuation)
        assert any(c in simbolos for c in contraseña)
    
    def test_genera_solo_minusculas(self, parametros_generador_solo_minusculas):
        """Test: Sin flags, genera solo minúsculas"""
        contraseña = generar_contraseña(parametros_generador_solo_minusculas)
        assert contraseña.islower()
    
    def test_genera_contraseña_es_string(self, parametros_generador_defecto):
        """Test: El resultado es siempre string"""
        contraseña = generar_contraseña(parametros_generador_defecto)
        assert isinstance(contraseña, str)
    
    def test_rechaza_parametros_no_dict(self):
        """Test: Rechaza entrada que no es dict"""
        with pytest.raises(TypeError):
            generar_contraseña("no es dict")
    
    def test_rechaza_parametros_faltantes(self):
        """Test: Rechaza si faltan claves en dict"""
        parametros = {"longitud": 12}  # Faltan muchas claves
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_excluye_caracteres_ambiguos(self):
        """Test: Excluye 0,O,l,I,1 cuando se especifica"""
        parametros = {
            "longitud": 100,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        caracteres_ambiguos = "0Ol1I"
        for caracter in caracteres_ambiguos:
            assert caracter not in contraseña
    
    def test_determinismo_no_existe(self, parametros_generador_defecto):
        """Test: Genera contraseñas distintas cada vez (aleatoriedad)"""
        contraseña1 = generar_contraseña(parametros_generador_defecto)
        contraseña2 = generar_contraseña(parametros_generador_defecto)
        # Muy improbable que genere dos iguales (1 entre 62^12)
        assert contraseña1 != contraseña2


# ====================
# TESTS - asegurar_tipos_caracteres
# ====================

class TestAsegurarTiposCaracteres:
    """Tests para la función asegurar_tipos_caracteres"""
    
    def test_asegura_mayuscula_en_posicion_0(self):
        """Test: Coloca mayúscula en posición 0 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
    
    def test_asegura_numero_en_posicion_1(self):
        """Test: Coloca número en posición 1 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[1].isdigit()
    
    def test_asegura_simbolo_en_posicion_2(self):
        """Test: Coloca símbolo en posición 2 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd', 'e']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True
        }
        import string
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[2] in string.punctuation
    
    def test_rechaza_lista_vacia(self):
        """Test: Rechaza lista vacía"""
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        with pytest.raises(ValueError):
            asegurar_tipos_caracteres([], parametros)
    
    def test_rechaza_no_lista(self):
        """Test: Rechaza entrada que no es lista"""
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        with pytest.raises(TypeError):
            asegurar_tipos_caracteres("no es lista", parametros)
    
    def test_maneja_lista_con_1_elemento(self):
        """Test: Maneja lista con 1 solo elemento"""
        contraseña = ['a']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        # Debe sobrescribir el único elemento con una mayúscula
        assert resultado[0].isupper()
    
    def test_maneja_lista_con_2_elementos(self):
        """Test: Maneja lista con 2 elementos"""
        contraseña = ['a', 'b']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
        assert resultado[1].isdigit()
    
    def test_rechaza_tipos_mas_queespacios(self):
        """Test: Rechaza si hay más tipos requeridos que espacio en lista"""
        contraseña = ['a']  # Solo 1 espacio
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True  # 3 tipos pero solo 1 espacio
        }
        with pytest.raises(ValueError):
            asegurar_tipos_caracteres(contraseña, parametros)
    
    def test_retorna_lista_misma_longitud(self):
        """Test: La lista resultante tiene la misma longitud"""
        contraseña = ['a', 'b', 'c', 'd', 'e']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert len(resultado) == len(contraseña)


# ====================
# TESTS - Parametrización
# ====================

class TestParametrizacion:
    """Tests parametrizados para múltiples casos"""
    
    def test_genera_multiples_longitudes(self, longitudes_validas):
        """Test parametrizado: Genera contraseñas con múltiples longitudes válidas"""
        parametros = {
            "longitud": longitudes_validas,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == longitudes_validas
    
    def test_rechaza_multiples_longitudes_invalidas(self, longitudes_invalidas):
        """Test parametrizado: Rechaza múltiples longitudes inválidas"""
        parametros = {
            "longitud": longitudes_invalidas,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)


# ====================
# TESTS - Stress
# ====================

class TestStress:
    """Tests de carga/stress para validar robustez"""
    
    def test_genera_50_contraseñas_sin_error(self, parametros_generador_defecto):
        """Test: Puede generar 50 contraseñas sin errores"""
        for _ in range(50):
            contraseña = generar_contraseña(parametros_generador_defecto)
            assert len(contraseña) == 12
    
    def test_todas_unicas_en_100_generaciones(self, parametros_generador_defecto):
        """Test: 100 generaciones produce contraseñas prácticamente todas únicas"""
        contraseñas = [generar_contraseña(parametros_generador_defecto) for _ in range(100)]
        unicidades = len(set(contraseñas))
        # Debería haber al menos 99 únicas de 100 (muy improbable colisión)
        assert unicidades >= 99
