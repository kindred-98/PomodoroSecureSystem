# FASE 6: OTP & Bloqueo — Implementación Completa

**Fecha:** 31 de Marzo de 2026  
**Estado:** ✅ COMPLETADA — 479 TESTS PASANDO (100%)  
**Documentación previa:** [FASE_5_TIMER_POMODORO.md](FASE_5_TIMER_POMODORO.md)

---

## Resumen Ejecutivo

### Estado del Proyecto Post-FASE 6

```
██████████████████████████████████████████████░ 90% Completo
(Generador 100% | BD 100% | Auth 100% | Timer 100% | OTP 100% | UI 0%)
```

| Módulo | Estado | Tests |
|--------|--------|-------|
| **Generador** | ✅ 100% | 202 |
| **Base de Datos** | ✅ 100% | 63 |
| **Autenticación** | ✅ 100% | 95 |
| **Timer & Pausas** | ✅ 100% | 81 |
| **OTP & Bloqueo** | ✅ 100% | 38 |
| **Interfaz Gráfica** | ⏳ Pendiente | 0 |
| **Pipeline** | ⏳ Pendiente | 0 |

---

## Arquitectura Implementada

```
src/
├── otp/
│   ├── __init__.py              ✅ Exports: 4 funciones
│   └── gestor_otp.py            ✅ Generación + verificación + estado
│
├── bloqueo/
│   ├── __init__.py              ✅ Exports: 1 función
│   └── windows_lock.py          ✅ Wrapper ctypes LockWorkStation
```

---

## Módulo: Gestor OTP (`src/otp/gestor_otp.py`)

### Concepto

El OTP (One-Time Password) verifica que hay una persona real delante del ordenador después de cada descanso. No es para desbloquear — es para **validar presencia**.

### Flujo del sistema

```
[Descanso iniciado por timer]
    ↓
Se genera OTP de 6 dígitos (secrets)
Se hashea con bcrypt
Se guarda en MongoDB (colección "eventos_otp")
Se muestra al usuario antes del bloqueo
    ↓
[Pantalla bloqueada — 7 minutos de gracia]
    ↓
Usuario introduce código
    ↓
┌─── ESCENARIO A: Correcto ─────────────────────┐
│ Timer reanuda ✅                                │
│ Evento marcado resuelto=true                    │
└─────────────────────────────────────────────────┘
┌─── ESCENARIO B: 3 intentos fallidos ──────────┐
│ Anomalía "tercer_intento_otp" registrada       │
│ Requiere credenciales completas (email + pw)   │
└─────────────────────────────────────────────────┘
┌─── ESCENARIO C: Expira (7 min) ───────────────┐
│ Anomalía "otp_expirado" registrada             │
│ minutos_retraso calculado                      │
│ Requiere credenciales completas                │
└─────────────────────────────────────────────────┘
```

### Funciones implementadas (4)

#### 1. `generar_otp(usuario_id, ciclo_id=None) -> dict`

Genera un código OTP de 6 dígitos criptográficamente seguro.

```python
resultado = generar_otp("507f...", "ciclo_abc")
# {
#     'codigo': '847291',
#     'expira_en_seg': 420,
#     'evento_id': '...'
# }
```

**Proceso interno:**
1. `secrets.randbelow(900000) + 100000` → siempre 6 dígitos
2. `hashear_contraseña(codigo)` → bcrypt hash
3. Guarda en `eventos_otp` con timestamp de expiración (+7 min)
4. Retorna el código en texto plano (única vez que se ve)

**Nueva colección `eventos_otp`:**

```json
{
    "_id": "ObjectId",
    "usuario_id": "ObjectId",
    "ciclo_id": "ObjectId",
    "otp_hash": "$2b$12$...",
    "timestamp_generado": "2026-03-31T10:30:00",
    "timestamp_expira": "2026-03-31T10:37:00",
    "intentos_fallidos": 0,
    "resuelto": false,
    "minutos_retraso": 0
}
```

#### 2. `verificar_otp(usuario_id, codigo_introducido) -> dict`

