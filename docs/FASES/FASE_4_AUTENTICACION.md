# FASE 4: Autenticación — Implementación Completa

**Fecha:** 31 de Marzo de 2026  
**Estado:** ✅ COMPLETADA — 360 TESTS PASANDO (100%)  
**Documentación:** [CORRECCIONES_Y_LIMPIEZA_PRE_FASE4.md](CORRECCIONES_Y_LIMPIEZA_PRE_FASE4.md) — Limpieza previa realizada

---

## Resumen Ejecutivo

### Estado del Proyecto Post-FASE 4

```
████████████████████████████████░░░░░░░░░░░░░░ 65% Completo
(Generador 100% | DB 100% | Auth 100% | Timer 0% | OTP 0% | UI 0%)
```

| Módulo | Estado | Tests |
|--------|--------|-------|
| **Generador** | ✅ 100% | 202 |
| **Base de Datos** | ✅ 100% | 63 |
| **Autenticación** | ✅ 100% | 95 |
| **Timer & Pausas** | ⏳ Pendiente | 0 |
| **OTP & Bloqueo** | ⏳ Pendiente | 0 |
| **Interfaz Gráfica** | ⏳ Pendiente | 0 |
| **Pipeline** | ⏳ Pendiente | 0 |

---

## Arquitectura Implementada

```
src/
├── seguridad/
│   ├── __init__.py              ✅ Exports: 5 funciones
│   └── encriptacion.py          ✅ bcrypt + Fernet + tokens
│
├── auth/
│   ├── __init__.py              ✅ Exports: 10 funciones
│   ├── registro.py              ✅ Flujo 4 pasos
│   ├── login.py                 ✅ Verificación + sesión
│   ├── logout.py                ✅ Cierre por token
│   ├── sesion.py                ✅ CRUD sesiones activas
│   ├── ver_contraseña.py        ✅ Ver con validación
│   ├── regenerar_contraseña.py  ✅ Nuevos parámetros
│   ├── cambiar_contraseña.py    ✅ Manual con validación
│   └── exportar_contraseña.py   ✅ JSON encriptado
```

---

## Módulo: Seguridad (`src/seguridad/encriptacion.py`)

### Funciones implementadas (5)

#### 1. `hashear_contraseña(contraseña: str) -> str`

Genera un hash bcrypt irreversible para verificación de login.

```python
hash_pw = hashear_contraseña("MiContraseña123!")
# → "$2b$12$..." (hash bcrypt, 60 caracteres)
```

- Usa `bcrypt.gensalt(rounds=12)` para salt automático
- Cada hash es único aunque la contraseña sea la misma
- No reversible — solo verificable

#### 2. `verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool`

Verifica si una contraseña coincide con un hash bcrypt.

```python
verificar_contraseña("MiContraseña123!", hash_pw)  # → True
verificar_contraseña("Otra", hash_pw)                # → False
```

- Retorna `False` en caso de error (no lanza excepción)
- Maneja tipos inválidos graciosamente

#### 3. `cifrar(texto: str) -> str`

Encripta un texto usando Fernet (AES-128-CBC + HMAC-SHA256).

```python
cifrado = cifrar("contraseña_secreta")
# → "gAAAAABl..." (base64)
```

- La clave se lee de `FERNET_KEY` en variables de entorno
- Cada cifrado produce un resultado diferente (IV aleatorio)
- Lanza `ValueError` si `FERNET_KEY` no está configurada

#### 4. `descifrar(texto_cifrado: str) -> str`

Desencripta un texto previamente cifrado con Fernet.

```python
descifrar(cifrado)  # → "contraseña_secreta"
```

- Lanza `ValueError` si el texto es inválido o la clave es incorrecta

#### 5. `generar_token_sesion() -> str`

Genera un token de sesión criptográficamente seguro.

```python
token = generar_token_sesion()
# → "a1b2c3d4..." (64 caracteres hex)
```

- Usa `secrets.token_hex(32)` — criptográficamente seguro
- Cada token es único

### Tests: 17 tests en `tests/seguridad/test_encriptacion.py`

