"""Tests para crear_equipo()"""

import pytest
from bson import ObjectId
from src.db.equipos.crear_equipo import crear_equipo


class TestCrearEquipoValidacion:
    """Tests para validación en crear_equipo"""
    
    def test_nombre_no_string(self, mock_conexion_global):
        """Debe fallar si nombre no es string"""
        with pytest.raises(TypeError, match="nombre debe ser string"):
            crear_equipo(123, str(ObjectId()), 'desc')
    
    def test_encargado_no_string(self, mock_conexion_global):
        """Debe fallar si encargado_id no es string"""
        with pytest.raises(TypeError, match="encargado_id debe ser string"):
            crear_equipo('Team', 123, 'desc')
    
    def test_nombre_vacio(self, mock_conexion_global):
        """Debe fallar si nombre es vacío"""
        with pytest.raises(ValueError, match="Nombre no puede estar vacío"):
            crear_equipo('', str(ObjectId()), 'desc')
    
    def test_encargado_invalido(self, mock_conexion_global):
        """Debe fallar si encargado_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="encargado_id inválido"):
            crear_equipo('Team', 'invalid', 'desc')


class TestCrearEquipoExito:
    """Tests para casos exitosos de crear_equipo"""
    
    def test_crea_equipo_correctamente(self, mock_conexion_global, usuario_en_db, coleccion_usuarios, coleccion_equipos):
        """Debe crear equipo correctamente"""
        resultado = crear_equipo('Dev Team', str(usuario_en_db['_id']), 'Development team')
        
        assert resultado['nombre'] == 'Dev Team'
        assert resultado['descripcion'] == 'Development team'
        assert resultado['encargado_id'] == usuario_en_db['_id']
        assert usuario_en_db['_id'] in resultado['miembros']
    
    def test_encargado_no_existe(self, mock_conexion_global, coleccion_usuarios, coleccion_equipos):
        """Debe fallar si encargado no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Encargado con ID .* no existe"):
            crear_equipo('Team', id_falso, 'desc')
