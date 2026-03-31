# FASE 5: Timer & Pomodoro Core — Implementación Completa

**Fecha:** 31 de Marzo de 2026  
**Estado:** ✅ COMPLETADA — 441 TESTS PASANDO (100%)  
**Documentación previa:** [FASE_4_AUTENTICACION.md](FASE_4_AUTENTICACION.md)

---

## Resumen Ejecutivo

### Estado del Proyecto Post-FASE 5

```
██████████████████████████████████████░░░░░░░░ 80% Completo
(Generador 100% | BD 100% | Auth 100% | Timer 100% | OTP 0% | UI 0%)
```

| Módulo | Estado | Tests |
|--------|--------|-------|
| **Generador** | ✅ 100% | 202 |
| **Base de Datos** | ✅ 100% | 63 |
| **Autenticación** | ✅ 100% | 95 |
| **Timer & Pausas** | ✅ 100% | 81 |
| **OTP & Bloqueo** | ⏳ Pendiente | 0 |
| **Interfaz Gráfica** | ⏳ Pendiente | 0 |
| **Pipeline** | ⏳ Pendiente | 0 |

---

## Arquitectura Implementada

```
src/
├── timer/
│   ├── __init__.py              ✅ Exports: 15 símbolos
│   ├── banco_tiempo.py          ✅ Validación descansos (50 min)
│   ├── estados.py               ✅ Máquina de estados + cálculo ciclos
│   ├── ciclo_pomodoro.py        ✅ Orquestación + callbacks
│   └── servicio_sesiones.py     ✅ Capa intermedia BD
│
├── pausas/
│   ├── __init__.py              ✅ Exports: 2 funciones
│   └── gestor_pausas.py         ✅ Pausas manuales (máx 2 × 10 min)
```

---

## Módulo: Banco de Tiempo (`src/timer/banco_tiempo.py`)

### Funciones implementadas (2)

#### 1. `validar_configuracion_descansos(descansos_cortos, banco_total=50) -> dict`

Valida que la configuración de descansos del usuario cumpla las reglas del sistema.

```python
resultado = validar_configuracion_descansos([5, 5, 5, 5])
# {
#     'valido': True,
#     'descansos_cortos': [5, 5, 5, 5],
#     'descanso_largo': 30,
#     'banco_total': 50,
#     'errores': []
# }
```

**Reglas validadas:**

```
4 descansos cortos (siempre 4, no más no menos)
├── Cada uno: 5 min mínimo, 10 min máximo
├── Suma total de cortos: entre 20 y 35 min
├── Descanso largo = banco_total - suma(cortos)
└── Largo resultante: 15 min mínimo, 30 min máximo
```

**Ejemplos:**

| Configuración | Suma | Largo | Resultado |
|---------------|------|-------|-----------|
| `[5, 5, 5, 5]` | 20 | 30 | ✅ Válido |
| `[10, 10, 10, 5]` | 35 | 15 | ✅ Válido |
| `[7, 7, 7, 7]` | 28 | 22 | ✅ Válido |
| `[10, 10, 10, 10]` | 40 | 10 | ❌ Largo < 15 |
| `[4, 5, 5, 5]` | 19 | — | ❌ Corto < 5 |
| `[11, 5, 5, 5]` | — | — | ❌ Corto > 10 |
| `[5, 5, 5]` | — | — | ❌ No son 4 |

#### 2. `calcular_descanso_largo(descansos_cortos, banco_total=50) -> int`

Retorna directamente `banco_total - sum(cortos)`.

```python
calcular_descanso_largo([5, 5, 5, 5])        # → 30
calcular_descanso_largo([10, 10, 10, 5])      # → 15
calcular_descanso_largo([8, 8, 8, 8], 40)     # → 8
```

### Tests: 20 tests en `tests/timer/test_banco_tiempo.py`

| Clase | Tests | Cobertura |
|-------|-------|-----------|
| `TestValidarConfiguracion` | 14 | Válidos, inválidos, tipos, bordes |
| `TestCalcularDescansoLargo` | 6 | Cálculo, custom banco, tipos |