| Clase | Tests | Cobertura |
|-------|-------|-----------|
| `TestHashearContraseña` | 4 | Hash válido, único, validación tipos |
| `TestVerificarContraseña` | 4 | Correcta, incorrecta, tipos inválidos |
| `TestCifrarDescifrar` | 7 | Roundtrip, unicidad, validación, error |
| `TestGenerarTokenSesion` | 3 | Longitud, formato hex, unicidad |

---

## Módulo: Auth — Registro (`src/auth/registro.py`)

### Función: `registrar_usuario(email, nombre, rol, parametros_contraseña) -> dict`

Flujo completo de 4 pasos integrando el generador de contraseñas.

```
PASO 1: Valida datos personales (email, nombre, rol)
    ↓
PASO 2: Genera contraseña con parámetros del usuario
    ↓
PASO 3: Crea hash (bcrypt) + encripta (Fernet)
    ↓
PASO 4: Guarda en MongoDB
```

```python
resultado = registrar_usuario(
    email="nuevo@empresa.com",
    nombre="Nuevo Usuario",
    rol="empleado",
    parametros_contraseña={
        "longitud": 16,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False
    }
)
# resultado = {
#     'usuario': {...documento MongoDB...},
#     'contraseña_generada': 'K#mW7$hPq9xN2zB!'
# }
```

### Validaciones

- Email, nombre y rol deben ser string no vacío
- Rol debe ser "empleado", "encargado" o "supervisor"
- Email debe ser único (verifica duplicados en BD)
- Parámetros de contraseña validados por `generar_contraseña()`

### Almacenamiento en BD

El usuario queda con estos campos de seguridad:

```json
{
    "contraseña_hash": "$2b$12$...",           // bcrypt para login
    "contraseña_encriptada": "gAAAAABl...",    // Fernet para recuperación
    "parametros_contraseña": {...}             // Para regeneración futura
}
```

### Tests: 14 tests en `tests/auth/test_registro.py`

| Clase | Tests |
|-------|-------|
| `TestRegistroValidacion` | 7 (email, nombre, rol, parámetros) |
| `TestRegistroExito` | 7 (completo, BD, longitud, duplicados, roles) |

---

## Módulo: Auth — Login (`src/auth/login.py`)

### Función: `iniciar_sesion(email, contraseña) -> dict`

```
1. Busca usuario por email en MongoDB
2. Verifica que el usuario está activo
3. Compara contraseña con hash bcrypt
4. Actualiza último acceso
5. Genera token de sesión y lo guarda en BD
6. Retorna usuario + token
```

```python
resultado = iniciar_sesion("usuario@empresa.com", "K#mW7$hPq9xN2zB!")
# resultado = {
#     'usuario': {...},
#     'token_sesion': 'a1b2c3d4...' (64 chars hex)
# }
```

### Manejo de errores

- Email inexistente → `Exception("Credenciales incorrectas")`
- Contraseña incorrecta → `Exception("Credenciales incorrectas")`
- Usuario desactivado → `Exception("Usuario desactivado")`

> Nota: no se diferencia entre email inexistente y contraseña incorrecta por seguridad (evita enumeración de usuarios).

### Tests: 10 tests en `tests/auth/test_login.py`

| Clase | Tests |
|-------|-------|
| `TestLoginValidacion` | 4 (tipos, vacíos) |
| `TestLoginCredenciales` | 4 (éxito, email incorrecto, pw incorrecto, desactivado) |
| `TestLoginSesion` | 2 (token en BD, último acceso) |

---

## Módulo: Auth — Sesión (`src/auth/sesion.py`)

### Funciones (3)

#### `crear_sesion(usuario_id, token_sesion) -> dict`

Crea un documento de sesión activa en la colección `sesiones_auth`.

```python
sesion = crear_sesion(
    usuario_id="507f1f77bcf86cd799439011",
    token_sesion="a1b2c3d4..."
)
# → {'_id': ..., 'activa': True, ...}
```

#### `verificar_sesion(token_sesion) -> dict`

Verifica un token y retorna el usuario asociado.

