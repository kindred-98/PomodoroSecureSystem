"""Tests para crear_equipo()"""

import pytest
from bson import ObjectId
from unittest.mock import patch
from src.db.equipos.crear_equipo import crear_equipo


class TestCrearEquipoValidacion:
    """Tests para validación en crear_equipo"""
    
    def test_nombre_no_string(self, conexion_mongodb_mock):
        """Debe fallar si nombre no es string"""
        with patch('src.db.equipos.crear_equipo.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="nombre debe ser string"):
                crear_equipo(123, str(ObjectId()), 'desc')
    
    def test_encargado_no_string(self, conexion_mongodb_mock):
        """Debe fallar si encargado_id no es string"""
        with patch('src.db.equipos.crear_equipo.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="encargado_id debe ser string"):
                crear_equipo('Team', 123, 'desc')
    
    def test_nombre_vacio(self, conexion_mongodb_mock):
        """Debe fallar si nombre es vacío"""
        with patch('src.db.equipos.crear_equipo.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="nombre no puede estar vacío"):
                crear_equipo('', str(ObjectId()), 'desc')
    
    def test_encargado_invalido(self, conexion_mongodb_mock):
        """Debe fallar si encargado_id no es ObjectId válido"""
        with patch('src.db.equipos.crear_equipo.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="encargado_id .* no es un ObjectId válido"):
                crear_equipo('Team', 'invalid', 'desc')


class TestCrearEquipoExito:
    """Tests para casos exitosos de crear_equipo"""
    
    def test_crea_equipo_correctamente(self, usuario_en_db, coleccion_usuarios, coleccion_equipos):
        """Debe crear equipo correctamente"""
        with patch('src.db.equipos.crear_equipo.ConexionMmongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_equipos
            )
            
            resultado = crear_equipo('Dev Team', str(usuario_en_db['_id']), 'Development team')
            
            assert resultado['nombre'] == 'Dev Team'
            assert resultado['descripcion'] == 'Development team'
            assert resultado['encargado_id'] == usuario_en_db['_id']
            assert usuario_en_db['_id'] in resultado['miembros']
    
    def test_encargado_no_existe(self, coleccion_usuarios, coleccion_equipos):
        """Debe fallar si encargado no existe"""
        with patch('src.db.equipos.crear_equipo.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_equipos
            )
            
            id_falso = str(ObjectId())
            with pytest.raises(Exception, match="Usuario con ID .* no existe"):
                crear_equipo('Team', id_falso, 'desc')
