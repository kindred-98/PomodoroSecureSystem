# FASE 7A: Interfaz Gráfica — Flujo Completo

**Fecha:** 31 de Marzo de 2026  
**Estado:** ✅ COMPLETADA — 479 TESTS PASANDO (100% backend)  
**Framework:** CustomTkinter 5.2.2  
**Documentación previa:** [FASE_6_OTP_BLOQUEO.md](FASE_6_OTP_BLOQUEO.md)

---

## Resumen Ejecutivo

### Estado del Proyecto Post-FASE 7A

```
████████████████████████████████████████████████████░ 95% Completo
(Generador 100% | BD 100% | Auth 100% | Timer 100% | OTP 100% | UI 7A 100%)
```

| Módulo | Estado | Tests |
|--------|--------|-------|
| **Generador** | ✅ 100% | 202 |
| **Base de Datos** | ✅ 100% | 63 |
| **Autenticación** | ✅ 100% | 95 |
| **Timer & Pausas** | ✅ 100% | 81 |
| **OTP & Bloqueo** | ✅ 100% | 38 |
| **UI — Flujo completo** | ✅ 100% | 0 (visual) |
| **UI — Dashboards avanzados** | ⏳ FASE 7B | 0 |

---

## Arquitectura Implementada

```
src/
├── config/
│   └── colores.py               ✅ Paleta centralizada (30+ colores)
│
├── ui/
│   ├── __init__.py              ✅ Exports: 6 vistas
│   ├── splash.py                ✅ Splash Screen (2-3 seg)
│   ├── login_view.py            ✅ Login funcional
│   ├── registro_view.py         ✅ Registro 4 pasos funcional
│   ├── dashboard_empleado.py    ✅ Timer + acciones
│   ├── bloqueo_view.py          ✅ Fullscreen + OTP
│   └── password_view.py         ✅ Gestión contraseña
│
├── app.py                       ✅ Controlador navegación
└── main.py                      ✅ Entry point
```

---

## Paleta de Colores (`src/config/colores.py`)

Tema oscuro profesional inspirado en Linear/VSCode/Vercel.

### Fondos
| Constante | Hex | Uso |
|-----------|-----|-----|
| `FONDO_PRINCIPAL` | `#1E1E2E` | Fondo general |
| `FONDO_SECUNDARIO` | `#2A2A3E` | Paneles, sidebars |
| `FONDO_CARD` | `#313145` | Tarjetas y elementos |

### Acentos funcionales
| Constante | Hex | Uso |
|-----------|-----|-----|
| `TRABAJO_ACTIVO` | `#7C3AED` | Violeta — pomodoro corriendo |
| `COMPLETADO` | `#10B981` | Verde — OK/completado |
| `AVISO` | `#F59E0B` | Naranja — warning |
| `PELIGRO` | `#EF4444` | Rojo — error/anomalía |
| `INFORMACION` | `#3B82F6` | Azul — info/enlaces |

### Pantalla de bloqueo
| Constante | Hex | Tipo |
|-----------|-----|------|
| `BLOQUEO_CORTO` | `#0F2744` | Azul oscuro |
| `BLOQUEO_LARGO` | `#0F2F1F` | Verde oscuro |
| `BLOQUEO_FIJO` | `#2D1B00` | Naranja oscuro |

---

## Pantalla: Splash (`src/ui/splash.py`)

### Qué muestra
- Emoji 🍅🔐 grande centrado
- Nombre "PomodoroSecure" en JetBrains Mono Bold
- Subtítulo "Sistema de Gestión Segura de Tiempo"
- Barra de progreso animada (2.5 segundos)
- Versión "v1.0.0"

### Flujo
```
Inicio → Splash (animación progreso 0→1) → Login
```

### Integración backend
Ninguna — es puramente visual.

---

## Pantalla: Login (`src/ui/login_view.py`)

### Qué muestra
- Card central (400×420) con fondo `FONDO_CARD`
- Logo + nombre app
- Campo Email (con placeholder)
- Campo Contraseña (con toggle mostrar/ocultar)
- Checkbox "Mostrar contraseña"
- Label de error (rojo, animado)
- Botón "Iniciar Sesión" (violeta)
- Link "¿Primera vez? Regístrate"
- Footer "v1.0.0 — Dicampus"

