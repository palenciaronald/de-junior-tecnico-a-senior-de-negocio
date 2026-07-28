# Preparación para el taller: "De junior técnico a senior de negocio"

Hola,

El próximo [FECHA] tendremos el taller **"De junior técnico a senior de negocio — Ciencia de datos con IA agéntica"**.

Para aprovechar al máximo las 2 horas de sesión, necesito que llegues con tu entorno de trabajo listo. Son unos 20 minutos de preparación. Si tienes algún problema, escríbeme antes del taller.

Un día antes de la sesión les compartiré el repositorio con el código del taller. Por ahora solo necesitan instalar las herramientas.

---

## Lo que vamos a hacer

Vamos a construir un producto de datos completo usando inteligencia artificial agéntica como copiloto. No es una competencia ni un hackathon — cada uno sigue el mismo ejercicio guiado en su computador.

**Necesitas traer:**
- Tu portátil (mínimo 8 GB RAM, 5 GB de disco libre).
- Cargador.
- Conexión a internet para la preparación previa.

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

## Paso 3: Instalar un editor de código

Recomiendo **Visual Studio Code**: https://code.visualstudio.com/

Instalar la extensión **Python** (de Microsoft) desde el marketplace.

---

## Paso 4: Crear tu cuenta de Kiro (gratis)

1. Ir a https://kiro.dev
2. Registrarte con tu correo, GitHub o Google.
3. La cuenta gratuita incluye **50 interacciones mensuales** — es suficiente para el taller.

> 💡 Si recibiste un código promocional de créditos, aplícalo en la configuración de tu cuenta después de registrarte.

---

## Paso 5: Instalar Kiro CLI

**macOS / Linux:**
```
curl -fsSL https://kiro.dev/install.sh | sh
```

**Windows (PowerShell como administrador):**
```
irm https://kiro.dev/install.ps1 | iex
```

**Autenticarse:**
```
kiro auth login
```
Se abrirá tu navegador. Completa el login.

**Verificar:**
```
kiro --version
kiro auth status
```
Debe decir "Authenticated as [tu correo]".

---

## Paso 6: Verificar que Python funciona con un entorno virtual

Solo para confirmar que puedes crear entornos virtuales sin problemas:

**macOS / Linux:**
```
python3.11 -m venv test-venv
source test-venv/bin/activate
python --version
deactivate
rm -rf test-venv
```

**Windows (PowerShell):**
```
python -m venv test-venv
.\test-venv\Scripts\Activate.ps1
python --version
deactivate
Remove-Item -Recurse -Force test-venv
```

> Si PowerShell bloquea la activación, ejecutar primero:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

Si ves la versión de Python sin errores, estás listo.

---

## Checklist

- [ ] Python 3.11 instalado y funcionando
- [ ] Git instalado
- [ ] Editor de código instalado (VS Code recomendado)
- [ ] Cuenta de Kiro creada
- [ ] Kiro CLI instalado y autenticado
- [ ] Puedo crear entornos virtuales sin error

---

## Si algo falla

| Problema | Solución |
|----------|----------|
| `python3.11: command not found` | Verificar PATH. En Windows usar solo `python`. |
| PowerShell no activa el venv | Ejecutar el comando de ExecutionPolicy mencionado arriba. |
| `kiro auth login` no abre navegador | Copiar la URL de la terminal y pegarla en el navegador. |
| Homebrew no encontrado (macOS) | Instalar desde https://brew.sh |
| Git no reconocido (Windows) | Reiniciar la terminal después de instalar Git. |

---

## ¿Y el repositorio del taller?

Lo compartiré un día antes de la sesión con las instrucciones para clonarlo e instalar las dependencias del proyecto. Por ahora solo necesitan tener las herramientas listas.

---

## Importante

🚨 **Si no tienes las herramientas instaladas, no podrás seguir el laboratorio práctico.** La segunda hora es completamente hands-on y no habrá tiempo para solucionar problemas de instalación.

Si tienes cualquier duda, escríbeme a ropalencia@unal.edu.co antes del 28/07/2026.

¡Nos vemos en el taller!

[TU NOMBRE]

