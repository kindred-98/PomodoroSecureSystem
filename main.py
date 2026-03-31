"""
main.py - Entry point de PomodoroSecure
Ejecutar: python main.py
"""

import sys
import os
from pathlib import Path

# Añadir src al path
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')


def main():
    """Punto de entrada principal de la aplicación."""
    # Verificar variables de entorno
    errores = []

    if not os.getenv('MONGODB_URI'):
        errores.append("MONGODB_URI no configurada en .env")

    if not os.getenv('FERNET_KEY'):
        errores.append(
            "FERNET_KEY no configurada en .env\n"
            "   Genera una: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )

    if errores:
        print("\n⚠️  Configuración incompleta:\n")
        for e in errores:
            print(f"   • {e}")
        print("\n   Crea un archivo .env en la raíz del proyecto con:")
        print("   MONGODB_URI=mongodb+srv://usuario:pass@cluster.mongodb.net/")
        print("   FERNET_KEY=tu_clave_aqui")
        print()
        return

    # Importar y lanzar la app
    from app import PomodoroSecureApp

    app = PomodoroSecureApp()
    app.mainloop()


if __name__ == "__main__":
    main()
