# Preparación completa para el taller: "De junior técnico a senior de negocio"

Hola,

Mañana tenemos el taller **"De junior técnico a senior de negocio — Ciencia de datos con IA agéntica"**.

Para poder ejecutar con éxito todo el taller necesitamos tener las siguientes herramientas instaladas y el repositorio configurado. Son unos 20–30 minutos. Si algo falla, escríbeme hoy.

---

## Lo que vamos a hacer

Vamos a construir un producto de datos completo usando inteligencia artificial agéntica como copiloto. No es una competencia ni un hackathon — cada uno sigue el mismo ejercicio guiado en su computador.

**Necesitas traer:**
- Tu portátil (mínimo 8 GB RAM, 5 GB de disco libre).
- Cargador.

---

## Paso 1: Instalar Python 3.11

**macOS:**
```
brew install python@3.11
```

**Windows:**
- Descargar de https://www.python.org/downloads/release/python-3119/
- ⚠️ Marcar "Add Python 3.11 to PATH" durante la instalación.

**Linux (Ubuntu/Debian):**
```
sudo apt update && sudo apt install python3.11 python3.11-venv python3.11-dev
```

**Verificar:**
```
python3.11 --version
```
Debe mostrar `Python 3.11.x`. En Windows puede ser solo `python --version`.

---

## Paso 2: Instalar Git

- **macOS:** Ya viene instalado. Si no: `brew install git`
- **Windows:** Descargar de https://git-scm.com/download/win (opciones por defecto).
- **Linux:** `sudo apt install git`

**Verificar:**
```
git --version
```

---

## Paso 3: Instalar VS Code

Descargar de https://code.visualstudio.com/

Instalar la extensión **Python** (de Microsoft) desde el marketplace.

---

## Paso 4: Crear cuenta de Kiro e instalar CLI

### Crear cuenta (gratis)

1. Ir a https://kiro.dev
2. Registrarse con correo, GitHub o Google.
3. La cuenta gratuita incluye **50 interacciones mensuales** — suficiente para el taller.

> 💡 Si recibiste un código promocional de créditos, aplícalo en la configuración de tu cuenta.

### Instalar Kiro CLI

**macOS / Linux:**
```
curl -fsSL https://kiro.dev/install.sh | sh
```

**Windows (PowerShell como administrador):**
```
irm https://kiro.dev/install.ps1 | iex
```

### Autenticarse

```
kiro auth login
```
Se abrirá el navegador. Completa el login.

**Verificar:**
```
kiro --version
kiro auth status
```
Debe decir "Authenticated as [tu correo]".

---

## Paso 5: Clonar el repositorio del taller

```
git clone https://github.com/palenciaronald/de-junior-tecnico-a-senior-de-negocio.git
cd de-junior-tecnico-a-senior-de-negocio
```

---

## Paso 6: Crear entorno virtual e instalar dependencias

**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell):**
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

> Si PowerShell bloquea la activación:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Paso 7: Verificar que todo funciona

Con el entorno virtual activo, ejecutar:

```
python -c "import pandas, numpy, sklearn, plotly, streamlit; print('✅ Dependencias OK')"
```

```
kiro --version
```

Si ambos funcionan, estás listo. ✅

---

## ¿Qué contiene el repositorio?

Lo que van a encontrar:

| Carpeta/Archivo | Qué es |
|----------------|--------|
| `docs/product-brief.md` | La definición del problema de negocio |
| `data/raw/` | Los datos de retiros (2 años) |
| `.kiro/agents/` | Los agentes de IA que usaremos |
| `.kiro/steering/` | Contexto y reglas para los agentes |
| `notebooks/templates/` | Plantillas que los agentes completarán |

Lo que **NO** van a encontrar (lo construiremos juntos en el taller):

- ❌ Modelo entrenado
- ❌ Dashboard
- ❌ Código de features ni decisión
- ❌ Recomendación de liquidez

Eso lo generamos mañana, en vivo, con los agentes.

---

## Checklist final

- [ ] Python 3.11 instalado
- [ ] Git instalado
- [ ] VS Code instalado
- [ ] Cuenta de Kiro creada
- [ ] Kiro CLI instalado y autenticado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y dependencias instaladas
- [ ] Verificación exitosa (`import pandas...` + `kiro --version`)

---

## Si algo falla

| Problema | Solución |
|----------|----------|
| `python3.11: command not found` | Verificar PATH. En Windows usar solo `python`. |
| `git clone` falla | Verificar internet y que Git esté instalado. |
| PowerShell no activa el venv | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip install` falla por permisos | Asegurarse de estar dentro del venv (`(.venv)` en el prompt). |
| `kiro auth login` no abre navegador | Copiar la URL de la terminal y pegarla en el navegador. |
| `ModuleNotFoundError` | Activar el venv primero: `source .venv/bin/activate` |
| Homebrew no encontrado (macOS) | Instalar desde https://brew.sh |

---

## Importante

🚨 **Si mañana no tienes todo instalado y funcionando, no podrás seguir el laboratorio práctico.** La segunda hora es completamente hands-on y habrá poco tiempo para resolver problemas de instalación.

Si tienes cualquier duda, escríbeme hoy a ropalencia@unal.edu.co

¡Nos vemos mañana!

Ronald Palencia