Verifica un código OTP contra el hash almacenado. Maneja los 3 escenarios.

```python
# Escenario A: Correcto
resultado = verificar_otp("507f...", "847291")
# {'correcto': True, 'intentos_restantes': 3, 'expirado': False,
#  'requiere_credenciales': False, 'anomalia': None}

# Escenario B: Incorrecto (1er intento)
resultado = verificar_otp("507f...", "000000")
# {'correcto': False, 'intentos_restantes': 2, 'requiere_credenciales': False}

# Escenario B: 3er intento fallido
resultado = verificar_otp("507f...", "999999")
# {'correcto': False, 'intentos_restantes': 0, 'requiere_credenciales': True,
#  'anomalia': {'tipo': 'tercer_intento_otp', ...}}

# Escenario C: Expirado
resultado = verificar_otp("507f...", "847291")
# {'correcto': False, 'expirado': True, 'requiere_credenciales': True,
#  'anomalia': {'tipo': 'otp_expirado', ...}}
```

**Validaciones:**
- Primero verifica expiración (antes de verificar código)
- Si expirado → anomalía `otp_expirado` + minutos de retraso
- Si no expirado → compara código con hash bcrypt
- Si incorrecto → incrementa `intentos_fallidos`
- Si llega a 3 → anomalía `tercer_intento_otp`

#### 3. `obtener_estado_otp(usuario_id) -> dict`

Retorna el estado del OTP activo sin verificarlo.

```python
estado = obtener_estado_otp("507f...")
# {
#     'tiene_otp_activo': True,
#     'expira_en_seg': 312,      ← countdown
#     'intentos_usados': 1,
#     'intentos_restantes': 2
# }
```

Útil para que la UI muestre el countdown de expiración y los intentos restantes.

#### 4. `cancelar_otp(usuario_id) -> bool`

Cancela el OTP activo del usuario.

```python
cancelar_otp("507f...")  # → True (había OTP activo)
cancelar_otp("507f...")  # → False (ya no hay OTP activo)
```

### Seguridad del OTP

```
EL OTP NUNCA se almacena en texto plano:
├── Se genera con secrets.randbelow() (criptográficamente seguro)
├── Se hashea con bcrypt (rounds=12) antes de guardar
├── Solo se muestra al usuario UNA vez (al generarlo)
└── bcrypt.checkpw() para verificar (sin exponer el hash)

EL HASH del OTP se elimina o marca resuelto al usarse correctamente.
```

### Tests: 31 tests en `tests/otp/test_gestor_otp.py`

| Clase | Tests | Cobertura |
|-------|-------|-----------|
| `TestGenerarOtp` | 9 | Generación, formato, hash BD, ciclo_id, validación |
| `TestVerificarOtp` | 11 | Correcto, incorrecto, 2do fallo, 3er fallo+anomalía, expirado, sin activo, validación |
| `TestObtenerEstadoOtp` | 6 | Activo, inactivo, intentos usados, validación |
| `TestCancelarOtp` | 5 | Cancelación, sin OTP, cancelado no verificable, validación |

---

## Módulo: Bloqueo Windows (`src/bloqueo/windows_lock.py`)

### Función: `bloquear_escritorio() -> dict`

Wrapper thin para `ctypes.windll.user32.LockWorkStation()`.

```python
resultado = bloquear_escritorio()
# En Windows exitoso:
# {'bloqueado': True, 'plataforma': 'win32', 'mensaje': '...'}

# En Linux/macOS:
# {'bloqueado': False, 'plataforma': 'linux', 'mensaje': '...'}
```

**Por qué es un módulo separado:**
- Se mockea fácil en tests (no depende de ctypes real)
- Maneja gracefully plataformas no-Windows
- Retorna dict con resultado siempre (nunca excepción)

### Tests: 7 tests en `tests/bloqueo/test_windows_lock.py`

| Clase | Tests |
|-------|-------|
| `TestBloquearEscritorio` | 7 (retorno, Windows éxito, error, Linux, macOS, excepción, campos) |

---

## Integración con FASE 5 (Timer)