---

## Módulo: Estados (`src/timer/estados.py`)

### Constantes

```python
ESTADO_INACTIVO        = "INACTIVO"
ESTADO_TRABAJANDO      = "TRABAJANDO"
ESTADO_DESCANSO_CORTO  = "DESCANSO_CORTO"
ESTADO_DESCANSO_LARGO  = "DESCANSO_LARGO"
ESTADO_PAUSADO         = "PAUSADO"
```

### Máquina de Estados

```
INACTIVO ──────────→ TRABAJANDO ──────────→ DESCANSO_CORTO ──────────→ TRABAJANDO
                        │                                               │
                        ↓                                               ↓
                     PAUSADO ──────────→ TRABAJANDO              DESCANSO_LARGO
                                                                            │
                                                                            ↓
                                                                    INACTIVO (ciclo fin)
```

### Funciones implementadas (2)

#### 1. `obtener_transiciones_validas() -> dict`

Retorna el mapa completo de transiciones válidas.

```python
{
    "INACTIVO":       ["TRABAJANDO"],
    "TRABAJANDO":     ["DESCANSO_CORTO", "DESCANSO_LARGO", "PAUSADO", "INACTIVO"],
    "DESCANSO_CORTO": ["TRABAJANDO", "DESCANSO_LARGO"],
    "DESCANSO_LARGO": ["TRABAJANDO", "INACTIVO"],
    "PAUSADO":        ["TRABAJANDO", "DESCANSO_CORTO"],
}
```

#### 2. `calcular_ciclos_jornada(horario_inicio, horario_fin, ...) -> dict`

Calcula cuántos ciclos Pomodoro caben en la jornada del trabajador. **Nada hardcodeado** — adapta todo al horario real.

```python
# Trabajador A: 08:00 - 16:00 (8h)
calcular_ciclos_jornada("08:00", "16:00")
# → duracion_jornada_min: 480
# → ciclos_completos: 3
# → minutos_sobrantes: 30

# Trabajador B: 09:00 - 15:00 (6h)
calcular_ciclos_jornada("09:00", "15:00")
# → duracion_jornada_min: 360
# → ciclos_completos: 2
# → ciclo_reducido: True (2 pomodoros caben en 60 min sobrantes)

# Pomodoro configurable a 30 min
calcular_ciclos_jornada("09:00", "16:00", pomodoro_min=30)
# → pomodoro_trabajo_min: 30
# → ciclos_completos: 2 (ciclo más largo = 170 min)
```

**Cálculo interno:**

```
duracion_ciclo = (pomodoro_min × 4) + sum(cortos) + descanso_largo
ciclos_completos = jornada_minutos // duracion_ciclo
minutos_sobrantes = jornada_minutos % duracion_ciclo
ciclo_reducido = minutos_sobrantes >= (pomodoro_min × 2) + min(cortos)
```

### Tests: 18 tests en `tests/timer/test_estados.py`

| Clase | Tests |
|-------|-------|
| `TestObtenerTransiciones` | 6 (estructura, estados específicos) |
| `TestCalcularCiclosJornada` | 12 (jornadas varias, configuración custom, validación) |

---

## Módulo: Ciclo Pomodoro (`src/timer/ciclo_pomodoro.py`)

### Sistema de Callbacks

Patrón de eventos para conectar con FASE 6 sin dependencias directas:

```python
# FASE 5 registra el mecanismo:
def registrar_callback(evento: str, funcion):
    ...

def _emitir_evento(evento: str, datos: dict):
    for callback in _callbacks[evento]:
        callback(datos)

# Eventos disponibles:
# - 'descanso_iniciado'    → FASE 6 genera OTP + muestra bloqueo
# - 'descanso_finalizado'  → FASE 6 solicita OTP al usuario
# - 'ciclo_completado'     → FASE 6 muestra resumen de jornada
# - 'pomodoro_completado'  → para registro de sesiones
# - 'anomalia_generada'    → FASE 6 registra en BD
```

