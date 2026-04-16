"""Tests para añadir_miembro."""

import pytest
from bson import ObjectId


class TestAñadirMiembro:
    """Tests para función añadir_miembro."""

    def test_tipos_invalidos(self, mock_conexion_global):
        """ rechack tipos."""
        from src.db.equipos.añadir_miembro import añadir_miembro
        
        with pytest.raises(TypeError):
            añadir_miembro(123, str(ObjectId()))
        
        with pytest.raises(TypeError):
            añadir_miembro(str(ObjectId()), 123)
        
        with pytest.raises(TypeError):
            añadir_miembro(None, str(ObjectId()))
        
        with pytest.raises(TypeError):
            añadir_miembro(str(ObjectId()), None)

    def test_ids_invalidos(self, mock_conexion_global):
        """ rechack IDs."""
        from src.db.equipos.añadir_miembro import añadir_miembro
        
        with pytest.raises(ValueError):
            añadir_miembro("invalid", str(ObjectId()))
        
        with pytest.raises(ValueError):
            añadir_miembro(str(ObjectId()), "invalid")
        
        with pytest.raises(ValueError):
            añadir_miembro("123", "456")

    def test_vacios(self, mock_conexion_global):
        """ rechack vacíos."""
        from src.db.equipos.añadir_miembro import añadir_miembro
        
        with pytest.raises(ValueError):
            añadir_miembro("", str(ObjectId()))
        
        with pytest.raises(ValueError):
            añadir_miembro(str(ObjectId()), "")