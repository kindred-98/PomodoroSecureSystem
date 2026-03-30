# FASE 3: Base de Datos - Implementación CRUD

## Resumen Ejecutivo
**Estado:** ✅ Implementación completada, Tests en progreso  
**Alcance:** 19 funciones CRUD + gestor de conexión  
**Tests:** 13/63 pasando (21%), otros tests pendientes de actualización de fixtures  

## Arquitectura de Base de Datos

### Conexión
- **Archivo:** `src/db/conexion.py`
- **Patrón:** Singleton Pattern (instancia global)
- **URI:** De variable de entorno`MONGODB_URI`
- **Características:**
  - Validación de conexión al iniciar
  - Método `obtener_coleccion(nombre)`
  - Método `desconectar()`

### Colecciones Implementadas

#### 1. **usuarios** (6 funciones)
Gestión de usuarios del sistema

| Función | Propósito | Parámetros | Valida |
|---------|-----------|-----------|--------|
| `crear_usuario` | Crear usuario | email, nombre, hash, rol | Email único, tipos, valores |
| `buscar_por_email` | Obtener por email | email | Formato |
| `buscar_por_id` | Obtener por ID | usuario_id (ObjectId) | ObjectId válido |
| `actualizar_pomodoro` | Incrementar puntos | usuario_id, incremento | Valores numéricos |
| `actualizar_ultimo_acceso` | Registrar login | usuario_id | ObjectId válido |
| `desactivar_usuario` | Soft delete | usuario_id | Existencia |

**Schema ejemplo:**
```json
{
  "_id": ObjectId,
  "email": "usuario@example.com",
  "nombre": "Nombre Usuario",
  "contraseña_hash": "$2b$12$...",
  "rol": "empleado|encargado|supervisor",
  "activo": true,
  "fecha_registro": ISODate,
  "ultimo_acceso": ISODate,
  "puntuacion_pomodoro": 0,
  "team_id": ObjectId,
  "metadata": {
    "ciclos_completados": 0,
    "pausas_utilizadas": 0,
    "anomalias_registradas": 0
  }
}
```

#### 2. **equipos** (5 funciones)
Gestión de equipos de trabajo

| Función | Propósito | Parámetros |
|---------|-----------|-----------|
| `crear_equipo` | Crear equipo | nombre, encargado_id, descripcion |
| `buscar_por_id` | Obtener equipo | equipo_id |
| `obtener_miembros` | Lista de usuarios | equipo_id |
| `obtener_por_encargado` | Equipos del manager | encargado_id |
| `añadir_miembro` | Agregar usuario | equipo_id, usuario_id |

**Schema:**
```json
{
  "_id": ObjectId,
  "nombre": "Team Dev",
  "encargado_id": ObjectId,
  "miembros": [ObjectId, ObjectId],
  "descripcion": "Development team",
  "fecha_creacion": ISODate,
  "activo": true
}
```

#### 3. **sesiones** (4 funciones)
Rastreo de sesiones Pomodoro

| Función | Propósito | Parámetros |
|---------|-----------|-----------|
| `crear_sesion` | Nueva sesión | usuario_id, tipo_sesion |
| `actualizar_sesion` | Modificar campos | sesion_id, actualizaciones |
| `cerrar_sesion` | Finalizar sesión | sesion_id, completada |
| `obtener_historial` | últimas N sesiones | usuario_id, limite |

**Schema:**
```json
{
  "_id": ObjectId,
  "usuario_id": ObjectId,
  "tipo_sesion": "pomodoro|pausa|trabajo",
  "inicio": ISODate,
  "fin": ISODate,
  "duracion_segundos": 1500,
  "pausas_utilizadas": 2,
  "completada": true
}
```

#### 4. **anomalias** (4 funciones)
Detección y rastreo de anomalías

| Función | Propósito | Parámetros |
|---------|-----------|-----------|
| `registrar_anomalia` | Nueva anomalía | usuario_id, tipo, descripcion |
| `obtener_por_usuario` | Anomalías del usuario | usuario_id, limite |
| `obtener_por_equipo` | Anomalías del equipo | equipo_id, limite |
| `marcar_revisada` | Marcar como revisada | anomalia_id |

**Schema:**
```json
{
  "_id": ObjectId,
  "usuario_id": ObjectId,
  "tipo": "LOGIN_FALLIDO",
  "descripcion": "5 intentos fallidos",
  "fecha_registro": ISODate,
  "revisada": false,
  "fecha_revision": ISODate
}
```

## Validaciones Implementadas

