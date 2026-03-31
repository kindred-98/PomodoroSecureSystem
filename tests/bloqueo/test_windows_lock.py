"""Tests para bloqueo/windows_lock.py"""

import pytest
from unittest.mock import patch, MagicMock
from src.bloqueo.windows_lock import bloquear_escritorio


class TestBloquearEscritorio:
    """Tests para bloquear_escritorio"""

    def test_retorna_dict(self):
        """Debe retornar dict siempre"""
        resultado = bloquear_escritorio()
        assert isinstance(resultado, dict)
        assert 'bloqueado' in resultado
        assert 'plataforma' in resultado
        assert 'mensaje' in resultado

    def test_windows_exitoso(self):
        """En Windows con LockWorkStation exitoso"""
        with patch('src.bloqueo.windows_lock.sys') as mock_sys, \
             patch('ctypes.windll.user32.LockWorkStation', return_value=1):
            mock_sys.platform = 'win32'
            
            resultado = bloquear_escritorio()
            
            assert resultado['bloqueado'] is True
            assert resultado['plataforma'] == 'win32'

    def test_windows_error(self):
        """LockWorkStation retorna 0 (error)"""
        with patch('src.bloqueo.windows_lock.sys') as mock_sys, \
             patch('ctypes.windll.user32.LockWorkStation', return_value=0):
            mock_sys.platform = 'win32'
            
            resultado = bloquear_escritorio()
            
            assert resultado['bloqueado'] is False

    def test_linux_no_soportado(self):
        """Linux no soporta LockWorkStation"""
        with patch('src.bloqueo.windows_lock.sys') as mock_sys:
            mock_sys.platform = 'linux'
            
            resultado = bloquear_escritorio()
            
            assert resultado['bloqueado'] is False
            assert 'linux' in resultado['mensaje'].lower()

    def test_macos_no_soportado(self):
        """macOS no soporta LockWorkStation"""
        with patch('src.bloqueo.windows_lock.sys') as mock_sys:
            mock_sys.platform = 'darwin'
            
            resultado = bloquear_escritorio()
            
            assert resultado['bloqueado'] is False

    def test_windows_excepcion(self):
        """Excepción en ctypes debe manejarse"""
        with patch('src.bloqueo.windows_lock.sys') as mock_sys, \
             patch('ctypes.windll.user32.LockWorkStation', side_effect=Exception("fail")):
            mock_sys.platform = 'win32'
            
            resultado = bloquear_escritorio()
            
            assert resultado['bloqueado'] is False
            assert 'Error' in resultado['mensaje']

    def test_campos_siempre_presentes(self):
        """Debe tener siempre los 3 campos"""
        resultado = bloquear_escritorio()
        assert 'bloqueado' in resultado
        assert 'plataforma' in resultado
        assert 'mensaje' in resultado
