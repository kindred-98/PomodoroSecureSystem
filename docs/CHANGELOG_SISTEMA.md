# PomodoroSecureSystem - Documentación del Sistema

## Resumen General

**PomodoroSecureSystem** es una aplicación de gestión de tiempo Pomodoro para empresas con sistema de roles (Supervisor, Encargado, Empleado), autenticación segura, tracking de actividad y gestión de equipos.

---

## Roles de Usuario

| Rol | Descripción |
|---|-------------|
| **Supervisor** | Gestiona equipos, ve historial completo, configura descansos, gestiona usuarios |
| **Encargado** | Lidera equipos, ve miembros del equipo, tiene timer propio |
| **Empleado** | Usa el timer Pomodoro, inicia/pausa giornada, gestiona contraseñas |

---

## Funcionalidades Implementadas

### 1. Autenticación y Seguridad

- **Login con email y contraseña**
- **PIN diario de 6 dígitos** para verificar identidad diariamente
- **Sesiones con expiración** (12 horas máximo)
- **Frase Semilla** para recuperación de cuenta (12 palabras, 90 días de cooldown)
- **Contraseñas seguras** generadas con evaluación de fortaleza

### 2. Timer Pomodoro

- **Ciclo estándar**: 25 min trabajo → descanso
- **Descansos cortos**: configurables (ej: [5, 5, 5, 5] minutos)
- **Descanso largo**: 15-30 minutos (después de 4 pomodoros)
- **Banco de tiempo**: seguimiento de tiempo acumulado
- **Pausas manuales**: máximo 2 por jornada, máximo 10 min cada una

### 3. Gestión de Equipos

- **Supervisor** crea equipos y asigna encargado
- **Encargado** ve su equipo en dashboard
- **Miembros** aparecen en panel del supervisor
- **Estados online/offline** basados en ciclos activos

### 4. Dashboard y Vistas

#### Supervisor Dashboard
- Vista de equipos con miembros
- Buscador de empleados
- Historial completo (sesiones + pausas de todo el equipo)
- Gestión de equipos (crear, editar, asignar encargado)
- Configuración de descansos de empresa

#### Encargado Dashboard
- Timer personal
- Panel de equipo con miembros
- Estado online/offline de miembros
- Historial personal

#### Empleado Dashboard
- Timer Pomodoro con controles
- Control de pausas (2 máximo)
- Iniciar/Fin de jornada
- Ver contraseña con PIN

### 5. Sistema de Contraseñas

En el dashboard de contraseña:
- **Ver contraseña** (requiere PIN diario)
- **Generar PIN** (1 hora de lockout si falla)
- **Frase Semilla** (90 días de cooldown)
- **Contraseña Segura** (generada automáticamente)
- **Contraseña Personalizada** (con reglas de validación)
- **Cambio manual** (con campo "Repetir contraseña")
- **Exportar** (TXT o JSON)
- **Copiar** botones para PIN, frase, contraseña

### 6. Historial y Reportes

#### Supervisor Historial
- Pestaña **Sesiones**: Todos los pomodoros de empleados/encargados
  - Muestra: nombre usuario, ciclo, pomodoro, duración, fecha/hora
- Pestaña **Pausas**: Todas las pausas del equipo
  - Muestra: nombre usuario, duración, fecha/hora, si excedió límite

#### Reportes de Pausas
Se generan automáticamente cuando un usuario termina una pausa:
- Usuario que tomó la pausa
- Hora de inicio y fin
- Duración en minutos
- Notificado a supervisor y encargado del equipo

### 7. Estados de Conexión

- **Online**: Usuario con ciclo Pomodoro activo
- **Offline**: Sin ciclo activo o presionó "Fin de Jornada"
- Se muestra en dashboard del supervisor y encargado

### 8. Pausas y Descansos

- **Pausas manuales**: Máximo 2 por jornada, 10 min cada una
- Si excede el límite, se registra anomalía
- **Descansos fijos**: Configurados por supervisor
  - Descansos cortos (4 valores)
  - Descanso largo (15-30 min)
- Se aplican automáticamente después de cada Pomodoro

---

## Colecciones MongoDB

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
| `_reportes_jornada` | Reportes diarios |
| `reportes_pausas` | Reportes de pausas |

---

## Estructura del Proyecto

```
PomodoroSecureSystem/
├── src/
│   ├── ui/                    # Interfaces Python
│   │   ├── dashboard_empleado.py
│   │   ├── dashboard_encargado.py
│   │   ├── dashboard_supervisor.py
│   │   ├── gestion_equipos_view.py
│   │   ├── historial_view.py
│   │   └── password_view.py
│   ├── auth/                  # Autenticación
│   │   ├── login.py
│   │   ├── sesion.py
│   │   ├── frase_semilla.py
│   │   └── pin_diario.py
│   ├── timer/                 # Timer Pomodoro
│   │   ├── servicio_timer.py
│   │   ├── ciclo_pomodoro.py
│   │   └── banco_tiempo.py
│   ├── pausas/               # Gestión de pausas
│   │   └── gestor_pausas.py
│   ├── db/                   # Base de datos
│   │   ├── equipos/
│   │   ├── sesiones/
│   │   └── usuarios/
│   └── config/
│       └── colores.py
├── tests/                    # Tests pytest
├── docs/                     # Documentación
└── main.py                   # Punto de entrada
```

---

## Comandos Importantes

```bash
# Ejecutar aplicación
python main.py

# Ejecutar tests
pytest

# Escan seguridad
bandit -r src/
```

---

## Notas de Uso

1. **Primer login del día**: Requiere PIN de 6 dígitos
2. **Configurar descansos**: Solo supervisor puede hacerlo
3. **Modificar descansos**: Solo después de completar un ciclo (4 cortos + 1 largo)
4. **Recuperar cuenta**: Usa frase semilla después de 90 días
5. **Ver contraseña**: Requiere PIN diario válido

---

## Fecha de Documentación

Abril 2026