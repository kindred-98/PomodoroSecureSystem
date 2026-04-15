# 🍅 PomodoroSecureSystem 🔐

> Aplicación de escritorio Windows para la gestión del tiempo laboral de equipos de programación.
> Combina la técnica Pomodoro con un sistema de autenticación segura, control de presencia real y gestión de equipos.

---

## 📋 Descripción

**PomodoroSecureSystem** es una aplicación empresarial para gestión del tiempo de trabajo que incluye:

- **Timer Pomodoro** con descansos configurables y pausas manuales
- **Gestión de equipos** con roles diferenciados (Supervisor, Encargado, Empleado)
- **Autenticación segura** con PIN diario, frases semilla y contraseñas generadas por el sistema
- **Historial y reportes** completo para supervisión

---

## 🎯 Funcionalidades Principales

### Autenticación y Seguridad
- Login con email y contraseña
- **PIN diario** de 6 dígitos para verificar identidad diariamente
- **Frase Semilla** (12 palabras) para recuperación de cuenta (90 días de cooldown)
- **Sesiones con expiración** (12 horas máximo)
- Contraseñas generadas por el sistema con evaluación de fortaleza
- Encriptación de contraseñas con Fernet (AES-128-CBC)
- Hash de verificación con bcrypt

### Timer Pomodoro
- Ciclo estándar de 25 minutos de trabajo
- **Descansos cortos** configurables (ej: [5, 5, 5, 5] minutos)
- **Descanso largo** de 15-30 minutos (después de 4 pomodoros)
- Banco de tiempo acumulado
- **Pausas manuales**: máximo 2 por jornada, máximo 10 minutos cada una

### Gestión de Equipos
- Supervisor crea equipos y asigna encargado
- Encargado lidera su equipo
- Miembros distribuidos por el supervisor
- Estados online/offline en tiempo real

### Dashboard por Rol

#### Supervisor
- Vista global de equipos con miembros
- Buscador de empleados
- Historial completo (sesiones + pausas del equipo)
- Gestión de equipos
- Configuración de descansos de empresa

#### Encargado
- Timer personal
- Panel de equipo con miembros
- Estado online/offline de miembros

#### Empleado
- Timer Pomodoro con controles
- Control de pausas (2 máximo)
- Iniciar/Fin de jornada
- Ver contraseña con PIN

### Sistema de Contraseñas
- Ver contraseña (requiere PIN diario)
- Generar PIN (1 hora de lockout)
- Frase Semilla (90 días de cooldown)
- Contraseña Segura (generada automáticamente)
- Contraseña Personalizada (con validación)
- Cambio manual con repetición
- Exportar a TXT/JSON

---

## 👥 Roles del Sistema

| Rol | Descripción |
|---|---|
| **Supervisor** | Gestiona equipos, ve historial completo, configura descansos, gestiona usuarios |
| **Encargado** | Lidera equipos, ve miembros, tiene timer propio |
| **Empleado** | Usa el timer Pomodoro, inicia/pausa jornada, gestiona contraseñas |

---

## 🗂️ Estructura del Proyecto

```
PomodoroSecureSystem/
├── src/
│   ├── ui/                    ← Interfaces CustomTkinter
│   │   ├── dashboard_empleado.py
│   │   ├── dashboard_encargado.py
│   │   ├── dashboard_supervisor.py
│   │   ├── gestion_equipos_view.py
│   │   ├── historial_view.py
│   │   └── password_view.py
│   ├── auth/                  ← Autenticación
│   │   ├── login.py
│   │   ├── sesion.py
│   │   ├── frase_semilla.py
│   │   └── pin_diario.py
│   ├── timer/                 ← Timer Pomodoro
│   │   ├── servicio_timer.py
│   │   ├── ciclo_pomodoro.py
│   │   └── banco_tiempo.py
│   ├── pausas/               ← Gestión de pausas
│   │   └── gestor_pausas.py
│   ├── db/                   ← MongoDB
│   │   ├── equipos/
│   │   ├── sesiones/
│   │   ��── usuarios/
│   └── generador/            ← Generador de contraseñas
├── tests/                    ← Tests pytest (620 tests)
├── docs/                     ← Documentación
├── main.py                   ← Punto de entrada
└── README.md
```

---

## ⚙️ Instalación y Configuración

### Requisitos Previos
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
python main.py
```

---

## 🧪 Ejecutar Tests

```powershell
# Ejecutar todos los tests
pytest

# Tests específicos
pytest tests/pausas/
pytest tests/timer/
pytest tests/db/
```

**Cobertura actual**: 620 tests passing

---

## 🔐 Seguridad

- Las contraseñas **nunca se almacenan en texto plano**
- Verificación de login mediante hash bcrypt
- Almacenamiento encriptado con Fernet
- PIN diario expira cada día
- Frase semilla con cooldown de 90 días
- Conexión a MongoDB Atlas por TLS/SSL

---

## 📁 Colecciones MongoDB

| Colección | Descripción |
|---|-------------|
| `usuarios` | Usuarios del sistema |
| `sesiones_auth` | Sesiones de login |
| `sesiones` | Sesiones Pomodoro |
| `ciclos_pomodoro` | Ciclos activos/completados |
| `equipos` | Equipos de trabajo |
| `config_descansos` | Configuración de descansos |
| `pausas_manuales` | Pausas tomadas |
| `anomalias` | Anomalías detectadas |
| `reportes_jornada` | Reportes diarios |
| `reportes_pausas` | Reportes de pausas |

---

## 📝 Notas de Uso

1. **Primer login del día**: Requiere PIN de 6 dígitos
2. **Configurar descansos**: Solo el supervisor puede hacerlo
3. **Modificar descansos**: Solo después de completar un ciclo (4 cortos + 1 largo)
4. **Recuperar cuenta**: Usa frase semilla después de 90 días
5. **Ver contraseña**: Requiere PIN diario válido

---

## 👨‍💻 Autor

**A.D.E.V.** · [kindred-98](https://github.com/kindred-98)