### Funciones implementadas (3 + callbacks)

#### 1. `iniciar_ciclo(usuario_id, configuracion=None) -> dict`

Crea un nuevo ciclo Pomodoro en la colección `ciclos_pomodoro`.

```python
resultado = iniciar_ciclo("507f...", {
    'pomodoro_min': 25,
    'descansos_cortos': [5, 5, 5, 5],
    'descanso_largo': 30,
})
# {
#     'ciclo_id': 'abc123...',
#     'numero_ciclo': 1,
#     'estado': 'TRABAJANDO',
#     'pomodoro_actual': 1,
#     'pomodoros_totales': 4,
#     'configuracion': {...}
# }
```

**Nueva colección `ciclos_pomodoro`:**

```json
{
    "_id": "ObjectId",
    "usuario_id": "ObjectId",
    "numero_ciclo": 1,
    "pomodoros_completados": 0,
    "pomodoro_actual": 1,
    "pomodoros_totales": 4,
    "estado_actual": "TRABAJANDO",
    "inicio_ciclo": "2026-03-31T09:00:00",
    "configuracion": {
        "pomodoro_min": 25,
        "descansos_cortos": [5, 5, 5, 5],
        "descanso_largo": 30
    },
    "descansos_cortos_restantes": [5, 5, 5, 5],
    "descanso_largo_restante": 30,
    "completado": false
}
```

**Validaciones:**
- No permite dos ciclos activos simultáneos
- Valida que `pomodoro_min` sea positivo
- Incrementa `numero_ciclo` automáticamente

#### 2. `obtener_estado_ciclo(usuario_id) -> dict`

Retorna el estado actual del ciclo del usuario.

```python
estado = obtener_estado_ciclo("507f...")
# {
#     'en_ciclo': True,
#     'ciclo_id': 'abc123...',
#     'numero_ciclo': 1,
#     'pomodoro_actual': 2,
#     'pomodoros_totales': 4,
#     'estado': 'TRABAJANDO',
#     'pomodoros_completados': 1,
#     'descansos_cortos_restantes': [5, 5, 5],
#     'descanso_largo_restante': 30,
#     'configuracion': {...}
# }
```

#### 3. `manejar_evento_timer(usuario_id, evento) -> dict`

**Motor principal del ciclo Pomodoro.** Procesa eventos y realiza transiciones.

```
EVENTO: "pomodoro_completado"
├── Registra sesión Pomodoro en BD (vía servicio_sesiones)
├── Si pomodoro < 4: DESCANSO_CORTO (consume siguiente descanso)
├── Si pomodoro = 4: DESCANSO_LARGO
└── Emite evento 'descanso_iniciado'

EVENTO: "descanso_completado"
├── Si era DESCANSO_CORTO: TRABAJANDO (siguiente pomodoro)
├── Si era DESCANSO_LARGO: marca ciclo completado
│   ├── Intenta iniciar siguiente ciclo automáticamente
│   └── Emite evento 'ciclo_completado'
└── Emite evento 'descanso_finalizado'
```

**Ejemplo de ciclo completo:**

```python
iniciar_ciclo(usuario_id)                           # → TRABAJANDO (pom 1/4)
manejar_evento_timer(usuario_id, "pomodoro_completado")  # → DESCANSO_CORTO (5 min)
manejar_evento_timer(usuario_id, "descanso_completado")  # → TRABAJANDO (pom 2/4)
manejar_evento_timer(usuario_id, "pomodoro_completado")  # → DESCANSO_CORTO (5 min)
manejar_evento_timer(usuario_id, "descanso_completado")  # → TRABAJANDO (pom 3/4)
manejar_evento_timer(usuario_id, "pomodoro_completado")  # → DESCANSO_CORTO (5 min)
manejar_evento_timer(usuario_id, "descanso_completado")  # → TRABAJANDO (pom 4/4)
manejar_evento_timer(usuario_id, "pomodoro_completado")  # → DESCANSO_LARGO (30 min)
manejar_evento_timer(usuario_id, "descanso_completado")  # → INACTIVO o nuevo ciclo
```

