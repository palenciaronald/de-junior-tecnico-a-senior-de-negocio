# Preparación para el taller: "De junior técnico a senior de negocio"

Hola,

Mañana tenemos el taller **"De junior técnico a senior de negocio — Ciencia de datos con IA agéntica"**.

En el correo anterior les pedí instalar las herramientas. Ahora les comparto el repositorio y los pasos finales para llegar listos.

Son 10 minutos. Si algo falla, escríbeme hoy.

---

## Lo que ya deben tener (del correo anterior)

- [ ] Python 3.11 instalado
- [ ] Git instalado
- [ ] VS Code instalado
- [ ] Cuenta de Kiro creada
- [ ] Kiro CLI instalado y autenticado

Si les falta algo, revisen el correo anterior.

---

## Paso 1: Clonar el repositorio

```
git clone https://github.com/palenciaronald/de-junior-tecnico-a-senior-de-negocio.git
cd de-junior-tecnico-a-senior-de-negocio
```

---

## Paso 2: Crear entorno virtual e instalar dependencias

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

## Paso 3: Verificar que todo funciona

Con el entorno virtual activo:

```
python -c "import pandas, numpy, sklearn, plotly, streamlit; print('✅ Dependencias OK')"
```

```
kiro --version
```

Si ambos funcionan, estás listo. ✅

---

## Paso 4: Abrir el proyecto en VS Code

```
code .
```

Explora brevemente la estructura. No necesitas entender todo — lo iremos explicando juntos.

---

## ¿Qué contiene el repositorio?

Lo que van a encontrar:

| Carpeta | Qué es |
|---------|--------|
| `docs/product-brief.md` | La definición del problema de negocio |
| `data/raw/` | Los datos de retiros (2 años) |
| `.kiro/agents/` | Los agentes de IA que usaremos |
| `.kiro/steering/` | Contexto y reglas para los agentes |
| `notebooks/templates/` | Plantillas que los agentes completarán |
| `schemas/` | Contratos entre fases |

Lo que **NO** van a encontrar (lo construiremos juntos):

- ❌ Modelo entrenado
- ❌ Dashboard
- ❌ Código de features o decisión
- ❌ Recomendación

Eso lo generamos mañana, en vivo, con los agentes.

---

## Durante el taller

- Cada uno trabaja en su computador siguiendo al instructor.
- No es una competencia ni trabajo en equipos.
- Vamos a ejecutar agentes de IA con prompts cortos.
- El instructor explica qué estamos haciendo y por qué antes de cada paso.

---

## Checklist final

- [ ] Repositorio clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas sin errores
- [ ] `python -c "import pandas..."` muestra ✅
- [ ] Kiro funciona

---

## Si algo falla

| Problema | Solución |
|----------|----------|
| `git clone` falla | Verificar internet. Probar con `git clone https://github.com/...` (HTTPS) |
| `pip install` falla por permisos | Asegurarse de estar dentro del venv (ver `(.venv)` en el prompt) |
| `ModuleNotFoundError` | Activar el venv primero: `source .venv/bin/activate` |
| Python no es 3.11 | Usar `python3.11 -m venv .venv` explícitamente |
| VS Code no abre | No es bloqueante, pueden usar cualquier editor |

---

## Importante

🚨 **Si mañana no tienen el repo clonado y las dependencias instaladas, no podrán seguir el laboratorio.** No habrá tiempo para resolver problemas de instalación durante la sesión.

¡Nos vemos mañana!

[TU NOMBRE]
