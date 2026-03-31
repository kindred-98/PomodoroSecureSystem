"""Tests para auth/exportar_contraseña.py"""

import os
import json
import pytest
from bson import ObjectId
from src.auth.exportar_contraseña import exportar_contraseña
from src.seguridad.encriptacion import descifrar


class TestExportarContraseñaValidacion:
    """Tests para validación en exportar_contraseña"""
    
    def test_usuario_id_no_string(self, mock_conexion_global, fernet_key_env, tmp_path):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            exportar_contraseña(123, str(tmp_path / "test.enc"))
    
    def test_ruta_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="ruta_destino debe ser string"):
            exportar_contraseña("id", 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global, fernet_key_env, tmp_path):
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            exportar_contraseña("", str(tmp_path / "test.enc"))
    
    def test_ruta_vacia(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="ruta_destino no puede estar vacía"):
            exportar_contraseña("id", "")
    
    def test_usuario_id_invalido(self, mock_conexion_global, fernet_key_env, tmp_path):
        with pytest.raises(ValueError, match="usuario_id inválido"):
            exportar_contraseña("no_es_objectid", str(tmp_path / "test.enc"))
    
    def test_directorio_no_existe(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="directorio no existe"):
            exportar_contraseña("507f1f77bcf86cd799439011", "/ruta/inexistente/test.enc")


class TestExportarContraseñaExito:
    """Tests para exportación exitosa"""
    
    def test_exportacion_exitosa(self, mock_conexion_global, fernet_key_env, usuario_registrado, tmp_path):
        """Debe crear archivo encriptado"""
        usr = usuario_registrado
        ruta = str(tmp_path / "mi_contraseña")
        
        ruta_final = exportar_contraseña(str(usr['usuario']['_id']), ruta)
        
        assert os.path.exists(ruta_final)
        assert ruta_final.endswith('.enc')
    
    def test_contenido_es_legible(self, mock_conexion_global, fernet_key_env, usuario_registrado, tmp_path):
        """Contenido del archivo debe poder desencriptarse"""
        usr = usuario_registrado
        ruta = str(tmp_path / "test_export")
        
        ruta_final = exportar_contraseña(str(usr['usuario']['_id']), ruta)
        
        with open(ruta_final, 'r', encoding='utf-8') as f:
            contenido_cifrado = f.read()
        
        contenido_json = descifrar(contenido_cifrado)
        datos = json.loads(contenido_json)
        
        assert datos['email'] == usr['usuario']['email']
        assert datos['contraseña'] == usr['contraseña']
    
    def test_usuario_no_existe(self, mock_conexion_global, fernet_key_env, tmp_path):
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario no encontrado"):
            exportar_contraseña(id_falso, str(tmp_path / "test.enc"))
