# Correcciones y Limpieza Pre-FASE 4

**Fecha:** 31 de Marzo de 2026  
**Estado:** ✅ COMPLETADO  
**Tests:** 265 pasando antes de FASE 4

---

## Contexto

Antes de iniciar FASE 4 (Autenticación), se realizó una revisión completa del proyecto que identificó varios problemas técnicos acumulados. Este documento registra todas las correcciones aplicadas.

---

## 1. Eliminación de Archivos Duplicados (Inglés)

Se identificaron 4 archivos que eran versiones antiguas en inglés, creadas durante la refactorización inicial a español pero nunca eliminadas.

### Archivos eliminados

| Archivo | Equivalente en español | Razón |
|---------|----------------------|-------|
| `src/generador/construir_charset.py` | `construir_juego_caracteres.py` | Duplicado |
| `src/generador/generar_password.py` | `generar_contraseña.py` | Duplicado |
| `src/generador/mezclar_password.py` | `mezclar_contraseña.py` | Duplicado |
| `src/generador/asegurar_tipos.py` | `asegurar_tipos_caracteres.py` | Duplicado |

### Verificación

Se confirmó mediante `grep` que ningún archivo del proyecto importaba estos archivos duplicados. Solo se importaban entre ellos mismos.

---

## 2. Migración de `datetime.utcnow()` deprecado

`datetime.utcnow()` está deprecado desde Python 3.12 y se eliminará en futuras versiones. Se migró a `datetime.now(timezone.utc)` que es la forma correcta y compatible con todas las versiones.

### Archivos modificados (código fuente)

| Archivo | Línea afectada |
|---------|---------------|
| `src/db/usuarios/crear_usuario.py` | `fecha_registro` |
| `src/db/usuarios/actualizar_ultimo_acceso.py` | `ultimo_acceso` |
| `src/db/equipos/crear_equipo.py` | `fecha_creacion` |
| `src/db/sesiones/crear_sesion.py` | `inicio` |
| `src/db/sesiones/cerrar_sesion.py` | `fin` |
| `src/db/anomalias/registrar_anomalia.py` | `fecha_registro` |
| `src/db/anomalias/marcar_revisada.py` | `fecha_revision` |

### Archivos modificados (tests y config)

| Archivo | Cambio |
|---------|--------|
| `conftest.py` | Fixtures `usuario_en_db`, `equipo_en_db`, `sesion_en_db` |
| `tests/db/usuarios/test_actualizar_ultimo_acceso.py` | Comparaciones de timestamp |
| `tests/db/usuarios/test_buscar_por_email.py` | Datos de prueba |

### Detalle técnico

```python
# ANTES (deprecado)
from datetime import datetime
datetime.utcnow()

# DESPUÉS (correcto)
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

### Problema encontrado

mongomock devuelve datetime naive (sin timezone), lo que causaba un `TypeError` al comparar con datetime aware en un test. Se solucionó normalizando la comparación:

```python
if ts.tzinfo is None:
    ahora_antes = ahora_antes.replace(tzinfo=None)
```

**Resultado:** 44 warnings eliminados → 0 warnings.

---

## 3. Corrección de Typo en Nombre de Base de Datos

### Problema

En `src/db/conexion.py:54` el nombre de la base de datos tenía un typo:

```python
# ANTES
self._base_datos = self._cliente['pomodoreso_secure']

# DESPUÉS
self._base_datos = self._cliente['pomodoro_secure']
```

---

## 4. Eliminación de Credencial Expuesta

### Problema

El archivo `docs/SOLUCION_SONAR_CREDENCIALES.md` contenía el nombre completo del cluster MongoDB Atlas (`nroyjcn.mongodb.net`), lo cual expone información de infraestructura.

### Solución

Se reemplazó el nombre real del cluster por un placeholder:

```markdown
<!-- ANTES -->
MONGODB_URI=mongodb+srv://PomodoroSecureSystem:YOUR_MONGODB_PASSWORD@tucluster.nroyjcn.mongodb.net/?appName=tuCluster

<!-- DESPUÉS -->
MONGODB_URI=mongodb+srv://PomodoroSecureSystem:YOUR_MONGODB_PASSWORD@tucluster.xxxxx.mongodb.net/?appName=tuCluster
```

---

## 5. Relleno de `src/db/__init__.py`

### Problema

El archivo `src/db/__init__.py` estaba completamente vacío, impidiendo imports como:

```python
from src.db import crear_usuario, conexion_global
```

### Solución

Se agregaron todos los exports del módulo db:

```python
from .conexion import ConexionMongoDB, conexion_global
from .usuarios import (crear_usuario, buscar_por_email, buscar_por_id,
                       actualizar_pomodoro, actualizar_ultimo_acceso,
                       desactivar_usuario)
from .equipos import (crear_equipo, obtener_miembros,
                      obtener_por_encargado, añadir_miembro)
from .sesiones import (crear_sesion, actualizar_sesion,
                       cerrar_sesion, obtener_historial)
from .anomalias import (registrar_anomalia, obtener_por_usuario,
                        obtener_por_equipo, marcar_revisada)
```

19 funciones + la conexión exportadas correctamente.

---

## 6. Migración de `print()` a `logging`

### Problema

`src/db/conexion.py` usaba `print()` para mensajes de estado, lo cual no es apropiado para código de producción.

### Solución

```python
# ANTES
print("✅ Conectado a MongoDB Atlas")
print("✅ Desconectado de MongoDB")

# DESPUÉS
import logging
logger = logging.getLogger(__name__)
logger.info("Conectado a MongoDB Atlas")
logger.info("Desconectado de MongoDB")
```

---

## 7. Corrección de Imports Inline

### Problema

Dos archivos tenían `import math` dentro de funciones en lugar de al inicio del archivo, rompiendo la convención del proyecto.

### Archivos corregidos

**`src/generador/evaluar_fortaleza.py`:**
```python
# ANTES: import math dentro de la función (línea 147)
# DESPUÉS: import math al inicio del archivo
```

**`src/generador/calcular_puntuacion.py`:**
```python
# ANTES: import math dentro de calcular_puntuacion() Y generar_y_evaluar()
# DESPUÉS: import math al inicio del archivo, eliminados los 2 inline
```

---

## 8. Refactorización del Fixture `mock_conexion_global`

### Problema

Al agregar los patches de los módulos auth, se excedió el límite de Python de context managers anidados en un solo `with` (`SyntaxError: too many statically nested blocks`).

### Solución

Se refactorizó usando `contextlib.ExitStack`:

```python
from contextlib import ExitStack

@pytest.fixture
def mock_conexion_global(conexion_mongodb_mock):
    modulos_db = [...19 módulos...]
    modulos_auth = [...7 módulos...]

    with ExitStack() as stack:
        for modulo in modulos_db + modulos_auth:
            stack.enter_context(
                patch(f'{modulo}.conexion_global', conexion_mongodb_mock)
            )
        yield conexion_mongodb_mock
```

Esto permite agregar nuevos módulos al patch simplemente añadiendo su nombre a la lista.

---

## Resultado Final

| Métrica | Antes | Después |
|---------|-------|---------|
| **Tests** | 265 | 265 (sin cambios) |
| **Warnings** | 44 | 0 |
| **Archivos duplicados** | 4 | 0 |
| **Deprecation warnings** | 44 | 0 |
| **Typos** | 1 | 0 |
| **Credenciales expuestas** | 1 | 0 |
| **__init__.py vacíos funcionales** | 1 | 0 |
| **print() en producción** | 2 | 0 |
| **Imports inline** | 3 | 0 |

El proyecto quedó limpio y listo para FASE 4.
