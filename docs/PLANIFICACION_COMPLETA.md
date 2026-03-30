# 🍅🔐 POMODORO SECURE SYSTEM
## Documento de Planificación Completa
**Autor:** A.D.E.V. (kindred-98)  
**Módulo:** 2 · Estrategias de Generación de Código con IA · Dicampus  
**Versión del documento:** 1.0  
**Estado:** Planificación — Pre-desarrollo  
**Fecha:** 2026  

---

> Este documento recoge **toda** la planificación, decisiones de diseño, arquitectura técnica, reglas de negocio y estructura del sistema acordadas antes de escribir una sola línea de código. Es la fuente de verdad del proyecto.

---

## ÍNDICE

1. [Origen del Proyecto](#1-origen-del-proyecto)
2. [Descripción General](#2-descripción-general)
3. [Objetivos del Sistema](#3-objetivos-del-sistema)
4. [Stack Tecnológico](#4-stack-tecnológico)
5. [Arquitectura del Sistema](#5-arquitectura-del-sistema)
6. [Sistema de Roles y Credenciales](#6-sistema-de-roles-y-credenciales)
7. [Sistema de Autenticación y Contraseñas](#7-sistema-de-autenticación-y-contraseñas)
8. [Lógica del Pomodoro Timer](#8-lógica-del-pomodoro-timer)
9. [Sistema de Pausas Manuales](#9-sistema-de-pausas-manuales)
10. [Sistema de Bloqueo de Pantalla](#10-sistema-de-bloqueo-de-pantalla)
11. [Sistema OTP de Validación de Presencia](#11-sistema-otp-de-validación-de-presencia)
12. [Sistema de Anomalías](#12-sistema-de-anomalías)
13. [Horario Laboral y Descansos](#13-horario-laboral-y-descansos)
14. [Banco de Tiempo de Descanso](#14-banco-de-tiempo-de-descanso)
15. [Base de Datos MongoDB Atlas](#15-base-de-datos-mongodb-atlas)
16. [Interfaz Gráfica](#16-interfaz-gráfica)
17. [Paleta de Colores y Diseño Visual](#17-paleta-de-colores-y-diseño-visual)
18. [Pantallas de la Aplicación](#18-pantallas-de-la-aplicación)
19. [Encriptación y Seguridad](#19-encriptación-y-seguridad)
20. [Pipeline de Calidad](#20-pipeline-de-calidad)
21. [Estructura del Proyecto](#21-estructura-del-proyecto)
22. [Plan de Commits Incrementales](#22-plan-de-commits-incrementales)
23. [Flujos Completos del Sistema](#23-flujos-completos-del-sistema)
24. [Reglas de Negocio — Resumen Ejecutivo](#24-reglas-de-negocio--resumen-ejecutivo)
25. [Decisiones Técnicas Justificadas](#25-decisiones-técnicas-justificadas)

---

## 1. Origen del Proyecto

Este proyecto nace de la **integración de dos ejercicios prácticos** del Módulo 2 de Dicampus:

- **Ejercicio A:** Generador de Contraseñas Seguras (Python + `secrets` + `string`)
- **Ejercicio B:** Reloj de Cuenta Regresiva — Pomodoro Timer (Python + `time` + `threading`)

La consigna original pedía desarrollar cada uno por separado con 10 commits incrementales cada uno. La decisión de A.D.E.V. fue **integrarlos en un único sistema cohesionado** donde el generador de contraseñas no es un módulo auxiliar, sino el **núcleo del sistema de autenticación**.

El resultado es una aplicación de escritorio profesional para la gestión del tiempo laboral de equipos de programadores, con seguridad real, roles diferenciados y trazabilidad completa.

---

## 2. Descripción General

**PomodoroSecure** es una aplicación de escritorio Windows desarrollada en Python que combina:

1. **Gestión del tiempo de trabajo** mediante la técnica Pomodoro adaptada al entorno laboral europeo de equipos de programación.
2. **Sistema de autenticación segura** donde las contraseñas son generadas por el sistema a partir de parámetros del usuario — nunca elegidas por él.
3. **Control de presencia real** mediante bloqueos de pantalla obligatorios, validación OTP y registro de anomalías.
4. **Panel de supervisión** con visibilidad diferenciada por rol (empleado / encargado / supervisor).

La aplicación corre exclusivamente en **Windows** como ejecutable `.exe` generado con PyInstaller, sin necesidad de instalar Python ni dependencias en el equipo del usuario final.

---

## 3. Objetivos del Sistema

### Objetivos Pedagógicos (Dicampus)
- Practicar Git con commits incrementales y mensajes descriptivos.
- Interactuar con IA para generar, analizar y modificar código.
- Trabajar con `secrets`, `string`, `threading`, `datetime`, `os` y `ctypes`.
- Implementar encriptación real con `cryptography.fernet`.
- Conectar una aplicación Python con MongoDB Atlas.
- Documentar el proceso de asistencia de IA en `docs/asistencia_ia.md`.
- Alcanzar cobertura de tests ≥ 80% con `pytest-cov`.

### Objetivos Funcionales
- Gestionar jornadas laborales de equipos de programación.
- Garantizar el cumplimiento de los ciclos Pomodoro configurados.
- Forzar descansos reales mediante bloqueo total de pantalla.
- Validar la presencia del usuario al retomar el trabajo.
- Registrar y escalar anomalías por jerarquía de roles.
- Generar contraseñas criptográficamente seguras basadas en parámetros del usuario.
- Permitir exportación local de contraseñas encriptadas en JSON.

---

## 4. Stack Tecnológico

### Lenguaje
```
Python 3.12+
```

### Interfaz Gráfica
```
CustomTkinter
└── Tkinter moderno con soporte para temas oscuros/claros
    Elegido por: aspecto profesional, compatible con PyInstaller,
    curva de aprendizaje baja, sin problemas de licencia
```

### Base de Datos
```
MongoDB Atlas (tier gratuito M0 — 512MB)
└── Acceso vía pymongo
    Elegido por: el .exe funciona en cualquier PC con internet
    sin instalar MongoDB localmente
```

### Seguridad y Criptografía
```
cryptography (Fernet)  → encriptación reversible de contraseñas
bcrypt                 → hash de verificación de login
secrets                → generación criptográficamente segura
```

### Sistema Operativo (Windows)
```
ctypes                 → LockWorkStation() — bloqueo nativo Windows
pywin32                → detección de eventos de sesión Windows
winsound               → alarmas sonoras nativas Windows
```

### Concurrencia
```
threading              → timer Pomodoro en hilo secundario
                         el hilo principal mantiene la UI responsiva
```

### Empaquetado
```
PyInstaller            → genera el .exe standalone para Windows
```

### Testing y Calidad
```
pytest                 → framework de tests
pytest-cov             → medición de cobertura (mínimo 80%)
unittest.mock          → mocks para threading, MongoDB y sistema OS
```

---

## 5. Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    POMODORO SECURE SYSTEM                   │
│                  Aplicación Desktop Windows                 │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   UI Layer   │────▶│  Logic Layer │────▶│   Data Layer     │
│ CustomTkinter│     │  (módulos)   │     │  MongoDB Atlas   │
└──────────────┘     └──────────────┘     └──────────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼──┐   ┌──────▼──┐   ┌─────▼───────┐
       │  timer  │   │  auth   │   │  bloqueo    │
       │ .py     │   │  .py    │   │  pantalla   │
       └─────────┘   └─────────┘   └─────────────┘
              │             │             │
       ┌──────▼──┐   ┌──────▼──┐   ┌─────▼───────┐
       │ pausa   │   │ genera  │   │   otp       │
       │ .py     │   │ dor.py  │   │   .py       │
       └─────────┘   └─────────┘   └─────────────┘
                            │
                     ┌──────▼──────┐
                     │ anomalias   │
                     │ .py         │
                     └─────────────┘
```

### Decisión arquitectónica clave: Threading

El Pomodoro Timer usa un **bucle bloqueante** (`time.sleep()` tick a tick). Si corre en el hilo principal congela toda la UI. Por eso:

- **Hilo principal** → UI (CustomTkinter), responde al usuario en todo momento.
- **Hilo secundario** → Timer Pomodoro, corre de forma independiente.
- **Comunicación** → mediante `threading.Event` y callbacks seguros a la UI.

---

## 6. Sistema de Roles y Credenciales

El sistema tiene **tres roles** pensados para equipos de programación con estructura jerárquica real:

### 6.1 Empleado

```
PERMISOS:
├── Acceso a su propio dashboard Pomodoro
├── Ver su historial de sesiones y anomalías propias
├── Configurar sus descansos flexibles (dentro del banco)
├── Ver y gestionar su contraseña (con validación de seguridad)
├── Exportar su contraseña a JSON local encriptado
└── Pausar el timer (máximo 2 veces por jornada, 10 min c/u)

NO PUEDE:
├── Ver información de otros usuarios
├── Modificar descansos fijos (café, comida)
├── Ver anomalías de otros empleados
└── Acceder a configuración de empresa
```

### 6.2 Encargado

```
PERMISOS (además de los de Empleado):
├── Ver el estado en tiempo real de SU equipo
├── Ver anomalías de todos los miembros de su equipo
├── Modificar horarios de sus empleados
├── Recibir notificaciones de anomalías de su equipo
└── Su propio Pomodoro activo con interfaz diferenciada

NO PUEDE:
├── Ver otros equipos
├── Modificar configuración global de empresa
└── Ver usuarios que no sean de su equipo
```

### 6.3 Supervisor / Admin

```
PERMISOS (acceso total):
├── Vista global de todos los equipos en tiempo real
├── Panel de anomalías globales
├── Configuración de horarios de empresa
├── Definir y modificar descansos fijos inmodificables
├── Gestión de usuarios (crear, editar, desactivar)
├── Gestión de equipos y asignación de encargados
├── Estadísticas globales de productividad
└── Su propio Pomodoro activo
```

### 6.4 Interfaz diferenciada por rol

Cada rol tiene un **dashboard distinto** al iniciar sesión:

- **Empleado** → Ve su timer, sus estadísticas, sus pausas disponibles.
- **Encargado** → Ve su timer + panel lateral con estado de su equipo.
- **Supervisor** → Ve su timer + panel de gestión global + anomalías.

---

## 7. Sistema de Autenticación y Contraseñas

### 7.1 Filosofía de diseño

El generador de contraseñas no es una herramienta auxiliar — **es el sistema de autenticación**. Ningún usuario puede elegir su propia contraseña. El sistema la genera a partir de parámetros que el usuario proporciona durante el registro.

Esto garantiza que **todas las contraseñas cumplen el estándar de seguridad del 99%** por definición, sin depender del criterio del usuario.

### 7.2 Flujo de registro — paso a paso

```
PASO 1 — Datos personales:
├── Nombre completo
├── Email (será el identificador de login)
├── Rol (empleado / encargado / supervisor)
└── Equipo al que pertenece

PASO 2 — Parámetros para generación de contraseña:
├── Longitud deseada (8 - 128 caracteres)
├── ¿Incluir mayúsculas? (s/n)
├── ¿Incluir números? (s/n)
├── ¿Incluir símbolos? (s/n)
└── ¿Excluir caracteres ambiguos? (0, O, l, I, 1) (s/n)

PASO 3 — El sistema genera la contraseña:
├── Usa el módulo secrets (criptográficamente seguro)
├── Construye el charset dinámicamente con los parámetros
├── Garantiza al menos 1 carácter de cada tipo seleccionado
├── Evalúa la fortaleza → siempre "Muy fuerte" (99%+)
└── Muestra la contraseña al usuario con opción de copiar

PASO 4 — Confirmación y guardado:
├── El usuario confirma que ha copiado/anotado la contraseña
├── Se almacena encriptada en MongoDB (Fernet)
├── Se almacena el hash en MongoDB (bcrypt) para verificar login
├── Se guardan los parámetros usados para regeneración futura
└── Opción de exportar a JSON local encriptado
```

### 7.3 Por qué dos mecanismos de almacenamiento

```
bcrypt hash:
└── Para verificar el login sin exponer la contraseña
    El sistema compara el hash — nunca ve la contraseña en claro

Fernet encriptado:
└── Para que el usuario pueda VER su contraseña si la olvida
    Solo accesible tras validación de seguridad (ver 7.5)
    La clave Fernet es gestionada por el sistema, no por el usuario
```

### 7.4 Login

```
FLUJO DE LOGIN:
├── Usuario introduce email + contraseña
├── Sistema recupera el hash bcrypt de MongoDB
├── bcrypt.checkpw() → True / False
├── Si True → genera token de sesión, carga dashboard por rol
└── Si False → intento fallido (se registra), mensaje de error
    └── Tras 5 intentos fallidos → bloqueo temporal de cuenta
```

### 7.5 Gestión de contraseña dentro de la app

Una vez logueado, el usuario puede acceder a la sección de gestión de contraseña:

```
OPCIONES DISPONIBLES:

A) VER CONTRASEÑA ACTUAL:
   ├── Requiere validación de seguridad
   ├── Se descifra con Fernet y se muestra en pantalla
   └── Se registra el acceso en MongoDB con timestamp

B) REGENERAR CONTRASEÑA (con nuevos parámetros):
   ├── El usuario proporciona nuevos parámetros
   ├── El sistema genera una nueva contraseña
   ├── Se actualiza en MongoDB (hash + encriptada)
   └── Se ofrece exportar el JSON local actualizado

C) CAMBIO MANUAL DE CONTRASEÑA:
   ├── El usuario introduce la contraseña que quiere usar
   ├── El sistema evalúa la fortaleza
   ├── REQUISITO: debe alcanzar validación del 99%
   │   (equivalente a lo que generan las contraseñas automáticas)
   ├── Si no alcanza el 99% → rechazada con explicación
   └── Si alcanza el 99% → se guarda (hash + encriptada)

D) EXPORTAR A JSON LOCAL:
   ├── Genera un archivo .json encriptado con Fernet
   ├── El archivo solo es legible por la propia aplicación
   └── Se guarda en la carpeta que el usuario elija
```

### 7.6 Algoritmo de evaluación de fortaleza (99%)

El sistema de scoring evalúa:

```
CRITERIOS DE PUNTUACIÓN:

Longitud:
├── < 8 caracteres    → 0 puntos (inválido)
├── 8-11 caracteres   → 10 puntos
├── 12-15 caracteres  → 20 puntos
├── 16-19 caracteres  → 30 puntos
└── 20+ caracteres    → 40 puntos

Diversidad de caracteres:
├── Contiene minúsculas  → +10 puntos
├── Contiene mayúsculas  → +15 puntos
├── Contiene números     → +15 puntos
└── Contiene símbolos    → +20 puntos

Penalizaciones:
├── Caracteres ambiguos presentes → -5 puntos
├── Secuencias comunes (123, abc) → -10 puntos
└── Repetición excesiva (aaa)     → -10 puntos

TOTAL MÁXIMO: 100 puntos
UMBRAL 99%: ≥ 95 puntos
```

Las contraseñas generadas por el sistema **siempre superan este umbral** por construcción. El cambio manual solo se permite si también lo supera.

---

## 8. Lógica del Pomodoro Timer

### 8.1 La técnica Pomodoro adaptada

El sistema implementa la técnica Pomodoro con adaptaciones para el entorno laboral profesional europeo:

```
CICLO POMODORO ESTÁNDAR DEL SISTEMA:

┌─────────────────────────────────────────┐
│  TRABAJO    │ DESCANSO CORTO 1 (5 min)  │
│  (25 min)   ├───────────────────────────┤
│             │ TRABAJO                   │
│             │ DESCANSO CORTO 2 (5 min)  │
│             ├───────────────────────────┤
│             │ TRABAJO                   │
│             │ DESCANSO CORTO 3 (5 min)  │
│             ├───────────────────────────┤
│             │ TRABAJO                   │
│             │ DESCANSO CORTO 4 (5 min)  │
│             ├───────────────────────────┤
│             │ DESCANSO LARGO (30 min)   │
└─────────────┴───────────────────────────┘
Banco total: 5+5+5+5+30 = 50 minutos por ciclo completo
```

### 8.2 Estados del timer

```
ESTADOS POSIBLES:

TRABAJANDO      → timer corriendo, UI activa
    │
    ├──[pausa manual]──────▶ PAUSADO_MANUAL
    │                           (máx 10 min, máx 2/día)
    │
    ├──[llega a 0]────────▶ AVISO_DESCANSO
    │                           (countdown 1 minuto)
    │
    └──[descanso fijo]────▶ DESCANSO_FIJO
                               (inmodificable, pantalla bloqueada)

AVISO_DESCANSO  → 1 minuto de cortesía para guardar trabajo
    │
    └──[expira 1 min]─────▶ PANTALLA_BLOQUEADA

PANTALLA_BLOQUEADA → timer pausado, cuenta de bloqueo activa
    │
    └──[usuario valida]───▶ TRABAJANDO (reanuda)

DESCANSO_FIJO   → pantalla bloqueada, timer pausado
    │
    └──[tiempo cumplido]──▶ VALIDACIÓN_OTP → TRABAJANDO
```

### 8.3 Contadores que el sistema mantiene

```
POR SESIÓN (jornada):
├── tiempo_trabajado_min          → minutos efectivos de trabajo
├── tiempo_descansos_reglados_min → descansos Pomodoro normales
├── tiempo_descansos_fijos_min    → café + comida
├── tiempo_pausas_manuales_min    → pausas manuales del usuario
├── tiempo_bloqueos_min           → tiempo en pantalla bloqueada
├── ciclos_completados            → cuántos ciclos Pomodoro completos
└── pausas_manuales_usadas        → contador (máx 2)

POR CICLO:
├── descansos_cortos_completados  → (0 a 4)
└── descanso_largo_pendiente      → bool
```

### 8.4 Threading — implementación segura

```python
# Concepto de implementación (no código final):

# El timer corre en un hilo separado
hilo_timer = threading.Thread(target=ejecutar_ciclo_pomodoro, daemon=True)

# Eventos para comunicación entre hilos
evento_pausa   = threading.Event()
evento_detener = threading.Event()
evento_bloqueo = threading.Event()

# El hilo principal (UI) controla los eventos
# El hilo del timer los escucha y actúa en consecuencia
```

---

## 9. Sistema de Pausas Manuales

### 9.1 Reglas definitivas

```
REGLAS DE PAUSA MANUAL:

├── Máximo 2 pausas por jornada laboral completa
├── Duración máxima por pausa: 10 minutos
├── La pausa se puede solicitar en cualquier momento
│   durante la fase de TRABAJANDO
│
├── Al pausar:
│   ├── El timer se detiene inmediatamente
│   ├── Se inicia un countdown de 10 minutos visible en UI
│   ├── Se registra la hora de inicio de pausa en BD
│   └── Se muestra en UI: "Pausa X/2 — X:XX restantes"
│
├── Al reanudar (manual, antes de 10 min):
│   ├── El timer reanuda desde donde estaba
│   └── Se registra duración real de la pausa
│
├── Si la pausa supera 10 minutos:
│   ├── ANOMALÍA registrada en MongoDB
│   ├── Alarma sonora en el PC
│   └── Se sigue contando el exceso en el registro
│
└── Si se solicita una 3ª pausa:
    ├── ANOMALÍA registrada inmediatamente
    ├── Se deniega la pausa (el botón queda deshabilitado)
    └── El encargado/supervisor recibe notificación
```

### 9.2 Visualización en UI

```
INDICADOR DE PAUSAS EN DASHBOARD:

[⏸ Pausa] ● ● ○   ← 2 disponibles, 0 usadas
[⏸ Pausa] ● ○ ○   ← 1 disponible, 1 usada
[⏸ Pausa] ○ ○ ○   ← 0 disponibles, botón deshabilitado
```

---

## 10. Sistema de Bloqueo de Pantalla

### 10.1 Filosofía del bloqueo

El bloqueo de pantalla es la garantía de que los descansos se cumplen **de verdad**. No es una sugerencia — es un bloqueo físico de la herramienta de trabajo.

El objetivo es que el usuario descanse, no que encuentre formas de saltarse el sistema.

### 10.2 Implementación técnica (doble capa)

```
CAPA 1 — Bloqueo nativo de Windows:
└── ctypes.windll.user32.LockWorkStation()
    Equivalente a Win+L. Requiere contraseña de Windows.
    No necesita permisos especiales de administrador.

CAPA 2 — Ventana fullscreen topmost (CustomTkinter):
└── Ventana que:
    ├── Ocupa el 100% de la pantalla
    ├── Siempre encima de todo (topmost=True)
    ├── Muestra reloj de descanso con countdown
    ├── Color de fondo acorde al tipo de descanso
    │   ├── Descanso corto → azul suave
    │   ├── Descanso largo → verde suave
    │   └── Descanso fijo (café/comida) → naranja suave
    ├── Mensaje motivacional o informativo
    └── Campo para introducir OTP cuando corresponde

COMBINACIÓN:
Al llegar el momento de bloqueo:
1. Se lanza la ventana fullscreen (CAPA 2)
2. Inmediatamente después: LockWorkStation() (CAPA 1)
3. El usuario ve la pantalla de descanso y luego el lock de Windows
4. Al desbloquear Windows, la ventana fullscreen sigue activa
5. El usuario debe introducir el OTP para retomar el trabajo
```

### 10.3 Aviso previo (1 minuto de cortesía)

```
AVISO DE 1 MINUTO:

Al quedar 60 segundos para el bloqueo:
├── Popup no bloqueante en esquina de pantalla
│   "⚠️ Tu descanso comienza en 60 segundos"
│   "Guarda tu trabajo antes de que se bloquee la pantalla"
├── Sonido de aviso (beep suave, no intrusivo)
├── Countdown visible en la barra de título de la app
└── Al llegar a 0 → bloqueo inmediato (ver 10.2)
```

### 10.4 Casos especiales

```
¿Qué pasa si el usuario cierra la ventana fullscreen?
└── El LockWorkStation() de Windows sigue activo
    El proceso de la app sigue corriendo en background
    Al desbloquear Windows → la app se restaura automáticamente
    y pide el OTP igualmente

¿Ctrl+Alt+Del?
└── No se puede interceptar desde userspace en Windows
    Es una limitación del kernel — aceptada y documentada
    El LockWorkStation() complementa esta limitación

¿El proceso sigue corriendo durante el bloqueo?
└── Sí — como proceso de background (daemon)
    Mantiene la conexión con MongoDB
    Sigue contando el tiempo de bloqueo
    Detecta cuando el usuario vuelve (evento de sesión Windows via pywin32)
```

---

## 11. Sistema OTP de Validación de Presencia

### 11.1 Propósito

El OTP no es solo para desbloquear la pantalla — es para **verificar que hay una persona real delante del ordenador**. Evita que el equipo quede encendido sin nadie y el timer siga contando como si el trabajador estuviera presente.

### 11.2 Generación del OTP

```python
# El OTP se genera con secrets — criptográficamente seguro
import secrets
otp = secrets.randbelow(900000) + 100000  # siempre 6 dígitos
```

```
CUÁNDO SE GENERA EL OTP:
├── Al inicio de cada período de bloqueo programado
├── Se muestra AL USUARIO antes del bloqueo (tiene 1 min para verlo/anotarlo)
│   "Tu código de retorno es: 847291 — expira en 7 minutos"
├── Se guarda en MongoDB (hasheado) con timestamp de expiración
└── Se elimina de MongoDB al ser usado correctamente
```

### 11.3 Flujo completo del OTP

```
FLUJO OTP:

[Aviso 1 minuto]
    ↓
Se genera OTP y se muestra al usuario
"Tu código de retorno: 847291"
    ↓
[Pantalla bloqueada — timer pausado — OTP activo]
    ↓
Usuario vuelve y desbloquea Windows
    ↓
App muestra campo "Introduce tu código de retorno:"
Countdown visible: X:XX restantes (de 7 min)
    ↓
┌─────────────────────────────────────────────┐
│ ESCENARIO A: OTP correcto antes de 7 min    │
│ └── Timer reanuda ✅                        │
│     Sesión continúa normalmente             │
│     Evento registrado en MongoDB            │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ESCENARIO B: OTP incorrecto (intentos)      │
│ ├── Intento 1 fallido → "Incorrecto,        │
│ │                         quedan 2 intentos"│
│ ├── Intento 2 fallido → "Incorrecto,        │
│ │                         queda 1 intento"  │
│ └── Intento 3 fallido →                     │
│     ├── ANOMALÍA registrada en MongoDB      │
│     ├── Alarma sonora intensa               │
│     └── Se piden credenciales completas     │
│         (email + contraseña de login)       │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ESCENARIO C: OTP expira (7 minutos)         │
│ ├── Alarma sonora en el PC                  │
│ ├── ANOMALÍA registrada:                    │
│ │   tipo: "otp_expirado"                    │
│ │   minutos_retraso: X                      │
│ ├── Se piden credenciales completas         │
│ │   (email + contraseña de login)           │
│ └── El retraso queda registrado para        │
│     visibilidad del encargado/supervisor    │
└─────────────────────────────────────────────┘
```

### 11.4 Qué se registra en MongoDB por cada evento OTP

```json
{
  "usuario_id": "ObjectId",
  "sesion_id": "ObjectId",
  "timestamp_generado": "2026-03-15T10:30:00",
  "timestamp_expira": "2026-03-15T10:37:00",
  "intentos_fallidos": 0,
  "resuelto": true,
  "resuelto_con_credenciales": false,
  "minutos_retraso": 0
}
```

---

## 12. Sistema de Anomalías

### 12.1 Tipos de anomalías

```
TIPO 1: tercera_pausa
├── Trigger: usuario solicita una 3ª pausa manual
├── Severidad: MEDIA
└── Notifica a: encargado del equipo

TIPO 2: pausa_excedida
├── Trigger: pausa manual supera los 10 minutos
├── Severidad: MEDIA
└── Notifica a: encargado del equipo

TIPO 3: tercer_intento_otp
├── Trigger: 3 intentos fallidos de introducir el OTP
├── Severidad: ALTA
└── Notifica a: encargado + supervisor

TIPO 4: otp_expirado
├── Trigger: los 7 minutos del OTP expiran sin validar
├── Severidad: ALTA
├── Datos extra: minutos_retraso
└── Notifica a: encargado + supervisor

TIPO 5: retraso_reincorporacion
├── Trigger: credenciales completas requeridas por fallo OTP
├── Severidad: ALTA
└── Notifica a: encargado + supervisor
```

### 12.2 Schema de anomalía en MongoDB

```json
{
  "_id": "ObjectId",
  "usuario_id": "ObjectId",
  "sesion_id": "ObjectId",
  "timestamp": "2026-03-15T11:45:00",
  "tipo": "otp_expirado",
  "detalle": "El usuario no validó presencia en 7 minutos",
  "minutos_exceso": 3,
  "resuelto": false,
  "visto_por_encargado": false,
  "visto_por_supervisor": false
}
```

### 12.3 Visibilidad por rol

```
EMPLEADO:
└── Ve sus propias anomalías en su historial personal

ENCARGADO:
├── Ve todas las anomalías de SU equipo
├── Recibe notificación en tiempo real (badge en UI)
└── Puede marcar anomalías como "revisadas"

SUPERVISOR:
├── Ve todas las anomalías de TODOS los equipos
├── Recibe notificación de anomalías ALTA severidad
└── Puede generar informes de anomalías por período
```

---

## 13. Horario Laboral y Descansos

### 13.1 Jornada laboral estándar

Basada en el estándar real del sector tech europeo (especialmente España):

```
JORNADA TIPO SECTOR TECH EUROPEO:

├── Modalidad: Jornada intensiva (sin partida)
├── Inicio típico: 08:00 o 09:00
├── Fin típico: 15:00 o 16:00
├── Duración: 7 horas efectivas
└── Sin jornada partida — todo continuo con pausas Pomodoro

Cada empresa/equipo configura su horario específico
via el panel del Supervisor.
```

### 13.2 Descansos fijos inmodificables

Definidos por el Supervisor o Admin. Los empleados **no pueden modificarlos**:

```
DESCANSOS FIJOS (ejemplo empresa):

Café mañana:
├── Hora inicio: 10:30
├── Duración: 15 minutos
├── Pantalla: bloqueada
└── OTP requerido al retornar: SÍ

Comida:
├── Hora inicio: 13:00
├── Duración: 30 minutos
├── Pantalla: bloqueada
└── OTP requerido al retornar: SÍ

NOTA LEGAL: el descanso de comida es obligatorio por ley
si la jornada supera las 6 horas continuas (legislación española).
```

### 13.3 Configuración por usuario

```
CAMPOS DE HORARIO EN BD (por usuario):
├── inicio_jornada: "09:00"
├── fin_jornada:    "16:00"
├── zona_horaria:   "Europe/Madrid"
└── descansos_fijos: [referencia a config de empresa]
```

---

## 14. Banco de Tiempo de Descanso

### 14.1 Concepto

Cada ciclo Pomodoro tiene un **banco de 50 minutos** de descanso que el empleado puede redistribuir según sus preferencias, dentro de los límites establecidos.

### 14.2 Reglas del banco — definitivas

```
BANCO TOTAL POR CICLO: 50 minutos

DESCANSOS CORTOS:
├── Cantidad: 4 (fijo — siempre son 4)
├── Mínimo por descanso: 5 minutos
├── Máximo por descanso: 10 minutos
└── Rango total de cortos: 20 min (4×5) → 40 min (4×10)

DESCANSO LARGO:
├── Cantidad: 1 (al final del ciclo)
├── Mínimo: 15 minutos
├── Máximo: 30 minutos
└── Cálculo: 50 - suma(descansos_cortos)

ZONA VÁLIDA de suma de cortos: 20 a 35 minutos
└── Para que el largo quede entre 15 y 30 min

VALIDACIÓN AL CONFIGURAR:
largo_resultante = 50 - (corto1 + corto2 + corto3 + corto4)

Si largo_resultante < 15:
└── "Reduce tus descansos cortos. El largo quedaría 
     en X min (mínimo 15)."

Si largo_resultante > 30:
└── "Aumenta tus descansos cortos. El largo quedaría 
     en X min (máximo 30)."

Si 15 ≤ largo_resultante ≤ 30:
└── Configuración válida ✅
```

### 14.3 Ejemplos válidos

```
ESTÁNDAR EMPRESA:     5 + 5 + 5 + 5 = 20 → largo: 30 ✅
PERSONALIZACIÓN A:    5 + 10 + 10 + 10 = 35 → largo: 15 ✅
PERSONALIZACIÓN B:    8 + 8 + 8 + 8 = 32 → largo: 18 ✅
PERSONALIZACIÓN C:    10 + 10 + 10 + 5 = 35 → largo: 15 ✅

INVÁLIDO:             10 + 10 + 10 + 10 = 40 → largo: 10 ❌ (< 15)
INVÁLIDO:             5 + 5 + 5 + 4 = 19 → corto4 < 5 ❌
```

### 14.4 Cuándo puede configurar el empleado

```
MOMENTOS PERMITIDOS:

1. Al iniciar sesión (antes de empezar la jornada)
   └── Pantalla de configuración previa al dashboard

2. Durante la jornada, antes de que empiece un nuevo ciclo
   └── Botón "Configurar próximo ciclo" visible entre ciclos

RESTRICCIÓN:
└── No se puede modificar durante un ciclo en curso
    Solo aplica para el siguiente ciclo
```

---

## 15. Base de Datos MongoDB Atlas

### 15.1 Por qué Atlas y no local

```
MongoDB Atlas (tier M0 gratuito):
├── ✅ El .exe funciona en cualquier PC con internet
│   sin instalar MongoDB localmente
├── ✅ TLS incluido — conexión segura por defecto
├── ✅ Backups automáticos
├── ✅ 512MB gratuitos — suficiente para miles de usuarios
│   con historial completo de sesiones y anomalías
└── ✅ La connection string va en config del app
```

### 15.2 Colecciones completas

#### 📁 `usuarios`
```json
{
  "_id": "ObjectId",
  "nombre": "Ángel Dev",
  "email": "angel@empresa.com",
  "rol": "empleado",
  "equipo_id": "ObjectId",
  "password_encriptada": "gAAAAAB...",
  "password_hash": "$2b$12$...",
  "parametros_password": {
    "longitud": 20,
    "usar_mayusculas": true,
    "usar_numeros": true,
    "usar_simbolos": true,
    "excluir_ambiguos": true
  },
  "horario": {
    "inicio": "09:00",
    "fin": "16:00",
    "zona_horaria": "Europe/Madrid"
  },
  "configuracion_pomodoro": {
    "descansos_cortos": [5, 5, 5, 5],
    "descanso_largo": 30,
    "banco_total": 50
  },
  "activo": true,
  "fecha_registro": "2026-01-15T08:00:00",
  "ultimo_acceso": "2026-03-15T09:03:00"
}
```

#### 📁 `sesiones`
```json
{
  "_id": "ObjectId",
  "usuario_id": "ObjectId",
  "fecha": "2026-03-15",
  "inicio_jornada": "2026-03-15T09:00:00",
  "fin_jornada": "2026-03-15T16:00:00",
  "ciclos_completados": 4,
  "tiempo_trabajado_min": 340,
  "tiempo_descansos_reglados_min": 80,
  "tiempo_descansos_fijos_min": 45,
  "tiempo_pausas_manuales_min": 15,
  "tiempo_bloqueos_min": 0,
  "pausas_manuales": [
    {
      "inicio": "2026-03-15T11:00:00",
      "fin": "2026-03-15T11:08:00",
      "duracion_min": 8
    }
  ],
  "pausas_manuales_usadas": 1,
  "estado": "completada"
}
```

#### 📁 `anomalias`
```json
{
  "_id": "ObjectId",
  "usuario_id": "ObjectId",
  "sesion_id": "ObjectId",
  "timestamp": "2026-03-15T11:45:00",
  "tipo": "otp_expirado",
  "detalle": "El usuario no validó presencia en 7 minutos tras el descanso",
  "minutos_exceso": 3,
  "resuelto": false,
  "visto_por_encargado": false,
  "visto_por_supervisor": false
}
```

#### 📁 `eventos_otp`
```json
{
  "_id": "ObjectId",
  "usuario_id": "ObjectId",
  "sesion_id": "ObjectId",
  "otp_hash": "$2b$12$...",
  "timestamp_generado": "2026-03-15T10:30:00",
  "timestamp_expira": "2026-03-15T10:37:00",
  "intentos_fallidos": 0,
  "resuelto": true,
  "resuelto_con_credenciales": false,
  "minutos_retraso": 0
}
```

#### 📁 `equipos`
```json
{
  "_id": "ObjectId",
  "nombre": "Equipo Backend",
  "encargado_id": "ObjectId",
  "miembros": ["ObjectId", "ObjectId"],
  "horario_base": {
    "inicio": "09:00",
    "fin": "16:00"
  },
  "descansos_fijos": [
    {
      "nombre": "Café mañana",
      "hora_inicio": "10:30",
      "duracion_min": 15
    },
    {
      "nombre": "Comida",
      "hora_inicio": "13:00",
      "duracion_min": 30
    }
  ],
  "configuracion_pomodoro_base": {
    "descansos_cortos": [5, 5, 5, 5],
    "descanso_largo": 30,
    "banco_total": 50
  }
}
```

---

## 16. Interfaz Gráfica

### 16.1 Framework elegido

**CustomTkinter** — elegido por:
- Aspecto moderno y profesional sin configuración extensa
- Compatible con PyInstaller para generar el .exe
- Soporte nativo para temas oscuros
- Sin problemas de licencia (MIT)
- Curva de aprendizaje baja comparado con PyQt6

### 16.2 Tipo de aplicación

**Aplicación de escritorio completa** con interfaz gráfica en todas las pantallas. No es una CLI con ventana de emergencia — es una app profesional desde el primer pixel.

```
CARACTERÍSTICAS GENERALES DE LA UI:
├── Tema: oscuro (dark mode por defecto)
├── Aspecto: profesional, limpio, colorido
├── Público: programadores — familiarizados con UIs tipo VSCode/Linear
├── Resolución mínima: 1280×720
└── Resolución recomendada: 1920×1080
```

---

## 17. Paleta de Colores y Diseño Visual

### 17.1 Paleta principal

```
TEMA OSCURO PROFESIONAL (inspirado en Linear/VSCode/Vercel):

Fondos:
├── Fondo principal:    #1E1E2E  ← casi negro azulado
├── Fondo secundario:   #2A2A3E  ← paneles y sidebars
└── Fondo cards:        #313145  ← tarjetas y elementos

Acentos funcionales:
├── Trabajo activo:     #7C3AED  ← violeta (Pomodoro corriendo)
├── Completado/OK:      #10B981  ← verde esmeralda
├── Aviso/Warning:      #F59E0B  ← naranja ámbar
├── Peligro/Anomalía:   #EF4444  ← rojo
└── Información:        #3B82F6  ← azul

Texto:
├── Principal:          #F8F8F2  ← blanco suave
└── Secundario:         #94A3B8  ← gris claro

Pantalla de bloqueo (por tipo):
├── Descanso corto:     #0F2744  ← azul oscuro
├── Descanso largo:     #0F2F1F  ← verde oscuro
└── Descanso fijo:      #2D1B00  ← naranja muy oscuro
```

### 17.2 Tipografía

```
Display (títulos grandes):    JetBrains Mono Bold
                              ← reconocible para programadores
                              ← connotación técnica y profesional

Cuerpo (texto normal):        JetBrains Mono Regular
                              ← coherencia visual total
                              ← excelente legibilidad en pantallas

Números (timer):              JetBrains Mono Bold
                              ← monoespaced garantiza que los
                                 números no "bailan" al cambiar
```

---

## 18. Pantallas de la Aplicación

### 18.1 Splash Screen

```
SPLASH SCREEN (2-3 segundos):
├── Fondo: #1E1E2E
├── Centro: Logo PomodoroSecure (🍅🔐)
├── Nombre de la app en JetBrains Mono Bold
├── Versión en texto pequeño
├── Barra de carga animada
└── Transición suave a pantalla de Login
```

### 18.2 Login

```
PANTALLA DE LOGIN:
├── Fondo oscuro con sutil gradiente
├── Card central con:
│   ├── Logo pequeño + nombre app
│   ├── Campo: Email
│   ├── Campo: Contraseña (oculta con toggle ojo)
│   ├── Botón: "Iniciar Sesión" (color acento violeta)
│   ├── Link: "¿Primera vez? Regístrate"
│   └── Mensaje de error animado si credenciales incorrectas
└── Footer: versión + Dicampus
```

### 18.3 Registro — flujo de 4 pasos

```
PASO 1 — Datos personales:
├── Nombre completo
├── Email
├── Rol (dropdown: empleado / encargado / supervisor)
├── Equipo (dropdown con equipos disponibles)
└── Botón: "Siguiente →"

PASO 2 — Parámetros de contraseña:
├── Header explicativo: "Configuraremos tu contraseña segura"
├── Slider: Longitud (8-128)
├── Toggle: ¿Incluir mayúsculas?
├── Toggle: ¿Incluir números?
├── Toggle: ¿Incluir símbolos?
├── Toggle: ¿Excluir caracteres ambiguos (0,O,l,I,1)?
├── Preview en tiempo real del nivel de fortaleza
└── Botón: "Generar mi contraseña →"

PASO 3 — Contraseña generada:
├── Display grande con la contraseña generada
├── Indicador: "✅ Muy fuerte — 99%"
├── Botón: "📋 Copiar al portapapeles"
├── Botón: "💾 Guardar en JSON local"
├── Aviso: "⚠️ Esta es la única vez que la verás así.
│           Guárdala en un lugar seguro."
└── Botón: "He guardado mi contraseña — Continuar →"

PASO 4 — Confirmación:
├── "✅ Registro completado"
├── "Ya puedes iniciar sesión con tu email y contraseña"
└── Botón: "Ir al Login"
```

### 18.4 Dashboard Empleado

```
DASHBOARD EMPLEADO:
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
│  [🍅 PomodoroSecure]    [Ángel Dev | Empleado]  [⚙️] │
├──────────────────┬───────────────────────────────────┤
│  PANEL LATERAL   │  PANEL CENTRAL                    │
│  (izquierda)     │                                   │
│                  │  ┌─────────────────────────────┐  │
│  📊 Hoy:         │  │     🍅 TRABAJANDO           │  │
│  Ciclos: 2/∞    │  │                             │  │
│  Trabajado: 1h32 │  │       24:37                 │  │
│                  │  │   [████████████░░░░] 65%    │  │
│  ⏸ Pausas:       │  │                             │  │
│  ● ● ○  (1 usada)│  │   [⏸ Pausar]  [ℹ️ Info]   │  │
│                  │  └─────────────────────────────┘  │
│  🕐 Jornada:     │                                   │
│  09:00 - 16:00   │  PRÓXIMOS DESCANSOS:              │
│  [████░░░] 55%   │  ├── Descanso 1: 5 min           │
│                  │  ├── Descanso 2: 5 min           │
│  📅 Descansos:   │  ├── Descanso 3: 5 min           │
│  [Configurar]    │  ├── Descanso 4: 5 min           │
│                  │  └── Descanso largo: 30 min      │
│  🔑 Contraseña   │                                   │
│  [Gestionar]     │  DESCANSOS FIJOS HOY:             │
│                  │  ├── ☕ Café:  10:30 (en 1h 12m) │
│  📋 Historial    │  └── 🍽️ Comida: 13:00 (en 3h 42m)│
└──────────────────┴───────────────────────────────────┘
```

### 18.5 Dashboard Encargado

```
DASHBOARD ENCARGADO:
├── Misma estructura que empleado
└── Panel lateral adicional: "Mi Equipo"
    ├── Lista de miembros con estado en tiempo real
    │   ├── 🟢 Trabajando (nombre + tiempo actual)
    │   ├── 🟡 En descanso (nombre + tiempo restante)
    │   ├── 🔴 Con anomalía (nombre + tipo)
    │   └── ⚫ Fuera de jornada
    └── Badge de anomalías pendientes: [🚨 2]
```

### 18.6 Dashboard Supervisor

```
DASHBOARD SUPERVISOR:
├── Panel de gestión principal (sin timer prominente)
├── Vista de todos los equipos
├── Panel de anomalías globales con filtros
├── Acceso a configuración de empresa
│   ├── Gestión de usuarios
│   ├── Gestión de equipos
│   ├── Configuración de horarios
│   └── Configuración de descansos fijos
└── Su timer Pomodoro en panel reducido (sigue activo)
```

### 18.7 Pantalla de Bloqueo (fullscreen topmost)

```
PANTALLA DE BLOQUEO:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                                                         │
│                    🍅 DESCANSO                          │
│                                                         │
│                    04:23                                │
│              tiempo de descanso restante                │
│                                                         │
│        ┌─────────────────────────────────────┐          │
│        │  Aprovecha para estirarte,          │          │
│        │  hidratarte y descansar la vista.   │          │
│        └─────────────────────────────────────┘          │
│                                                         │
│  [Solo visible cuando el tiempo expira:]                │
│                                                         │
│        Introduce tu código de retorno:                  │
│        ┌──────────────────┐                             │
│        │  _ _ _ _ _ _    │  ← campo OTP                │
│        └──────────────────┘                             │
│        ⏱️ El código expira en: 6:43                     │
│                                                         │
│        [Confirmar]                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
Color fondo según tipo:
├── Corto:  #0F2744 (azul oscuro)
├── Largo:  #0F2F1F (verde oscuro)
└── Fijo:   #2D1B00 (naranja oscuro)
```

### 18.8 Gestión de Contraseña

```
PANTALLA GESTIÓN DE CONTRASEÑA:
├── Opción A: Ver contraseña actual
│   ├── Solicita validación (contraseña de login)
│   └── Muestra contraseña desencriptada con opción copiar
├── Opción B: Regenerar con nuevos parámetros
│   ├── Flujo igual que el paso 2-3 del registro
│   └── Actualiza MongoDB + ofrece exportar JSON
├── Opción C: Cambio manual
│   ├── Campo para introducir contraseña deseada
│   ├── Indicador de fortaleza en tiempo real
│   ├── Barra de progreso hacia el 99%
│   └── Solo permite guardar si ≥ 95 puntos
└── Opción D: Exportar JSON local
    ├── Selector de carpeta destino
    └── Genera contraseñas.json encriptado con Fernet
```

---

## 19. Encriptación y Seguridad

### 19.1 Arquitectura de seguridad en capas

```
CAPA 1 — Contraseña de login (verificación):
└── bcrypt con salt automático
    bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
    Nunca se puede revertir — solo verificar

CAPA 2 — Contraseña almacenada (recuperación):
└── Fernet (cryptography library)
    Encriptación simétrica AES-128-CBC + HMAC-SHA256
    La clave Fernet se gestiona por el sistema
    Permite desencriptar para mostrar al usuario

CAPA 3 — OTP (validación de presencia):
└── bcrypt también
    El OTP se hashea antes de guardarse en MongoDB
    Al verificar: bcrypt.checkpw(otp_introducido, otp_hash)

CAPA 4 — Transporte (MongoDB Atlas):
└── TLS/SSL incluido por defecto en Atlas
    La connection string usa mongodb+srv:// (TLS forzado)

CAPA 5 — JSON local:
└── Fernet con la misma clave del sistema
    El archivo solo es legible por la propia app
```

### 19.2 Gestión de la clave Fernet

```
LA CLAVE FERNET:
├── Se genera una vez al configurar la app por primera vez
├── Se almacena en un archivo .key local (fuera del repo)
├── .key está en .gitignore — nunca va al repositorio
├── En el .exe se gestiona via variable de entorno o
│   archivo de configuración cifrado
└── Sin esta clave, los datos en MongoDB son ilegibles
```

### 19.3 Lo que NUNCA se almacena en texto plano

```
NUNCA EN TEXTO PLANO:
├── Contraseñas de usuarios
├── Códigos OTP
├── Connection string de MongoDB (en variables de entorno)
└── Clave Fernet
```

---

## 20. Pipeline de Calidad

### 20.1 Requisito de cobertura

```
REQUISITO: Coverage ≥ 80%
HERRAMIENTAS: pytest + pytest-cov
```

### 20.2 Estructura de tests

```
tests/
├── test_generador.py        → tests del generador de contraseñas
│   ├── test_longitud_valida
│   ├── test_charset_dinamico
│   ├── test_evaluacion_fortaleza
│   ├── test_parametros_borde (longitud 8, longitud 128)
│   └── test_fortaleza_99_porciento
│
├── test_timer.py            → tests del Pomodoro timer
│   ├── test_estados_timer
│   ├── test_calculo_banco_tiempo
│   ├── test_validacion_descansos
│   └── test_transiciones_estado (mock de threading)
│
├── test_pausas.py           → tests del sistema de pausas
│   ├── test_primera_pausa
│   ├── test_segunda_pausa
│   ├── test_tercera_pausa_anomalia
│   └── test_pausa_excedida_anomalia
│
├── test_otp.py              → tests del sistema OTP
│   ├── test_generacion_otp
│   ├── test_otp_correcto
│   ├── test_intentos_fallidos
│   ├── test_tercer_intento_anomalia
│   └── test_expiracion_otp
│
├── test_auth.py             → tests de autenticación
│   ├── test_registro_completo
│   ├── test_login_correcto
│   ├── test_login_incorrecto
│   └── test_evaluacion_fortaleza_manual
│
├── test_banco_tiempo.py     → tests del banco de descansos
│   ├── test_configuracion_valida
│   ├── test_largo_minimo
│   ├── test_largo_maximo
│   └── test_configuracion_invalida
│
└── conftest.py              → fixtures compartidos
    ├── usuario_mock
    ├── sesion_mock
    └── mongodb_mock (unittest.mock)
```

### 20.3 Módulos difíciles de testear — estrategia

```
threading (Timer):
└── Se mockea threading.Event y threading.Thread
    Se testea la lógica, no el threading real

MongoDB:
└── Se mockea pymongo con unittest.mock
    Se testea la lógica de datos, no la conexión real

ctypes (LockWorkStation):
└── Se mockea ctypes.windll
    Se testea que se llama con los parámetros correctos

winsound (alarmas):
└── Se mockea winsound.Beep
    Se testea que se llama en los momentos correctos
```

---

## 21. Estructura del Proyecto

```
pomodoro-secure/
│
├── README.md                      ← descripción + instrucciones uso
├── .gitignore                     ← incluye .key, .env, __pycache__
├── requirements.txt               ← todas las dependencias
├── .env.example                   ← plantilla de variables de entorno
│
├── src/
│   ├── main.py                    ← punto de entrada, splash + login
│   ├── app.py                     ← controlador principal de la app
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login.py               ← lógica de autenticación
│   │   ├── registro.py            ← flujo de registro
│   │   └── sesion.py              ← gestión de sesión activa
│   │
│   ├── generador/
│   │   ├── __init__.py
│   │   ├── generador.py           ← generación de contraseñas
│   │   ├── evaluador.py           ← scoring de fortaleza
│   │   └── exportador.py         ← exportación a JSON local
│   │
│   ├── timer/
│   │   ├── __init__.py
│   │   ├── pomodoro.py            ← lógica del ciclo Pomodoro
│   │   ├── estados.py             ← máquina de estados del timer
│   │   └── banco_tiempo.py       ← gestión del banco de descansos
│   │
│   ├── pausas/
│   │   ├── __init__.py
│   │   └── gestor_pausas.py      ← reglas y control de pausas
│   │
│   ├── bloqueo/
│   │   ├── __init__.py
│   │   ├── pantalla.py            ← ventana fullscreen CustomTkinter
│   │   └── windows_lock.py       ← ctypes LockWorkStation
│   │
│   ├── otp/
│   │   ├── __init__.py
│   │   └── gestor_otp.py         ← generación, hash, verificación
│   │
│   ├── anomalias/
│   │   ├── __init__.py
│   │   └── registro.py            ← registro y notificación
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── conexion.py            ← singleton de conexión Atlas
│   │   ├── usuarios.py            ← CRUD usuarios
│   │   ├── sesiones.py            ← CRUD sesiones
│   │   ├── anomalias.py           ← CRUD anomalías
│   │   └── equipos.py             ← CRUD equipos
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── splash.py              ← pantalla de carga
│   │   ├── login_view.py          ← pantalla de login
│   │   ├── registro_view.py       ← flujo de registro (4 pasos)
│   │   ├── dashboard_empleado.py  ← dashboard empleado
│   │   ├── dashboard_encargado.py ← dashboard encargado
│   │   ├── dashboard_supervisor.py← dashboard supervisor
│   │   ├── bloqueo_view.py        ← pantalla de bloqueo
│   │   ├── password_view.py       ← gestión de contraseña
│   │   └── componentes/           ← widgets reutilizables
│   │       ├── timer_widget.py
│   │       ├── progress_bar.py
│   │       └── notificacion.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py              ← configuración global
│   │   └── colores.py             ← paleta de colores centralizada
│   │
│   ├── seguridad/
│   │   ├── __init__.py
│   │   ├── encriptacion.py        ← Fernet (encriptar/desencriptar)
│   │   └── hashing.py             ← bcrypt (hash/verify)
│   │
│   └── notificaciones/
│       ├── __init__.py
│       └── alertas.py             ← sonidos y alertas visuales
│
├── tests/
│   ├── conftest.py
│   ├── test_generador.py
│   ├── test_timer.py
│   ├── test_pausas.py
│   ├── test_otp.py
│   ├── test_auth.py
│   └── test_banco_tiempo.py
│
├── docs/
│   ├── asistencia_ia.md           ← prompts usados (requisito Dicampus)
│   └── PLANIFICACION_COMPLETA.md  ← este documento
│
└── build/
    └── .gitkeep                   ← aquí irá el .exe generado
```

---

## 22. Plan de Commits Incrementales

La integración de dos proyectos (10 commits cada uno) en uno solo se replanifica en **20 commits** que cuentan una historia coherente de principio a fin.

```
FASE 1 — FUNDAMENTOS (Commits 1-3)

Commit 1: setup-inicial
├── README.md, .gitignore, requirements.txt
├── Estructura de carpetas completa
└── .env.example con variables necesarias

Commit 2: [ai] conexion-mongodb-atlas
├── src/db/conexion.py (singleton)
├── src/config/config.py
└── Test de conexión básico

Commit 3: [ai] modelos-datos-usuarios-equipos
├── src/db/usuarios.py (CRUD)
├── src/db/equipos.py (CRUD)
└── tests/conftest.py con mocks

FASE 2 — AUTENTICACIÓN (Commits 4-6)

Commit 4: [ai] sistema-encriptacion
├── src/seguridad/encriptacion.py (Fernet)
├── src/seguridad/hashing.py (bcrypt)
└── tests/test_auth.py (parcial)

Commit 5: [ai] generador-contrasenas-evaluador
├── src/generador/generador.py
├── src/generador/evaluador.py
└── tests/test_generador.py

Commit 6: [ai] flujo-registro-y-login
├── src/auth/registro.py
├── src/auth/login.py
├── src/auth/sesion.py
└── tests/test_auth.py (completo)

FASE 3 — POMODORO CORE (Commits 7-10)

Commit 7: [ai] banco-tiempo-validacion-descansos
├── src/timer/banco_tiempo.py
└── tests/test_banco_tiempo.py

Commit 8: [ai] maquina-estados-timer
├── src/timer/estados.py
└── tests/test_timer.py (parcial)

Commit 9: [ai] ciclo-pomodoro-threading
├── src/timer/pomodoro.py
└── tests/test_timer.py (completo)

Commit 10: [ai] sistema-pausas-manuales
├── src/pausas/gestor_pausas.py
└── tests/test_pausas.py

FASE 4 — BLOQUEO Y OTP (Commits 11-13)

Commit 11: [ai] gestor-otp
├── src/otp/gestor_otp.py
├── src/db/sesiones.py (eventos_otp)
└── tests/test_otp.py

Commit 12: [ai] bloqueo-pantalla-windows
├── src/bloqueo/windows_lock.py (ctypes)
├── src/bloqueo/pantalla.py (CustomTkinter fullscreen)
└── src/notificaciones/alertas.py

Commit 13: [ai] sistema-anomalias-completo
├── src/anomalias/registro.py
├── src/db/anomalias.py
└── tests integración anomalías + OTP

FASE 5 — INTERFAZ GRÁFICA (Commits 14-17)

Commit 14: [ai] ui-splash-login
├── src/ui/splash.py
├── src/ui/login_view.py
└── src/config/colores.py

Commit 15: [ai] ui-registro-4-pasos
├── src/ui/registro_view.py
└── src/generador/exportador.py

Commit 16: [ai] ui-dashboard-empleado
└── src/ui/dashboard_empleado.py
    (timer widget, panel pausas, progreso jornada)

Commit 17: [ai] ui-dashboards-encargado-supervisor
├── src/ui/dashboard_encargado.py
└── src/ui/dashboard_supervisor.py

FASE 6 — INTEGRACIÓN Y CALIDAD (Commits 18-20)

Commit 18: [ai] ui-bloqueo-gestion-password
├── src/ui/bloqueo_view.py
└── src/ui/password_view.py

Commit 19: pipeline-tests-coverage-80
├── Revisión completa de tests
├── Mocks para todos los módulos externos
└── Coverage ≥ 80% verificado

Commit 20: docs-version-final-ejecutable
├── docs/asistencia_ia.md (completo)
├── README.md (instrucciones uso + ejemplos)
├── Configuración PyInstaller
└── Build del .exe Windows
```

---

## 23. Flujos Completos del Sistema

### 23.1 Flujo de una jornada laboral completa

```
08:55 — Usuario abre el .exe
         └── Splash screen (2 seg) → Login

09:00 — Login correcto
         └── Carga dashboard empleado por rol
             └── Muestra: "Buenos días, Ángel"
             └── Botón: "Iniciar jornada"

09:01 — Usuario pulsa "Iniciar jornada"
         └── Timer Pomodoro arranca en hilo secundario
             └── Estado: TRABAJANDO (violeta)
             └── Countdown: 25:00

09:26 — Timer llega a 0 (primer Pomodoro)
         └── Aviso 1 minuto: ⚠️ "Descanso en 60 seg"

09:27 — Pantalla bloqueada (Descanso corto 1 — 5 min)
         └── OTP generado y mostrado antes del bloqueo
         └── LockWorkStation() ejecutado
         └── Pantalla fullscreen azul oscuro
         └── Countdown: 05:00

09:32 — Descanso termina
         └── Pantalla solicita OTP
         └── Countdown OTP: 07:00

09:33 — Usuario introduce OTP correcto
         └── Timer reanuda → TRABAJANDO
         └── Siguiente Pomodoro: 25:00

10:30 — Descanso fijo: CAFÉ (inmodificable)
         └── Aviso 1 minuto
         └── Pantalla bloqueada (naranja oscuro — 15 min)
         └── OTP requerido al retornar

[... ciclos continúan ...]

13:00 — Descanso fijo: COMIDA (30 min)
         └── Mismo flujo que café

11:00 — El usuario pulsa "⏸ Pausar" (pausa 1/2)
         └── Countdown pausa: 10:00
         └── UI muestra: "Pausa 1/2 — 9:47 restantes"

11:08 — Usuario pulsa "Reanudar"
         └── Pausa 1: 8 minutos → registrada en BD
         └── Timer reanuda

15:58 — Sistema detecta fin de jornada inminente (2 min)
         └── Aviso: "Tu jornada termina en 2 minutos"

16:00 — Fin de jornada
         └── Pantalla resumen:
             ├── Ciclos completados: 5
             ├── Tiempo trabajado: 6h 12m
             ├── Pausas usadas: 1/2
             └── Anomalías: 0
         └── Botón: "Cerrar sesión"
```

### 23.2 Flujo de anomalía — 3 intentos OTP fallidos

```
[Descanso termina → pantalla solicita OTP]
     ↓
Usuario introduce OTP incorrecto (intento 1/3)
     └── "Código incorrecto. Te quedan 2 intentos."
     ↓
Usuario introduce OTP incorrecto (intento 2/3)
     └── "Código incorrecto. Te queda 1 intento. ⚠️"
     ↓
Usuario introduce OTP incorrecto (intento 3/3)
     └── ANOMALÍA guardada en MongoDB:
         tipo: "tercer_intento_otp"
         timestamp: ahora
     └── Alarma sonora intensa
     └── Pantalla: "Acceso bloqueado por 3 intentos fallidos"
     └── Formulario de credenciales completas:
         ├── Campo: Email
         └── Campo: Contraseña
     ↓
Usuario introduce credenciales correctas
     └── ANOMALÍA adicional: "retraso_reincorporacion"
     └── Timer reanuda
     └── Encargado ve badge rojo: [🚨 1 anomalía]
```

---

## 24. Reglas de Negocio — Resumen Ejecutivo

```
CONTRASEÑAS:
├── R1: El usuario NO puede elegir su contraseña en el registro
├── R2: El sistema genera siempre contraseñas con fortaleza ≥ 99%
├── R3: Cambio manual solo si fortaleza ≥ 95 puntos (99%)
├── R4: Las contraseñas se almacenan siempre encriptadas (Fernet)
└── R5: El hash bcrypt es la única forma de verificar login

PAUSAS MANUALES:
├── R6: Máximo 2 pausas por jornada
├── R7: Máximo 10 minutos por pausa
├── R8: La 3ª pausa genera anomalía y se deniega
└── R9: Superar 10 min genera anomalía y alarma

OTP:
├── R10: El OTP se genera con secrets (6 dígitos)
├── R11: El OTP se muestra AL USUARIO antes del bloqueo
├── R12: El OTP expira en 7 minutos
├── R13: Máximo 3 intentos de introducir el OTP
├── R14: El 3er intento fallido genera anomalía
└── R15: El OTP expirado genera anomalía y pide credenciales completas

BANCO DE TIEMPO:
├── R16: Banco total por ciclo: 50 minutos
├── R17: 4 descansos cortos, mínimo 5 min, máximo 10 min cada uno
├── R18: Descanso largo mínimo 15 min, máximo 30 min
├── R19: Suma cortos válida: entre 20 y 35 minutos
└── R20: Solo se puede configurar antes del ciclo, no durante

DESCANSOS FIJOS:
├── R21: Solo el Supervisor/Admin puede definirlos
├── R22: Los empleados no pueden modificarlos ni saltárselos
└── R23: El bloqueo de pantalla es obligatorio en descansos fijos

ROLES:
├── R24: Empleado solo ve su propia información
├── R25: Encargado ve la información de SU equipo
└── R26: Supervisor ve toda la información de la empresa

HORARIO:
├── R27: El horario lo define el Supervisor/Admin por equipo
└── R28: El empleado no puede modificar su horario
```

---

## 25. Decisiones Técnicas Justificadas

| Decisión | Alternativas descartadas | Razón |
|---|---|---|
| CustomTkinter | Tkinter nativo, PyQt6 | Tkinter nativo feo, PyQt6 licencia compleja |
| MongoDB Atlas | MongoDB local | El .exe no requiere instalación de MongoDB |
| Fernet (reversible) | Solo bcrypt | El usuario necesita poder VER su contraseña |
| bcrypt + Fernet | Solo Fernet | Verificar login sin exponer la contraseña |
| threading | asyncio | asyncio no integra bien con tkinter |
| LockWorkStation() + fullscreen | Solo fullscreen | Ctrl+Alt+Del no se puede bloquear desde userspace |
| secrets (no random) | random | random es predecible, no apto para seguridad |
| PyInstaller | cx_Freeze, Nuitka | Mayor comunidad, mejor soporte CustomTkinter |
| OTP de 7 minutos | 5 min, 10 min | 5 min muy justo, 10 min demasiado permisivo |
| Máximo 2 pausas | 3 pausas, sin límite | Balance entre flexibilidad y control laboral |
| JetBrains Mono | Inter, Roboto | Connotación técnica, monoespaciado para timers |

---

## Notas Finales

Este documento es la **fuente de verdad** del proyecto PomodoroSecure. Cualquier decisión de implementación que no esté recogida aquí debe consultarse y añadirse antes de codificarse.

El proyecto integra los dos ejercicios del Módulo 2 de Dicampus en un sistema real, profesional y cohesionado, donde cada módulo cumple una función esencial — no son dos herramientas pegadas, sino un único sistema con identidad propia.

**El generador de contraseñas es el sistema de autenticación.**  
**El Pomodoro Timer es el motor de la jornada laboral.**  
**La seguridad es transversal a todo.**

---

*Documento generado en sesión de planificación con Claude (Anthropic)*  
*A.D.E.V. · kindred-98 · Dicampus Módulo 2*
