import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================
# BASE DE DATOS — MONGODB ATLAS
# ============================
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://user:pass@cluster0.mongodb.net/?appName=Cluster0"
)

if not MONGODB_URI or "YOUR_PASSWORD" in MONGODB_URI:
    raise ValueError(
        "❌ MONGODB_URI no está configurada en .env\n"
        "Por favor, configura tu variable de entorno MONGODB_URI"
    )

# ============================
# APLICACIÓN
# ============================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_NAME = "PomodoroSecureSystem"
APP_VERSION = "1.0.0"