### Tests: 21 tests en `tests/timer/test_ciclo_pomodoro.py`

| Clase | Tests |
|-------|-------|
| `TestIniciarCiclo` | 8 (creación, config, duplicado, validación) |
| `TestObtenerEstadoCiclo` | 4 (sin ciclo, con ciclo, validación) |
| `TestManejarEventoTimer` | 6 (transiciones, registro sesiones, validación) |
| `TestRegistrarCallback` | 3 (registro, evento inválido, no callable) |

---

## Módulo: Servicio de Sesiones (`src/timer/servicio_sesiones.py`)

### Capa intermedia (clean architecture)

Separa el timer de la BD. El timer NO sabe nada de MongoDB directamente.

```
Timer (ciclo_pomodoro)
    │
    ↓ llama a
Servicio (servicio_sesiones)
    │
    ↓ guarda en
MongoDB (colección "sesiones")
```

### Función: `registrar_sesion_pomodoro(usuario_id, datos_ciclo, duracion_min) -> dict`

Registra una sesión Pomodoro individual en la colección `sesiones`.

```python
sesion = registrar_sesion_pomodoro(
    usuario_id="507f...",
    datos_ciclo={'_id': ..., 'numero_ciclo': 1, 'pomodoro_actual': 1},
    duracion_min=25
)
# {
#     '_id': '...',
#     'usuario_id': ObjectId('...'),
#     'ciclo_id': ObjectId('...'),
#     'numero_ciclo': 1,
#     'tipo_sesion': 'pomodoro',
#     'pomodoro_numero': 1,
#     'inicio': datetime,
#     'duracion_programada_min': 25,
#     'duracion_segundos': 1500,
# }
```

### Tests: 6 tests en `tests/timer/test_servicio_sesiones.py`

---

## Módulo: Gestor de Pausas (`src/pausas/gestor_pausas.py`)

### Reglas del sistema de pausas

```
PAUSAS MANUALES DEL TRABAJADOR:
├── Máximo 2 por jornada
├── Máximo 10 minutos cada una
├── 3ra pausa → ERROR "Máximo alcanzado"
├── Pausa > 10 min → ANOMALÍA "pausa_excedida"
└── No puede iniciar pausa sin ciclo activo
```

### Funciones implementadas (2)

#### 1. `iniciar_pausa(usuario_id) -> dict`

Inicia una pausa manual con validación de todas las reglas.

```python
resultado = iniciar_pausa("507f...")
# {
#     'pausa_id': 'abc123...',
#     'inicio': datetime,
#     'pausas_usadas': 1,
#     'pausas_restantes': 1
# }
```

**Validaciones (en orden):**
1. ¿Hay ciclo activo? → si no, ERROR
2. ¿Hay pausa activa? → si sí, ERROR
3. ¿Ya usó 2 pausas hoy? → si sí, ERROR

#### 2. `finalizar_pausa(usuario_id) -> dict`

Finaliza la pausa activa y registra anomalía si excedió 10 min.

```python
resultado = finalizar_pausa("507f...")
# {
#     'pausa_id': 'abc123...',
#     'duracion_minutos': 8,
#     'excedida': False,
#     'anomalia': None,
#     'pausas_usadas': 1
# }

# Si excedió 10 min:
# {
#     'pausa_id': 'abc123...',
#     'duracion_minutos': 12,
#     'excedida': True,
#     'anomalia': {tipo: 'pausa_excedida', ...},
#     'pausas_usadas': 1
# }
```

**Nueva colección `pausas_manuales`:**

```json
{
    "_id": "ObjectId",
    "usuario_id": "ObjectId",
    "ciclo_id": "ObjectId",
    "inicio": "2026-03-31T11:00:00",
    "fin": "2026-03-31T11:08:00",
    "duracion_minutos": 8,
    "activa": false,
    "excedida": false
}
```

