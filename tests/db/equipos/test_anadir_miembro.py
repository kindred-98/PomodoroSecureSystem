"""Tests para añadir_miembro."""

import pytest
from bson import ObjectId

from src.db.equipos.anadir_miembro import anadir_miembro


class TestAnadirMiembro:
    """Tests para función añadir_miembro."""

    @pytest.mark.parametrize(
        "equipo_id, usuario_id",
        [
            (123, str(ObjectId())),
            (str(ObjectId()), 123),
            (None, str(ObjectId())),
            (str(ObjectId()), None),
        ],
    )
    def test_tipos_invalidos(self, mock_conexion_global, equipo_id, usuario_id):
        """ rechack tipos."""
        with pytest.raises(TypeError):
            anadir_miembro(equipo_id, usuario_id)

    @pytest.mark.parametrize(
        "equipo_id, usuario_id",
        [
            ("invalid", str(ObjectId())),
            (str(ObjectId()), "invalid"),
            ("123", "456"),
        ],
    )
    def test_ids_invalidos(self, mock_conexion_global, equipo_id, usuario_id):
        """ rechack IDs."""
        with pytest.raises(ValueError):
            anadir_miembro(equipo_id, usuario_id)

    @pytest.mark.parametrize(
        "equipo_id, usuario_id",
        [
            ("", str(ObjectId())),
            (str(ObjectId()), ""),
        ],
    )
    def test_vacios(self, mock_conexion_global, equipo_id, usuario_id):
        """ rechack vacíos."""
        with pytest.raises(ValueError):
            anadir_miembro(equipo_id, usuario_id)
