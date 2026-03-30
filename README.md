# 🍅🔐 PomodoroSecure System

> Aplicación de escritorio Windows para la gestión del tiempo laboral de equipos de programación.  
> Combina la técnica Pomodoro con un sistema de autenticación segura, control de presencia real y trazabilidad de anomalías.

---

## 📋 Descripción

**PomodoroSecure** integra dos herramientas en un único sistema cohesionado:

- **Generador de contraseñas seguras** — el sistema de autenticación genera las contraseñas a partir de parámetros del usuario. Nadie elige su propia contraseña.
- **Pomodoro Timer profesional** — gestión del tiempo de trabajo con descansos forzados, bloqueo de pantalla y validación de presencia mediante OTP.

Desarrollado como proyecto integrador del **Módulo 2 — Estrategias de Generación de Código con IA** de Dicampus.

---

## 🎯 Funcionalidades principales

- Autenticación segura con contraseñas generadas por el sistema (módulo `secrets`)
- Encriptación de contraseñas almacenadas con Fernet (AES-128-CBC)
- Hash de verificación de login con bcrypt
- Timer Pomodoro con banco de tiempo configurable (50 min por ciclo)
- Bloqueo total de pantalla Windows en descansos obligatorios
- Validación de presencia mediante OTP de 6 dígitos (expira en 7 min)
- Sistema de pausas manuales con límites y control de anomalías
- Panel de supervisión diferenciado por rol (empleado / encargado / supervisor)
- Registro de anomalías con trazabilidad completa en MongoDB Atlas
- Cobertura de tests ≥ 80% con pytest-cov

---

## 👥 Roles del sistema

| Rol | Descripción |
|---|---|
| Empleado | Acceso a su Pomodoro, historial propio y configuración de descansos flexibles |
| Encargado | Vista de su equipo en tiempo real + anomalías de su equipo |
| Supervisor | Panel global, configuración de empresa y gestión de usuarios |

---

## 🗂️ Estructura del proyecto
```
PomodoroSecureSystem/
├── src/
│   ├── auth/          ← Autenticación: login, registro, sesión
│   ├── generador/     ← Generador de contraseñas y evaluador de fortaleza
│   ├── timer/         ← Lógica del ciclo Pomodoro y banco de tiempo
│   ├── pausas/        ← Control de pausas manuales
│   ├── bloqueo/       ← Bloqueo de pantalla Windows
│   ├── otp/           ← Generación y verificación de códigos OTP
│   ├── anomalias/     ← Registro y notificación de anomalías
│   ├── db/            ← Conexión y operaciones MongoDB Atlas
│   ├── ui/            ← Interfaz gráfica CustomTkinter
│   ├── config/        ← Configuración global y paleta de colores
│   ├── seguridad/     ← Encriptación Fernet y hashing bcrypt
│   └── notificaciones/ ← Alertas sonoras y visuales
├── tests/             ← Tests unitarios (cobertura ≥ 80%)
├── docs/              ← Documentación y registro de asistencia IA
├── build/             ← Ejecutable .exe (generado con PyInstaller)
├── .env.example       ← Plantilla de variables de entorno
├── requirements.txt   ← Dependencias del proyecto
└── README.md          ← Este archivo
```

---

## ⚙️ Instalación y configuración

### Requisitos previos
- Windows 10/11
- Python 3.12+
- Cuenta en MongoDB Atlas (tier gratuito M0)

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/kindred-98/PomodoroSecureSystem.git
cd PomodoroSecureSystem
```

**2. Crear y activar el entorno virtual**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**3. Instalar dependencias**
```powershell
pip install -r requirements.txt
```

**4. Configurar variables de entorno**
```powershell
copy .env.example .env
# Edita .env con tu connection string de MongoDB Atlas
```

**5. Ejecutar la aplicación**
```powershell
python src/main.py
```

---

## 🧪 Ejecutar tests
```powershell
# Ejecutar todos los tests
pytest

# Con informe de cobertura
pytest --cov=src --cov-report=term-missing

# Cobertura mínima requerida: 80%
pytest --cov=src --cov-fail-under=80
```

---

## 🔐 Seguridad

- Las contraseñas **nunca se almacenan en texto plano**
- Verificación de login mediante hash bcrypt (no reversible)
- Almacenamiento encriptado con Fernet para recuperación por el usuario
- El archivo `.env` y las claves (`.key`) están en `.gitignore`
- Conexión a MongoDB Atlas siempre por TLS/SSL

---

## 📁 Documentación

- [`docs/PLANIFICACION_COMPLETA.md`](docs/PLANIFICACION_COMPLETA.md) — Arquitectura y decisiones de diseño completas
- [`docs/asistencia_ia.md`](docs/asistencia_ia.md) — Registro de prompts utilizados con IA

---

## 👨‍💻 Autor

**A.D.E.V.** · [kindred-98](https://github.com/kindred-98)  
Módulo 2 · Estrategias de Generación de Código con IA · Dicampus