# Preparación previa al taller

## "De junior técnico a senior de negocio — Ciencia de datos con IA agéntica"

> ⏱️ Tiempo estimado de preparación: 20–30 minutos.  
> ⚠️ **Completar ANTES del día del taller.** No habrá tiempo para instalar herramientas durante la sesión.

---

## 1. Requisitos de hardware

- Computador portátil con al menos 8 GB de RAM.
- 5 GB de espacio en disco disponible.
- Conexión a internet (solo para la instalación previa; el taller funciona offline).

---

## 2. Instalar Python 3.11

### macOS

```bash
# Opción 1: Homebrew (recomendado)
brew install python@3.11

# Opción 2: Descarga directa
# https://www.python.org/downloads/release/python-3119/
```

### Windows

1. Descargar el instalador desde: https://www.python.org/downloads/release/python-3119/
2. **Marcar la casilla "Add Python 3.11 to PATH"** durante la instalación.
3. Seleccionar "Install Now".

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### Verificación

```bash
python3.11 --version
# Debe mostrar: Python 3.11.x
```

> En Windows el comando puede ser `python` en lugar de `python3.11`.

---

## 3. Instalar Git

### macOS

```bash
# Viene preinstalado. Si no:
brew install git
```

### Windows

Descargar desde: https://git-scm.com/download/win

Durante la instalación, aceptar las opciones por defecto.

### Linux

```bash
sudo apt install git
```

### Verificación

```bash
git --version
# Debe mostrar: git version 2.x.x
```

---

## 4. Instalar Visual Studio Code (recomendado)

1. Descargar desde: https://code.visualstudio.com/
2. Instalar la extensión **Python** (Microsoft).
3. Instalar la extensión **Kiro** (si está disponible en el marketplace).

> VS Code no es obligatorio, pero facilita la experiencia con Kiro.

---

## 5. Crear cuenta en Kiro e instalar el CLI

### 5.1 Crear cuenta gratuita

1. Ir a: https://kiro.dev
2. Registrarse con tu correo o cuenta de GitHub/Google.
3. La cuenta gratuita incluye **50 interacciones por mes** — suficiente para el taller.

> 💡 Si tienes un código promocional de 500 créditos de prueba, aplícalo durante el registro o en la configuración de tu cuenta.

### 5.2 Instalar Kiro CLI

#### macOS / Linux

```bash
curl -fsSL https://kiro.dev/install.sh | sh
```

#### Windows (PowerShell como administrador)

```powershell
irm https://kiro.dev/install.ps1 | iex
```

### 5.3 Autenticarse

```bash
kiro auth login
```

Se abrirá el navegador para completar la autenticación.

### 5.4 Verificación

```bash
kiro --version
# Debe mostrar la versión instalada

kiro auth status
# Debe mostrar: Authenticated as <tu-email>
```

---

## 6. Clonar el repositorio del taller

```bash
git clone https://github.com/<ORGANIZACION>/de-junior-tecnico-a-senior-de-negocio.git
cd de-junior-tecnico-a-senior-de-negocio
```

> La URL exacta se compartirá antes del taller.

---

## 7. Crear entorno virtual e instalar dependencias

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación, ejecutar primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## 8. Verificar que todo funciona

Ejecutar los siguientes comandos desde la raíz del repositorio con el entorno virtual activo:

```bash
# 1. Python funciona
python --version
# Esperado: Python 3.11.x

# 2. Dependencias instaladas
python -c "import pandas; import numpy; import sklearn; import plotly; import streamlit; print('✅ Dependencias OK')"

# 3. Kiro responde
kiro --version

# 4. Tests pasan (si ya hay tests disponibles)
pytest -q
```

Si todos los comandos funcionan, estás listo para el taller. ✅

---

## 9. Checklist final

| # | Paso | ¿Listo? |
|---|------|---------|
| 1 | Python 3.11 instalado | ☐ |
| 2 | Git instalado | ☐ |
| 3 | VS Code instalado (recomendado) | ☐ |
| 4 | Cuenta de Kiro creada | ☐ |
| 5 | Kiro CLI instalado y autenticado | ☐ |
| 6 | Repositorio clonado | ☐ |
| 7 | Entorno virtual creado y dependencias instaladas | ☐ |
| 8 | Verificación exitosa | ☐ |

---

## Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `python3.11: command not found` | Verificar que Python 3.11 está en el PATH. En Windows usar `python` sin versión. |
| `pip install` falla por permisos | Asegurarse de estar dentro del entorno virtual (`.venv`). |
| PowerShell bloquea activación del venv | Ejecutar `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `kiro auth login` no abre navegador | Copiar la URL que aparece en terminal y pegarla manualmente en el navegador. |
| `ModuleNotFoundError` al importar | Verificar que el venv está activo (`which python` debe apuntar a `.venv/`). |
| Error de SSL al clonar | Verificar conexión a internet o usar `git clone` con HTTPS (no SSH). |

---

## ¿Necesitas ayuda?

Si tienes problemas con la instalación, contacta al instructor antes del día del taller:

- **Correo:** [POR DEFINIR]
- **Canal:** [POR DEFINIR]

> 🚨 **No llegarás a completar el taller si no tienes el entorno listo.** Dedica 20 minutos antes de la sesión para seguir estos pasos.