- Verifica que la sesión existe y está activa
- Verifica expiración (8 horas máximo)
- Verifica que el usuario sigue activo
- Marca sesiones expiradas como inactivas automáticamente

#### `cerrar_sesion_por_token(token_sesion) -> bool`

Cierra una sesión activa (marca `activa: False`).

### Tests: 12 tests en `tests/auth/test_sesion.py`

| Clase | Tests |
|-------|-------|
| `TestCrearSesion` | 6 (éxito, validación tipos, IDs inválidos) |
| `TestVerificarSesion` | 5 (válida, inexistente, cerrada, validación) |
| `TestCerrarSesionPorToken` | 3 (éxito, no existe, validación) |

---

## Módulo: Auth — Logout (`src/auth/logout.py`)

### Función: `cerrar_sesion(token_sesion) -> bool`

Wrapper que delega a `cerrar_sesion_por_token()`.

```python
cerrar_sesion("a1b2c3d4...")  # → True
```

### Tests: 6 tests en `tests/auth/test_logout.py`

| Clase | Tests |
|-------|-------|
| `TestLogoutValidacion` | 2 (tipos, vacíos) |
| `TestLogoutExito` | 4 (cierra, token inexistente, sesión ya cerrada, login→logout) |

---

## Módulo: Auth — Ver Contraseña (`src/auth/ver_contraseña.py`)

### Función: `ver_contraseña(usuario_id, contraseña_login) -> str`

Permite al usuario ver su contraseña almacenada, pero requiere verificar su identidad primero.

```python
contraseña = ver_contraseña(
    usuario_id="507f1f77bcf86cd799439011",
    contraseña_login="MiPasswordDeLogin"
)
# → "K#mW7$hPq9xN2zB!" (desencriptada)
```

### Flujo

1. Busca usuario por ID
2. Verifica contraseña de login contra hash bcrypt
3. Desencripta `contraseña_encriptada` con Fernet
4. Retorna la contraseña en texto plano

### Tests: 8 tests en `tests/auth/test_ver_contraseña.py`

| Clase | Tests |
|-------|-------|
| `TestVerContraseñaValidacion` | 5 (tipos, vacíos, ID inválido) |
| `TestVerContraseñaExito` | 3 (correcta, login incorrecto, usuario no existe) |

---

## Módulo: Auth — Regenerar Contraseña (`src/auth/regenerar_contraseña.py`)

### Función: `regenerar_contraseña(usuario_id, nuevos_parametros) -> dict`

Genera una nueva contraseña con parámetros diferentes y actualiza la BD.

```python
resultado = regenerar_contraseña(
    usuario_id="507f1f77bcf86cd799439011",
    nuevos_parametros={
        "longitud": 20,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": True
    }
)
# → {'nueva_contraseña': 'XyZ9!@Bw$qR3nK7mP1tV', 'mensaje': '...'}
```

### Actualiza en BD

- `contraseña_hash` — nuevo hash bcrypt
- `contraseña_encriptada` — nueva versión Fernet
- `parametros_contraseña` — nuevos parámetros guardados

### Tests: 7 tests en `tests/auth/test_regenerar_contraseña.py`

---

## Módulo: Auth — Cambiar Contraseña Manual (`src/auth/cambiar_contraseña.py`)

### Función: `cambiar_contraseña(usuario_id, nueva_contraseña) -> dict`

Permite al usuario elegir su propia contraseña, pero **requiere nivel "Muy Fuerte"** (≥80 puntos en el sistema de scoring).

```python
# Contraseña débil → RECHAZADA
cambiar_contraseña(id, "abc")
# → ValueError: La contraseña debe ser nivel 'Muy Fuerte'. Nivel actual: Débil (2/100)

# Contraseña muy fuerte → ACEPTADA
cambiar_contraseña(id, "K#mW7$hPq9xN2zB!Lw4T")
# → {'mensaje': 'Contraseña cambiada exitosamente', 'fortaleza': {...}}
```

### Tests: 9 tests en `tests/auth/test_cambiar_contraseña.py`

