"""Tests para seguridad/encriptacion.py"""

import pytest
from unittest.mock import patch
from src.seguridad.encriptacion import (
    hashear_contraseña,
    verificar_contraseña,
    cifrar,
    descifrar,
    generar_token_sesion,
)


class TestHashearContraseña:
    """Tests para hashear_contraseña"""
    
    def test_genera_hash_bcrypt(self):
        """Hash debe empezar con $2b$ (formato bcrypt)"""
        hash_resultado = hashear_contraseña("MiContraseña123!")
        assert hash_resultado.startswith("$2b$")
    
    def test_hashes_son_diferentes(self):
        """Cada hash debe ser diferente (salt único)"""
        h1 = hashear_contraseña("Igual123!")
        h2 = hashear_contraseña("Igual123!")
        assert h1 != h2
    
    def test_no_es_string_lanza_error(self):
        """Debe fallar si contraseña no es string"""
        with pytest.raises(TypeError, match="contraseña debe ser string"):
            hashear_contraseña(12345)
    
    def test_vacia_lanza_error(self):
        """Debe fallar si contraseña está vacía"""
        with pytest.raises(ValueError, match="no puede estar vacía"):
            hashear_contraseña("")


class TestVerificarContraseña:
    """Tests para verificar_contraseña"""
    
    def test_contraseña_correcta(self):
        """Debe retornar True para contraseña correcta"""
        pw = "TestSegura123!"
        hash_pw = hashear_contraseña(pw)
        assert verificar_contraseña(pw, hash_pw) is True
    
    def test_contraseña_incorrecta(self):
        """Debe retornar False para contraseña incorrecta"""
        hash_pw = hashear_contraseña("Correcta123!")
        assert verificar_contraseña("Incorrecta456!", hash_pw) is False
    
    def test_tipo_invalido_retorna_false(self):
        """Debe retornar False si tipos no son string"""
        assert verificar_contraseña(123, "hash") is False
        assert verificar_contraseña("pw", 123) is False
    
    def test_hash_invalido_retorna_false(self):
        """Debe retornar False si hash no es válido"""
        assert verificar_contraseña("pw", "no_es_hash") is False


class TestCifrarDescifrar:
    """Tests para cifrar y descifrar"""
    
    def test_cifrar_descifrar_roundtrip(self, fernet_key_env):
        """Cifrar y descifrar debe retornar el texto original"""
        texto = "contraseña_secreta_123!"
        cifrado = cifrar(texto)
        descifrado = descifrar(cifrado)
        assert descifrado == texto
    
    def test_cifrado_es_diferente(self, fernet_key_env):
        """Cada cifrado debe ser diferente (IV aleatorio)"""
        texto = "mismo_texto"
        c1 = cifrar(texto)
        c2 = cifrar(texto)
        assert c1 != c2
        assert descifrar(c1) == descifrar(c2) == texto
    
    def test_cifrar_no_string_lanza_error(self, fernet_key_env):
        """Debe fallar si texto no es string"""
        with pytest.raises(TypeError, match="texto debe ser string"):
            cifrar(123)
    
    def test_cifrar_vacio_lanza_error(self, fernet_key_env):
        """Debe fallar si texto está vacío"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            cifrar("")
    
    def test_sin_fernet_key_lanza_error(self):
        """Debe fallar si FERNET_KEY no está configurada"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="FERNET_KEY no configurada"):
                cifrar("test")
    
    def test_descifrar_texto_invalido(self, fernet_key_env):
        """Debe fallar si texto cifrado es inválido"""
        with pytest.raises(ValueError, match="Error al descifrar"):
            descifrar("texto_invalido_no_es_fernet")
    
    def test_descifrar_no_string(self, fernet_key_env):
        """Debe fallar si texto_cifrado no es string"""
        with pytest.raises(TypeError, match="texto_cifrado debe ser string"):
            descifrar(123)
    
    def test_descifrar_vacio(self, fernet_key_env):
        """Debe fallar si texto_cifrado está vacío"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            descifrar("")


class TestGenerarTokenSesion:
    """Tests para generar_token_sesion"""
    
    def test_longitud_correcta(self):
        """Token debe tener 64 caracteres hex"""
        token = generar_token_sesion()
        assert len(token) == 64
    
    def test_solo_hex(self):
        """Token debe ser solo caracteres hexadecimales"""
        token = generar_token_sesion()
        assert all(c in '0123456789abcdef' for c in token)
    
    def test_tokens_son_unicos(self):
        """Tokens consecutivos deben ser diferentes"""
        t1 = generar_token_sesion()
        t2 = generar_token_sesion()
        assert t1 != t2