### Tests: 16 tests en `tests/pausas/test_gestor_pausas.py`

| Clase | Tests |
|-------|-------|
| `TestIniciarPausa` | 8 (éxito, 2da pausa, 3ra falla, sin ciclo, pausa activa, validación) |
| `TestFinalizarPausa` | 8 (éxito, sin pausa, excedida con anomalía, no excedida sin anomalía) |

---

## Métricas Finales

### Tests

| Módulo | Tests |
|--------|-------|
| Timer (banco_tiempo) | 20 |
| Timer (estados) | 18 |
| Timer (ciclo_pomodoro) | 21 |
| Timer (servicio_sesiones) | 6 |
| Pausas (gestor_pausas) | 16 |
| **Total FASE 5** | **81** |
| **Total proyecto** | **441** |

### Código

| Métrica | Valor |
|---------|-------|
| Archivos de código creados | 5 |
| Líneas de código | ~480 |
| Archivos de tests creados | 5 |
| Líneas de tests | ~520 |
| Tiempo de ejecución tests | 10.99s |
| Warnings | 0 |

### Colecciones MongoDB nuevas

| Colección | Uso |
|-----------|-----|
| `ciclos_pomodoro` | Ciclos Pomodoro activos y completados |
| `pausas_manuales` | Pausas manuales del trabajador |

---

## Decisiones de Diseño

### 1. Pomodoro configurable por usuario

No se hardcodearon los 25 minutos. El usuario puede configurar `pomodoro_min` en sus parámetros. Los descansos también son configurables dentro de las reglas del banco de tiempo.

### 2. Ciclos adaptables al horario

`calcular_ciclos_jornada()` calcula automáticamente cuántos ciclos caben en la jornada del trabajador, soportando horarios variables (6h, 7h, 8h). Genera ciclos reducidos si sobran suficientes minutos.

### 3. Separación Timer ↔ BD (clean architecture)

`servicio_sesiones.py` actúa como capa intermedia. El timer (`ciclo_pomodoro.py`) emite eventos y llama al servicio, pero nunca accede directamente a MongoDB. Esto permite:
- Testear el timer sin BD real
- Cambiar la BD sin tocar el timer
- FASE 6 conectarse via callbacks sin modificar FASE 5

### 4. Sistema de callbacks para FASE 6

Los eventos se registran con `registrar_callback()`. FASE 6 registrará sus funciones cuando se implemente:
```python
# FASE 6 hará:
from src.timer import registrar_callback
registrar_callback('descanso_iniciado', mostrar_bloqueo_con_otp)
registrar_callback('descanso_finalizado', solicitar_otp)
```

### 5. Colección `ciclos_pomodoro` separada de `sesiones`

`ciclos_pomodoro` agrupa los 4 pomodoros + descansos como unidad.
`sesiones` registra cada pomodoro individual (ya existía).
Esto permite consultar tanto ciclos completos como sesiones individuales.

---

## Puntos de Enganche para FASE 6

| Hook | Cuándo se emite | FASE 6 lo usa para |
|------|----------------|-------------------|
| `descanso_iniciado` | Timer cambia a DESCANSO_CORTO/LARGO | Generar OTP + mostrar pantalla bloqueo |
| `descanso_finalizado` | Countdown descanso llega a 0 | Solicitar OTP al usuario |
| `ciclo_completado` | DESCANSO_LARGO termina + no más ciclos | Mostrar resumen de jornada |
| `anomalia_generada` | Pausa excedida / 3ra pausa | Registrar anomalía en BD |

---

## Próximo Paso

→ **FASE 6: OTP & Bloqueo**
- Generación OTP 6 dígitos con `secrets`
- Hash bcrypt del OTP para verificación
- Bloqueo Windows via `ctypes.windll.user32.LockWorkStation()`
- Pantalla fullscreen CustomTkinter durante descansos
- Verificación OTP con límite de 3 intentos
- Registro de anomalías por OTP expirado / intentos fallidos
- ~6 funciones, ~70+ tests