| Clase | Tests |
|-------|-------|
| `TestCambiarContraseñaValidacion` | 5 (tipos, vacíos, ID) |
| `TestCambiarContraseñaFortaleza` | 2 (débil rechazada, normal rechazada) |
| `TestCambiarContraseñaExito` | 3 (fuerte aceptada, hash actualizado, usuario no existe) |

---

## Módulo: Auth — Exportar Contraseña (`src/auth/exportar_contraseña.py`)

### Función: `exportar_contraseña(usuario_id, ruta_destino) -> str`

Exporta la contraseña a un archivo JSON encriptado con Fernet.

```python
ruta = exportar_contraseña(
    usuario_id="507f1f77bcf86cd799439011",
    ruta_destino="/home/usuario/backup"
)
# → "/home/usuario/backup.enc"
```

### Contenido del archivo

El archivo `.enc` contiene un JSON cifrado con Fernet:

```json
{
    "email": "usuario@empresa.com",
    "nombre": "Nombre Usuario",
    "contraseña": "K#mW7$hPq9xN2zB!",
    "parametros": {...},
    "exportado_en": "backup.enc"
}
```

Solo la propia aplicación (con la misma `FERNET_KEY`) puede leer este archivo.

### Tests: 8 tests en `tests/auth/test_exportar_contraseña.py`

| Clase | Tests |
|-------|-------|
| `TestExportarContraseñaValidacion` | 5 (tipos, vacíos, ID, directorio) |
| `TestExportarContraseñaExito` | 3 (archivo creado, contenido legible, usuario no existe) |

---

## Métricas Finales

### Tests

| Módulo | Tests |
|--------|-------|
| Seguridad (encriptacion) | 17 |
| Auth (registro) | 14 |
| Auth (login) | 10 |
| Auth (logout) | 6 |
| Auth (sesion) | 12 |
| Auth (ver_contraseña) | 8 |
| Auth (regenerar_contraseña) | 7 |
| Auth (cambiar_contraseña) | 9 |
| Auth (exportar_contraseña) | 8 |
| **Total FASE 4** | **95** |
| **Total proyecto** | **360** |

### Código

| Métrica | Valor |
|---------|-------|
| Archivos de código creados | 9 |
| Líneas de código | ~530 |
| Archivos de tests creados | 10 |
| Líneas de tests | ~650 |
| Tiempo de ejecución tests | 10.48s |
| Warnings | 0 |

### Dependencias utilizadas

| Paquete | Uso |
|---------|-----|
| `bcrypt` | Hash irreversible de contraseñas |
| `cryptography` (Fernet) | Encriptación reversible para recuperación |
| `secrets` | Generación de tokens criptográficamente seguros |
| `bson` (ObjectId) | Manejo de IDs de MongoDB |

---

## Decisiones de Diseño

### 1. Colección separada para sesiones de auth

Se usó `sesiones_auth` en lugar de reutilizar la colección `sesiones` existente. Las sesiones Pomodoro y las sesiones de autenticación son entidades diferentes con propósitos distintos.

### 2. FERNET_KEY en variable de entorno

La clave Fernet se lee de `os.getenv('FERNET_KEY')` en cada operación de cifrado/descifrado, no se cachea. Esto permite que los tests la configuren dinámicamente sin afectar otros tests.

### 3. Logout marca como inactiva, no elimina

Las sesiones cerradas se marcan `activa: False` en lugar de eliminarse. Esto permite auditoría futura de sesiones.

### 4. Expiración de sesión: 8 horas

Las sesiones expiran automáticamente después de 8 horas de inactivación, alineado con jornadas laborales típicas.

### 5. Cambio manual requiere "Muy Fuerte"

El cambio manual de contraseña requiere nivel "Muy Fuerte" (≥80 puntos) para mantener el estándar del sistema donde todas las contraseñas generadas automáticamente son de este nivel.

---

## Próximo Paso

→ **FASE 5: Timer & Pomodoro Core**
- Máquina de estados del timer
- Ciclo Pomodoro con threading
- Sistema de pausas manuales (máx 2 × 10 min)
- Banco de tiempo de descansos (50 min por ciclo)
- ~6-7 funciones, ~60+ tests
