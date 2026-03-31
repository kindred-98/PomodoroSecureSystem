"""Tests para auth/regenerar_contraseña.py"""

import pytest
from bson import ObjectId
from src.auth.regenerar_contraseña import regenerar_contraseña


class TestRegenerarContraseñaValidacion:
    """Tests para validación en regenerar_contraseña"""
    
    def test_usuario_id_no_string(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            regenerar_contraseña(123, parametros_contraseña_defecto)
    
    def test_parametros_no_dict(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="nuevos_parametros debe ser dict"):
            regenerar_contraseña("id", "no_dict")
    
    def test_usuario_id_vacio(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            regenerar_contraseña("", parametros_contraseña_defecto)
    
    def test_usuario_id_invalido(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(ValueError, match="usuario_id inválido"):
            regenerar_contraseña("no_es_objectid", parametros_contraseña_defecto)


class TestRegenerarContraseñaExito:
    """Tests para regeneración exitosa"""
    
    def test_regeneracion_exitosa(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Debe regenerar contraseña con nuevos parámetros"""
        usr = usuario_registrado
        nuevos_params = {"longitud": 20, "usar_mayusculas": True,
                        "usar_numeros": True, "usar_simbolos": True,
                        "excluir_ambiguos": True}
        
        resultado = regenerar_contraseña(str(usr['usuario']['_id']), nuevos_params)
        
        assert 'nueva_contraseña' in resultado
        assert len(resultado['nueva_contraseña']) == 20
        assert resultado['mensaje'] == "Contraseña regenerada exitosamente"
    
    def test_hash_se_actualiza(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Hash en BD debe cambiar después de regenerar"""
        usr = usuario_registrado
        hash_original = usr['usuario']['contraseña_hash']
        
        nuevos_params = {"longitud": 12, "usar_mayusculas": True,
                        "usar_numeros": True, "usar_simbolos": False,
                        "excluir_ambiguos": False}
        regenerar_contraseña(str(usr['usuario']['_id']), nuevos_params)
        
        coleccion = mock_conexion_global.obtener_coleccion('usuarios')
        usuario_bd = coleccion.find_one({'_id': usr['usuario']['_id']})
        assert usuario_bd['contraseña_hash'] != hash_original
    
    def test_usuario_no_existe(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario no encontrado"):
            regenerar_contraseña(id_falso, parametros_contraseña_defecto)
