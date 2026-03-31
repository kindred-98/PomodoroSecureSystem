"""
Módulo: main.py
Responsabilidad: Entry point de la aplicación PomodoroSecure.
"""

import sys
import os

# Asegurar que src está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Punto de entrada principal."""
    # Verificar variables de entorno necesarias
    if not os.getenv('FERNET_KEY'):
        print("⚠️  FERNET_KEY no configurada.")
        print("   Genera una clave con: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"")
        print("   Y añádela a tu archivo .env como: FERNET_KEY=tu_clave_aqui")
        print()

    from app import PomodoroSecureApp

    app = PomodoroSecureApp()
    app.mainloop()


if __name__ == "__main__":
    main()