Los hooks preparados en FASE 5 se conectan así con FASE 6:

```
FASE 5 emite:                    FASE 6 responde:
──────────────                   ───────────────
descanso_iniciado           →    1. generar_otp(usuario_id, ciclo_id)
    {tipo_descanso,              2. obtener_estado_otp() para countdown
     duracion_min,               3. bloquear_escritorio()
     usuario_id,                 
     ciclo_id}                  

descanso_finalizado          →    1. verificar_otp(usuario_id, codigo)
    {tipo_descanso,              2. Si correcto → timer reanuda
     usuario_id}                 3. Si 3 fallos → anomalía + credenciales
                                 4. Si expira → anomalía + retraso
```

**Patrón de integración (se implementará en FASE 7 UI):**

```python
from src.timer import registrar_callback
from src.otp import generar_otp, verificar_otp
from src.bloqueo import bloquear_escritorio

def al_iniciar_descanso(datos):
    otp = generar_otp(datos['usuario_id'], datos.get('ciclo_id'))
    # mostrar_codigo_en_pantalla(otp['codigo'])  ← FASE 7
    bloquear_escritorio()

def al_terminar_descanso(datos):
    pass  # La UI solicita el OTP y llama a verificar_otp()
```

---

## Nuevas Anomalías del Sistema OTP

Implementadas usando `src.db.anomalias.registrar_anomalia()` (ya existente).

| Tipo | Trigger | Severidad | Datos extra |
|------|---------|-----------|-------------|
| `tercer_intento_otp` | 3 intentos fallidos consecutivos | ALTA | intentos_fallidos: 3 |
| `otp_expirado` | 7 minutos sin validar | ALTA | minutos_retraso |

---

## Métricas Finales

### Tests

| Módulo | Tests |
|--------|-------|
| OTP (gestor_otp) | 31 |
| Bloqueo (windows_lock) | 7 |
| **Total FASE 6** | **38** |
| **Total proyecto** | **479** |

### Código

| Métrica | Valor |
|---------|-------|
| Archivos de código creados | 2 |
| Líneas de código | ~250 |
| Archivos de tests creados | 2 |
| Líneas de tests | ~280 |
| Tiempo de ejecución tests | 17.23s |
| Warnings | 0 |

### Colecciones MongoDB nuevas

| Colección | Uso |
|-----------|-----|
| `eventos_otp` | Códigos OTP generados, hashes, intentos, resolución |

---

## Decisiones de Diseño

### 1. OTP con bcrypt, no Fernet

Se usa bcrypt (igual que contraseñas de login) en lugar de Fernet porque:
- El OTP no necesita ser reversible (solo verificable)
- Reutiliza `hashear_contraseña()` y `verificar_contraseña()` existentes
- Misma seguridad que el sistema de login

### 2. Wrapper separado para LockWorkStation

`windows_lock.py` es un módulo de 30 líneas que solo llama a ctypes. Separado porque:
- Se mockea fácil en tests sin dependencias de Windows
- Maneja plataformas no-Windows gracefully (retorna dict, no excepción)
- No depende de CustomTkinter ni de la UI

### 3. Pantalla fullscreen queda para FASE 7

La pantalla de bloqueo CustomTkinter necesita la UI completa (FASE 7). La lógica OTP es testeable independientemente. La UI solo mostrará el código y el campo de entrada, conectándose a `generar_otp()` y `verificar_otp()`.

### 4. Colección `eventos_otp` separada de `sesiones`

Los eventos OTP son entidades diferentes a las sesiones Pomodoro. Un evento OTP puede existir sin una sesión activa (ej: OTP expirado después de crash). Separar permite consultas independientes.

---

## Próximo Paso

→ **FASE 7: Interfaz Gráfica (CustomTkinter)**
- Splash screen + Login + Registro (4 pasos)
- Dashboard por rol (empleado, encargado, supervisor)
- Pantalla de bloqueo fullscreen durante descansos
- Campo de OTP + campo de credenciales tras fallos
- Timer visual con countdown
- Configuración de descansos fijos de empresa
- ~500+ líneas de UI
