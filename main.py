"""
main.py - Entry point de PomodoroSecure
Ejecutar: python main.py
"""

import os
import sys
from pathlib import Path

# Cargar .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')


def main():
    errores = []

    if not os.getenv('MONGODB_URI'):
        errores.append("MONGODB_URI no configurada en .env")

    if not os.getenv('FERNET_KEY'):
        errores.append("FERNET_KEY no configurada en .env")

    if errores:
        print("")
        print("Configuracion incompleta:")
        print("")
        for e in errores:
            print(f"   - {e}")
        print("")
        print("   Crea/edita .env en la raiz del proyecto:")
        print("   MONGODB_URI=mongodb+srv://usuario:pass@cluster.mongodb.net/")
        print("   FERNET_KEY=tu_clave_aqui")
        print("")
        return

    from src.app import PomodoroSecureApp

    app = PomodoroSecureApp()
    app.mainloop()


if __name__ == "__main__":
    main()