### Integración backend
```python
from src.auth import iniciar_sesion
resultado = iniciar_sesion(email, contraseña)
# → usuario + token_sesion
```

### Flujo
```
Login → introduce email + pw → clic "Iniciar Sesión"
├── Éxito → Dashboard Empleado
└── Error → label_error muestra mensaje + botón re-habilitado
```

---

## Pantalla: Registro (`src/ui/registro_view.py`)

### Qué muestra — 4 pasos

**Paso 1 — Datos personales:**
- Campo Nombre completo
- Campo Email
- ComboBox Rol (empleado/encargado/supervisor)
- Botón "Siguiente →"

**Paso 2 — Parámetros de contraseña:**
- Slider Longitud (8-128, default 20)
- Toggle mayúsculas (default ON)
- Toggle números (default ON)
- Toggle símbolos (default ON)
- Toggle excluir ambiguos (default OFF)
- Botón "Generar →"

**Paso 3 — Contraseña generada:**
- Aviso ⚠️ "Única vez que la verás"
- Contraseña generada grande (verde)
- Indicador "✅ Muy fuerte — 99%"
- Botón "📋 Copiar al portapapeles"
- Botón "Continuar →"

**Paso 4 — Confirmación:**
- ✅ grande
- "Registro completado"
- Info del usuario (email + rol)
- Botón "Ir al Login →"

### Integración backend
```python
from src.auth import registrar_usuario
resultado = registrar_usuario(email, nombre, rol, parametros)
# → usuario + contraseña_generada
```

---

## Pantalla: Dashboard Empleado (`src/ui/dashboard_empleado.py`)

### Layout
```
┌──────────────────────────────────────────────────────┐
│  HEADER [🍅 PomodoroSecure] [Nombre | Rol]           │
├──────────────────┬───────────────────────────────────┤
│  PANEL LATERAL   │  PANEL CENTRAL                    │
│                  │  ┌─────────────────────────────┐  │
│  📊 Hoy          │  │  🍅 INACTIVO / TRABAJANDO  │  │
│  Ciclos: 0/∞     │  │                             │  │
│  Trabajado: 0h0m │  │       25:00                 │  │
│                  │  │   [████████░░░░░░░░] 50%    │  │
│  ⏸ Pausas        │  │                             │  │
│  ○ ○  (0 usadas) │  │  [▶ Iniciar]  [⏸ Pausar]  │  │
│                  │  └─────────────────────────────┘  │
│  [🔑 Contraseña] │                                   │
│  [🚪 Logout]     │  Próximos descansos:              │
│                  │  Corto 1-4: 5 min / Largo: 30 min│
└──────────────────┴───────────────────────────────────┘
```

### Integración backend
```python
from src.timer import iniciar_ciclo, obtener_estado_ciclo, manejar_evento_timer
from src.pausas import iniciar_pausa, finalizar_pausa

# Iniciar ciclo
iniciar_ciclo(usuario_id)

# Countdown: actualiza cada 1 segundo
# Al llegar a 0: manejar_evento_timer(usuario_id, "pomodoro_completado")
# Al terminar descanso: manejar_evento_timer(usuario_id, "descanso_completado")

# Pausas
iniciar_pausa(usuario_id)
finalizar_pausa(usuario_id)
```

### Flujo del timer
```
[▶ Iniciar Jornada] → estado = TRABAJANDO → countdown 25:00
    ↓ (llega a 0)
    manejar_evento_timer("pomodoro_completado")
    ↓
    estado = DESCANSO → countdown 5:00 (o 30:00 si largo)
    ↓ (llega a 0)
    manejar_evento_timer("descanso_completado")
    ↓
    vuelve a TRABAJANDO

[⏸ Pausar] → iniciar_pausa() → estado = PAUSADO → timer se detiene
[▶ Reanudar] → finalizar_pausa() → estado = TRABAJANDO → timer continúa
```

---

## Pantalla: Bloqueo Fullscreen (`src/ui/bloqueo_view.py`)

### Qué muestra (CTkToplevel — ventana emergente)
- Fullscreen + topmost (siempre encima)
- Color fondo según tipo: azul (corto), verde (largo), naranja (fijo)
- Emoji según tipo: ☕ / 🌴 / 🍽️
- Countdown grande del descanso
- Mensaje motivacional
- Al terminar: campo OTP de 6 dígitos + botón Confirmar
- Label de estado de verificación