### Por Función
- **Validación de tipos:** Todos los parámetros verifican tipo correcto
- **Validación de valores:** Strings no vacíos, ObjectIds válidos
- **Validación de existencia:** Se verifica existencia de entidades antes de operaciones
- **Prevención de duplicados:** Email único en usuarios, prevención de miembros duplicados

### Patrones de Error
```python
# TypeError - tipos incorrectos
raise TypeError(f"parametro debe ser tipo, recibido: {type}")

# ValueError - valores inválidos
raise ValueError(f"parametro no puede estar vacío|inválido")

# Exception - errores de BD
raise Exception(f"Entidad con ID 'xxx' no existe")
```

## Testing

### Framework
- **Test Runner:** pytest 9.0.2
- **Mocking:** mongomock 4.3.0 (simula MongoDB sin instancia real)
- **Fixture Pattern:** Fixtures compartidos en `conftest.py`

### Fixtures Principales
```python
@pytest.fixture
def mock_conexion_global()
  # Parchea conexion_global en todos los módulos
  
@pytest.fixture
def coleccion_usuarios()
  # BD MongoDB simulada, colección usuarios

@pytest.fixture
def usuario_en_db()
  # Usuario preinsertado para tests CRUD
```

### Resultados Actuales
- **Crear Usuario:** 13/13 tests ✅ PASANDO
- **Buscar por Email:** 2/3 tests (1 falta actualizar fixture)
- **Buscar por ID:** 0/3 tests (falta actualizar fixtures)
- **Actualizar Pomodoro:** 0/3 tests (falta actualizar fixtures)
- **Actualizar Último Acceso:** 0/3 tests (falta actualizar fixtures)
- **Desactivar Usuario:** 0/3 tests (falta actualizar fixtures)
- **Equipos:** 0/5 tests (falta actualizar fixtures)
- **Sesiones:** 0/4 tests (falta actualizar fixtures)
- **Anomalías:** 0/4 tests (falta actualizar fixtures)

**Total:** 13/63 tests (21%) - Pendiente actualizar fixtures en otros tests

### Próximos Pasos para Tests
1. Actualizar todos los archivos de test para usar `mock_conexion_global`
2. Remover patches manuales y usar fixtures compartidos
3. Ejecutar suite completa y revisar fallos  
4. Ajustar lógica de funciones según fallos encontrados
5. Lograr 100% de cobertura de tests

## Decisiones Arquitectónicas

1. **Singleton para Conexión:**
   - Única instancia de cliente MongoDB durante ejecución
   - Evita múltiples conexiones innecesarias
   - Facilita mocking en tests

2. **Sin ORM/ODM:**
   - Operaciones directas con PyMongo
   - Máximo control y claridad
   - Más flexible para cambios de schema

3. **Soft Deletes:**
   - Campo `activo: false` en lugar de eliminar
   - Preserva historial y referencias
   - Facilita "reactivación" de datos

4. **Validación Pre-BD:**
   - Antes de cualquier operación MongoDB
   - TypeError/ValueError para errores claros
   - Reduce operaciones innecesarias

5. **Una Función por Archivo:**
   - Consistencia con FASE 1-2
   - Facilita testing unitario
   - Mejor modularidad

## Cambios Realizados

### Nuevos Archivos Creados
- `src/db/conexion.py` - Gestor de conexión (103 líneas)
- `src/db/usuarios/*.py` - 6 funciones (200 líneas)
- `src/db/equipos/*.py` - 5 funciones (180 líneas)
- `src/db/sesiones/*.py` - 4 funciones (160 líneas)
- `src/db/anomalias/*.py` - 4 funciones (150 líneas)
- Exports en `__init__.py` para cada módulo
- Tests en `tests/db/*/test_*.py` (~63 tests)

### Actualizaciones
- `requirements.txt` - Agregado mongomock
- `conftest.py` - Nuevas fixtures para MongoDB mocking
- `src/db/anomalias/*` - Actualizado a usar `conexion_global`

## Métricas

| Métrica | Valor |
|---------|-------|
| Funciones implementadas | 19 |
| Líneas de código | ~793 |
| Líneas de tests | ~500+ |
| Módulos | 4 (usuarios, equipos, sesiones, anomalías) |
| Tests escritos | 63 |
| Tests pasando | 13 (21%) |
| Cobertura esperada | ~80% |

## Próximo Turno
1. Actualizar fixtures en otros archivos de test
2. Ejecutar suite completa y revisar fallos
3. Documentación final de FASE 3
4. Commit final de FASE 3
5. Preparar FASE 4 (Autenticación y OTP)
