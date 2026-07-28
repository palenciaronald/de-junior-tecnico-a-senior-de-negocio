# Hoja de Ruta — Laboratorio Práctico (60 minutos)

## "De junior técnico a senior de negocio — Ciencia de datos con IA agéntica"

> Formato: el instructor explica → el participante ejecuta con Kiro → inspecciona → decide GO/NO-GO.

---

## Preparación (antes del taller)

```bash
git clone https://github.com/palenciaronald/de-junior-tecnico-a-senior-de-negocio.git
cd de-junior-tecnico-a-senior-de-negocio
git checkout workshop-start
python3 -m venv .venv
source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Fase 0 — Verificación de entorno (2 min)

**El instructor dice:** "Verificamos que todo funcione antes de empezar."

**El participante ejecuta:**
```bash
python -c "import pandas, numpy, sklearn, plotly, streamlit; print('✅ OK')"
kiro --version
```

**Resultado esperado:** Imports exitosos + Kiro responde.

---

## Fase 1 — Gate de negocio (5 min) 🧠

**El instructor dice:** "Antes de escribir código, validamos que entendemos el problema. No es solo 'predecir retiros' — es decidir cuánto reservar."

**El participante ejecuta en Kiro:**
```
/agent business-understanding
```

**Prompt:**
> Revisa docs/product-brief.md y valida si el problema de negocio está listo para desarrollo técnico. Confirma problema, decisión, usuario, KPI y entregable.

**El agente produce:**
- `reports/00_business_understanding.md`
- `manifests/00_business_understanding.json`

**Pregunta del instructor:** "¿Cuál es la diferencia entre la predicción y la decisión?"

**GO/NO-GO:** El KPI es medible, la decisión es explícita → **GO**

---

## Fase 2 — Entendimiento de datos (10 min) 📊

**El instructor dice:** "Ahora el agente va a explorar los datos. No es un EDA infinito — cada gráfico responde una pregunta."

**El participante ejecuta:**
```
/agent data-understanding
```

**Prompt:**
> Analiza data/raw/daily_withdrawals.csv. Genera un notebook con EDA orientada a decisiones: calidad, estacionalidad, tendencia y viabilidad predictiva.

**El agente produce:**
- `notebooks/01_data_understanding.ipynb` (ejecutado)
- `reports/01_data_understanding.md`
- `manifests/01_data_understanding.json`

**El participante inspecciona el notebook** (abrirlo en VS Code o Jupyter).

**Preguntas del instructor:**
- "¿Cuántos días tenemos?"
- "¿Qué pasa los sábados vs domingos?"
- "¿Los festivos suben o bajan los retiros?"
- "¿Hay tendencia?"

**GO/NO-GO:** Datos completos, patrones claros → **GO**

---

## Fase 3 — Preparación de datos (12 min) 🔧

**El instructor dice:** "Ahora construimos las features. La regla de oro: NUNCA usar información del futuro. Todo lag y rolling debe usar shift(1)."

**El participante ejecuta:**
```
/agent data-preparation
```

**Prompt:**
> Prepara los datos para modelado: genera features de lags, rolling y calendario. Separa train/validation/test cronológicamente. Valida ausencia de leakage.

**El agente produce:**
- `notebooks/02_data_preparation.ipynb` (ejecutado)
- `data/processed/train.csv`, `validation.csv`, `test.csv`
- `manifests/02_data_preparation.json`

**Preguntas del instructor:**
- "¿Por qué usamos shift(1) antes del rolling?"
- "¿Por qué el split es cronológico y no aleatorio?"
- "¿El test set está bloqueado — por qué?"

**GO/NO-GO:** Sin leakage, split correcto → **GO**

---

## Fase 4 — Torneo de modelos (10 min) 🏆

**El instructor dice:** "Ahora comparamos modelos. No buscamos el más sofisticado — buscamos el que soporte mejor la decisión. El test sigue bloqueado."

**El participante ejecuta:**
```
/agent modeling-tournament
```

**Prompt:**
> Ejecuta un torneo de modelos sobre validation: 3 baselines + ElasticNet + GradientBoosting (central y cuantil 95). Genera scorecard con MAPE y gráfico de backtesting real vs predicho. Si Prophet está disponible, inclúyelo.

**El agente produce:**
- `notebooks/03_model_tournament.ipynb` (ejecutado con scorecard y gráficos)
- `artifacts/models/*.joblib`
- `outputs/model_leaderboard.csv`
- `manifests/03_model_tournament.json`

**El participante inspecciona:** leaderboard, gráfico de backtesting.

**Preguntas del instructor:**
- "¿Cuál modelo tiene mejor MAPE?"
- "¿Eso significa que es el mejor para la decisión?"
- "¿Por qué NO usamos el test set todavía?"

**GO/NO-GO:** Modelos superan baselines, candidatos persistidos → **GO**

---

## Fase 5 — Evaluación de negocio (10 min) 💰

**El instructor dice:** "Ahora SÍ usamos el test. Pero no solo medimos error técnico — traducimos a dinero: ¿cuánto cuesta equivocarse?"

**El participante ejecuta:**
```
/agent evaluation-business
```

**Prompt:**
> Evalúa los modelos candidatos sobre test. Calcula métricas técnicas (MAPE) y de negocio (costo total, dinero ocioso, faltante, nivel de servicio). Genera gráfico de inferencia (real vs predicho) y compara políticas de reserva.

**El agente produce:**
- `notebooks/04_evaluation_business.ipynb` (ejecutado)
- `outputs/selected_model.json`
- `outputs/business_backtest.csv`
- `manifests/04_evaluation_business.json`

**Momento clave del instructor:** "Miren: el modelo con menor MAPE no necesariamente da la mejor decisión. La predicción NO es la decisión."

**Preguntas:**
- "¿Cuál política cumple el nivel de servicio del 95%?"
- "¿Cuánto dinero ocioso tiene cada política?"
- "¿Prefieren ahorrar dinero ocioso o garantizar servicio?"

**GO/NO-GO:** Se selecciona política que cumple guardrail → **GO**

---

## Fase 6 — Producto (6 min) 🖥️

**El instructor dice:** "El agente ahora convierte todo esto en un producto consumible. Un analista de tesorería va a ver este tablero — no le importa el RMSE, le importa cuánto reservar."

**El participante ejecuta:**
```
/agent productization-deployment
```

**Prompt:**
> Extrae la lógica a módulos en src/, genera la recomendación diaria en CSV, y construye el dashboard en Streamlit con simulador de costos.

**Luego, ejecutar el dashboard:**
```bash
streamlit run app.py
```

**El participante interactúa:**
1. Ve el monto recomendado para mañana.
2. Mueve el slider de "Costo faltante" → ve cómo sube la reserva.
3. Mueve "Nivel de servicio" a 99% → ve el costo.
4. Descarga el CSV.

**Pregunta del instructor:** "Si el gerente pide 99% de servicio, ¿cuánto más cuesta?"

---

## Fase 7 — Operación (2 min) 📋

**El instructor dice:** "Ya tenemos producto. ¿Quién lo mantiene? ¿Qué pasa si el modelo se degrada?"

**Revisión rápida (sin ejecutar agente):**
- ¿Quién es el owner? → Analítica de Liquidez
- ¿Cada cuánto se ejecuta? → Diario
- ¿Qué monitorear? → Drift, error reciente, nivel de servicio
- ¿Cómo actualizar? → Re-entrenar con datos nuevos

---

## Cierre (1 min) 🎯

**El instructor dice:**

> "En 60 minutos, con un agente de IA, construimos:
> - Un análisis exploratorio
> - Un torneo de modelos
> - Una evaluación de negocio
> - Un producto con dashboard y simulador
>
> Pero la pregunta es..."

**El instructor pregunta:**

> **"El agente construyó mucho, pero ¿quién decidió qué debía construir?"**

---

## Resumen de comandos

| Fase | Comando |
|------|---------|
| 0 | `python -c "import pandas..."` |
| 1 | `/agent business-understanding` |
| 2 | `/agent data-understanding` |
| 3 | `/agent data-preparation` |
| 4 | `/agent modeling-tournament` |
| 5 | `/agent evaluation-business` |
| 6 | `/agent productization-deployment` + `streamlit run app.py` |
| 7 | Revisión de docs |

---

## Recuperación (si algo falla)

| Problema | Solución |
|----------|----------|
| El agente tarda mucho | Ctrl+C, reintentar con prompt más corto |
| Error en un notebook | `python scripts/run_notebook.py notebooks/0X_...ipynb` |
| Se pierde el estado | `git checkout workshop-start` y empezar de nuevo |
| Streamlit no carga | Verificar que `outputs/daily_recommendation.csv` existe → correr `python -m src.decision.recommend` |
| Quiero saltar a una fase | Los manifests de fases anteriores deben existir primero |

---

## Prompts cortos (referencia rápida del participante)

```
Fase 1: "Valida si el problema de negocio está listo para desarrollo técnico."
Fase 2: "Genera un notebook EDA orientado a decisiones."
Fase 3: "Prepara datos con features temporales, valida leakage, separa train/val/test."
Fase 4: "Torneo de modelos con scorecard MAPE y gráfico backtesting."
Fase 5: "Evalúa sobre test, traduce a KPIs de negocio, compara políticas."
Fase 6: "Productiviza: módulos src/, recomendación CSV, dashboard Streamlit."
```