### Integración backend
```python
from src.otp import generar_otp, verificar_otp
from src.bloqueo import bloquear_escritorio

# Al iniciar descanso:
otp = generar_otp(usuario_id, ciclo_id)
bloquear_escritorio()
# Muestra código al usuario antes del bloqueo

# Al terminar descanso:
resultado = verificar_otp(usuario_id, codigo_introducido)
# A → correcto → cerrar y continuar
# B → 3 fallos → requiere credenciales
# C → expirado → requiere credenciales
```

### Flujo
```
Descanso iniciado → fullscreen topmost → countdown 5:00
    ↓ (countdown llega a 0)
    Campo OTP aparece → usuario introduce código
    ├── Correcto → cierra ventana, timer reanuda
    ├── Incorrecto → "Quedan X intentos"
    └── 3 fallos → "Introduce credenciales completas"
```

---

## Pantalla: Gestión Contraseña (`src/ui/password_view.py`)

### Qué muestra — 4 opciones en cards

**Card A — Ver contraseña:**
- Campo contraseña de login (para verificación)
- Botón "Ver"
- Resultado: contraseña desencriptada

**Card B — Regenerar:**
- Botón "Regenerar"
- Resultado: nueva contraseña generada

**Card C — Cambio manual:**
- Campo para nueva contraseña
- Botón "Cambiar"
- Validación: debe ser nivel "Muy Fuerte"

**Card D — Exportar:**
- Botón "Exportar"
- FileDialog para seleccionar ruta
- Resultado: archivo .enc creado

### Integración backend
```python
from src.auth import (
    ver_contraseña,
    regenerar_contraseña,
    cambiar_contraseña,
    exportar_contraseña,
)
```

---

## Controlador: App (`src/app.py`)

### Navegación entre vistas
```
main.py
    ↓
PomodoroSecureApp (CTk root)
    ├── SplashView → on_complete → LoginView
    ├── LoginView → on_login → DashboardEmpleado
    │                on_ir_registro → RegistroView
    ├── RegistroView → on_ir_login → LoginView
    ├── DashboardEmpleado → on_logout → LoginView
    │                        on_ver_contraseña → PasswordView
    ├── PasswordView → on_volver → DashboardEmpleado
    └── BloqueoView → on_verificado → DashboardEmpleado (Toplevel)
```

### Estado global
```python
self.usuario_actual = None  # Se establece en login
# Se usa en todas las vistas para llamar al backend
```

---

## Entry Point: `src/main.py`

```python
python src/main.py
```

- Verifica `FERNET_KEY` en variables de entorno
- Crea la app y ejecuta `mainloop()`

---

## Decisiones de Diseño

### 1. Paleta centralizada en `colores.py`

Todos los colores están en un solo archivo. Cambiar el tema requiere modificar solo este archivo.

### 2. Cada vista es un `CTkFrame` (no `CTkToplevel`)

Las vistas principales (login, registro, dashboard) son frames que se intercambian dentro de la ventana raíz. Solo `BloqueoView` es un `CTkToplevel` porque necesita fullscreen + topmost.

### 3. Navigation pattern con callbacks

Cada vista recibe callbacks (`on_login`, `on_logout`, etc.) en lugar de referencias directas al controlador. Esto mantiene las vistas desacopladas.

### 4. Backend no sabe de UI

La UI importa y llama al backend. El backend nunca importa la UI. Los tests del backend corren sin `customtkinter`.

### 5. Sin tests de UI

CustomTkinter es difícil de testear automáticamente. Los tests existentes del backend (479) garantizan que la lógica funciona. La UI es una capa visual sobre funciones ya testeadas.

---

## Métricas

| Métrica | Valor |
|---------|-------|
| Archivos de UI creados | 8 |
| Líneas de UI | ~750 |
| Pantallas implementadas | 6 (splash, login, registro, dashboard, bloqueo, contraseña) |
| Paleta de colores | 30+ constantes |
| Backend tests | 479/479 ✅ |
| Tiempo tests | 17.50s |

---

## Próximo Paso

→ **FASE 7B: Dashboards avanzados**
- Dashboard Encargado (panel de equipo con estados en tiempo real)
- Dashboard Supervisor (gestión global, anomalías, configuración empresa)
- Vista de historial de sesiones
- Configuración de descansos fijos de empresa
