# Changelog - PomodoroSecureSystem

## v2.0.0 (2026-04-06)

### Bug Fixes

#### Sesion Expiracion
- **Problema**: Las sesiones de empleados permanecian activas por 4+ dias cuando la app no se cerraba
- **Solucion**: Se agrego verificacion de expiracion en el metodo `tick()` de `servicio_timer.py` antes de continuar el ciclo

### Nuevas Funcionalidades

#### 1. Gestion de Contrasenas
- Campo "Repetir contrasena" en cambio de contrasena
- Generador de PIN de 6 digitos para ver contrasena actual
- Validacion de fortaleza de contrasena

#### 2. Dashboard Encargado
- Timer Pomodoro completo con controles (iniciar/pausar/reiniciar)
- Panel de pausas con minutos restantes
- Boton "Fin de jornada laboral"
- Panel de equipo con miembros asignados

#### 3. Dashboard Supervisor
- Buscador de empleados por nombre
- Estado online/offline en tiempo real para cada usuario
- Estadisticas de conexion (X conectados)
- Gestion de equipos via interfaz grafica

#### 4. Gestion de Equipos (CRUD)
- Crear nuevos equipos
- Editar nombre de equipo
- Asignar encargado a equipo
- Agregar/quitar miembros del equipo
- Eliminar equipos

#### 5. Estado de Conexion
- Verificacion en tiempo real de usuarios conectados
- Tiempo desconectado (ej: "Hace 2h 15m")
- Iconos visuales (verde/rojo) para estado

#### 6. Modulo de Reportes
- Estadisticas de actividad
- Exportacion de datos

### Nuevas Funciones DB

| Archivo | Descripcion |
|---------|-------------|
| `db/equipos/listar_todos.py` | Lista todos los equipos |
| `db/equipos/editar_equipo.py` | Edita nombre, asigna/quita encargado y miembros |
| `db/usuarios/estado_conexion.py` | Obtiene estado de conexion de usuarios |
| `db/reportes.py` | Genera reportes de actividad |

### CI/CD

- GitHub Actions workflow para security audit
- Configuracion pytest con coverage (83%)

### Tests

**620 tests passing**

- `tests/timer/test_servicio_timer_expiracion.py` - Tests de expiracion de sesion
- `tests/timer/test_ciclo_pomodoro_completo.py` - Tests de ciclo completo
- `tests/auth/test_pin_diario.py` - Tests de PIN diario
- `tests/db/test_reportes.py` - Tests de reportes
- `tests/db/sesiones/*` - Tests de sesiones
- `tests/db/equipos/*` - Tests de equipos
- `tests/db/anomalias/*` - Tests de anomalias

---

## Roles del Sistema

| Rol | Permisos |
|-----|----------|
| **Empleado** | Timer Pomodoro, pausas, ver PIN diario, cambiar contrasena |
| **Encargado** | Todo lo anterior + ver equipo, timer propio + dashboard |
| **Supervisor** | Todo lo anterior + gestionar usuarios, equipos, anomalias, reportes |

## Duracion de Sesiones

- **Maximo**: 12 horas
- **Forzar reset**: Si la app permanece abierta mas de 12 horas, se fuerza el cierre de sesion

## Estructura del Proyecto

```
PomodoroSecureSystem/
├── src/
│   ├── db/
│   │   ├── equipos/          # CRUD equipos
│   │   ├── usuarios/         # Estado conexion
│   │   ├── anomalias.py
│   │   ├── reportes.py
│   │   └── sesiones.py
│   ├── timer/
│   │   └── servicio_timer.py # Logica Pomodoro
│   └── ui/
│       ├── dashboard_*.py     # Dashboards por rol
│       ├── password_view.py  # Gestion contrasenas
│       └── gestion_equipos_view.py
├── tests/                    # 620 tests
└── .github/workflows/        # CI/CD
```
