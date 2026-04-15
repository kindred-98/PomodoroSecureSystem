# ContraseñaDashboard - Documentación

## Descripción

Módulo de gestión de contraseña accesible desde todos los roles (Empleado, Encargado, Supervisor). Permite ver, generar, cambiar y exportar la contraseña personal del usuario.

## Ubicación

```
src/ui/password_view.py
```

## Secciones del Dashboard

### 1. 👁️ Ver Contraseña Actual

Permite visualizar la contraseña actual del usuario.

**Campos:**
- PIN de 6 dígitos (input)
- Botón "🔍 Ver"

**Flujo:**
1. El usuario introduce su PIN de 6 dígitos
2. Presiona "Ver"
3. El sistema verifica el PIN
4. Si es correcto, muestra la contraseña desencriptada

**Validaciones:**
- PIN obligatorio
- PIN debe ser válido (coincidir con el del día)

---

### 2. 🔐 Generar PIN de 6 Dígitos

Genera un PIN temporal para poder ver la contraseña.

**Características:**
- Botón "🔑 Generar PIN"
- **Bloqueo de 1 hora** entre generaciones
- Botón "📋 Copiar" para copiar al portapapeles
- Muestra el PIN generado en pantalla

**Flujo:**
1. Usuario presiona "Generar PIN"
2. Sistema verifica si pasó 1 hora desde el último PIN
3. Si no pasó, muestra tiempo restante
4. Si sí pasó, genera nuevo PIN
5. PIN se muestra una sola vez
6. Botón queda bloqueado por 1 hora

---

### 3. 🔑 Frase Semilla de Recuperación

Frase de 12 palabras para recuperar la cuenta en caso de pérdida.

**Características:**
- Botón "🔑 Generar Frase"
- **Bloqueo de 90 días** entre generaciones
- Botón "📋 Copiar" para copiar al portapapeles
- Solo se muestra una vez al generar

**Importante:**
> Esta frase es CRÍTICA para recuperación. El usuario debe guardarla en un lugar seguro externo (gestor de contraseñas, papel, etc).

---

### 4. 🔐 Contraseña Segura

Genera una contraseña aleatoria y segura automáticamente.

**Características:**
- Botón "🔄 Generar"
- Botón "📋 Copiar" para copiar al portapapeles
- No requiere parámetros (usa valores por defecto seguros)
- Longitud: 16 caracteres
- Incluye: mayúsculas, números, símbolos

**Configuración por defecto:**
- Longitud: 16
- Mayúsculas: Sí
- Números: Sí
- Símbolos: Sí
- Excluir ambiguos: Sí

---

### 5. 🔧 Contraseña Personalizada

Genera contraseña usando los propios caracteres del usuario.

**Campos:**
- Semilla (input) - mínimo 8 caracteres
- Botón "Generar"

**Flujo:**
1. Usuario introduce su semilla
2. Presiona "Generar"
3. Sistema mezcla los caracteres
4. Genera nueva contraseña segura

---

### 6. ✏️ Cambio Manual

Cambia la contraseña manualmente verificando la actual.

**Campos:**
- Contraseña actual (input, oculto)
- Nueva contraseña (input)
- Repetir nueva contraseña (input)
- Botón "✓ Cambiar Contraseña" (debajo de Repetir)

**Validaciones:**
- Todos los campos son obligatorios
- Nueva y Repetir deben ser iguales
- La nueva debe tener al menos 80 puntos de fortaleza (Muy Fuerte)
- La actual debe ser correcta

---

### 7. 💾 Exportar Datos

Exporta los datos del usuario (sin encriptar) en archivo legible.

**Botones:**
- "Exportar TXT" - Archivo de texto plano
- "Exportar JSON" - Archivo JSON

**Contenido exportado:**
- Usuario (email)
- Fecha de exportación
- Contraseña
- Frase Semilla (si existe)

---

## Estilo Visual

### Fuente
- **Comic Sans MS** en todo el dashboard

### Emojis por Sección
| Sección | Emoji |
|---------|-------|
| Ver contraseña | 👁️ |
| Generar PIN | 🔐 |
| Frase Semilla | 🔑 |
| Contraseña Segura | 🔐 |
| Personalizada | 🔧 |
| Cambio manual | ✏️ |
| Exportar | 💾 |

### Botones Uniformes
- **Altura:** 40px
- **Ancho variable** según función
- Estados hover activos

### Colores
| Elemento | Color |
|---------|-------|
| Botón Generar PIN | #9B59B6 (morado) |
| Botón Frase Semilla | #E7952B (naranja) |
| Botón Cambiar | #10B981 (verde) |
| Botones secundarios | #313145 |

---

## Funciones del Módulo

### _ver_contraseña()
Verifica PIN y muestra contraseña.

### _generar_pin()
Genera nuevo PIN con bloqueo de 1 hora.

### _generar_frase_semilla()
Genera frase semilla con bloqueo de 90 días.

### _regenerar()
Genera contraseña segura automática.

### _generar_personalizada()
Genera contraseña con semilla del usuario.

### _cambiar_manual()
Cambia contraseña con verificación.

### _exportar_txt()
Exporta a archivo TXT legible.

### _exportar_json()
Exporta a archivo JSON legible.

### _copiar_pin(), _copiar_frase(), _copiar_segura()
Funciones para copiar al portapapeles.

---

## Validaciones de Seguridad

1. **PIN:**
   - Solo 1 cada hora
   - Se guarda con hash en BD

2. **Frase Semilla:**
   - Solo 1 cada 90 días
   - Hash guardado en BD

3. **Cambio manual:**
   - Requiere contraseña actual
   - Nueva debe ser "Muy Fuerte" (≥80 pts)
   - Nueva debe repetirse

---

## Archivos Relacionados

```
src/
├── ui/
│   └── password_view.py          # Interfaz
├── auth/
│   ├── pin_diario.py             # Lógica PIN
│   └── frase_semilla.py         # Lógica frase
└── config/
    └── colores.py             # Colores
```

---

## Notas

- Todos los roles ven las mismas opciones
- La contraseña se almacena encriptada en la BD (Fernet)
- La exportación es legible solo para el usuario
- La frase semilla es el método de recuperación último