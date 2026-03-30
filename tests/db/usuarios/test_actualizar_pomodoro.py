"""Tests para actualizar_pomodoro()"""

import pytest
from bson import ObjectId
from src.db.usuarios.actualizar_pomodoro import actualizar_pomodoro


class TestActualizarPomodoroValidacion:
    """Tests para validación en actualizar_pomodoro"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            actualizar_pomodoro(123, 5)
    
    def test_incremento_no_int(self, mock_conexion_global):
        """Debe fallar si incremento no es int"""
        with pytest.raises(TypeError, match="incremento debe ser int"):
            actualizar_pomodoro(str(ObjectId()), 'cinco')
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="ID inválido"):
            actualizar_pomodoro('', 5)
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="ID inválido"):
            actualizar_pomodoro('invalid', 5)


class TestActualizarPomodoroExito:
    """Tests para casos exitosos de actualizar_pomodoro"""
    
    def test_incrementa_puntuacion(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Debe incrementar puntuación del usuario"""
        usuario_inicial = coleccion_usuarios.find_one({'_id': usuario_en_db['_id']})
        puntos_iniciales = usuario_inicial.get('puntuacion_pomodoro', 0)
        
        resultado = actualizar_pomodoro(str(usuario_en_db['_id']), 10)
        
        assert resultado['puntuacion_pomodoro'] == puntos_iniciales + 10
    
    def test_puede_usar_incremento_negativo(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Debe permitir decrementos (incremento negativo)"""
        # Primero incrementar
        actualizar_pomodoro(str(usuario_en_db['_id']), 20)
        usuario = coleccion_usuarios.find_one({'_id': usuario_en_db['_id']})
        puntos_con_20 = usuario['puntuacion_pomodoro']
        
        # Luego decrementar
        resultado = actualizar_pomodoro(str(usuario_en_db['_id']), -5)
        
        assert resultado['puntuacion_pomodoro'] == puntos_con_20 - 5
    
    def test_usuario_no_existe(self, mock_conexion_global, coleccion_usuarios):
        """Debe fallar si usuario no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario con ID .* no existe"):
            actualizar_pomodoro(id_falso, 5)
