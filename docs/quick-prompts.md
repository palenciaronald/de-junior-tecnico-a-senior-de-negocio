# Guía rápida — Prompts y comandos

## Iniciar sesión en Kiro

```bash
# Desde terminal
kiro chat

# Desde IDE (VS Code): abrir panel de chat de Kiro
```

---

## Fase 1 — Business Understanding

```
/agent business-understanding
```

```
Revisa docs/product-brief.md y valida si el problema de negocio está listo para desarrollo técnico. Confirma problema, decisión, usuario, KPI y entregable. Genera el reporte y manifest.
```

---

## Fase 2 — Data Understanding

```
/agent data-understanding
```

```
Analiza data/raw/daily_withdrawals.csv. Genera un notebook con EDA orientada a decisiones: calidad, estacionalidad semanal, efecto quincena, festivos, tendencia y viabilidad predictiva. Cada gráfico debe tener pregunta, hallazgo e implicación.
```

---

## Fase 3 — Data Preparation

```
/agent data-preparation
```

```
Prepara los datos para modelado temporal. Genera features de lags (1,7,14,28), rolling (mean_7, mean_14, std_7) con shift(1), y calendario. Separa en train/validation/test cronológicamente. Valida ausencia de leakage. Exporta los datasets.
```

---

## Fase 4 — Modeling Tournament

```
/agent modeling-tournament
```

```
Ejecuta un torneo de modelos sobre validation: baselines (lag-1, lag-7, MA-7) + ElasticNet + GradientBoosting central y cuantil 95. Genera scorecard con MAPE, SMAPE, MAE, RMSE, POE, PUE. Incluye gráfico de backtesting real vs predicho. Si Prophet está disponible, inclúyelo.
```

---

## Fase 5 — Evaluation Business

```
/agent evaluation-business
```

```
Evalúa los modelos candidatos sobre el test set. Calcula métricas técnicas (MAPE, cobertura Q95) y de negocio (costo total con c_ociosidad=0.0001 y c_faltante=0.0005). Genera gráfico de inferencia real vs predicho. Compara política tradicional (max 7d + 10%) vs política modelo. Selecciona la que cumpla nivel de servicio 95% con menor costo.
```

---

## Fase 6 — Productization

```
/agent productization-deployment
```

```
Extrae la lógica de los notebooks a módulos en src/. Crea src/decision/ con funciones de costo y políticas. Genera la recomendación diaria en CSV. Construye el dashboard en Streamlit con tarjetas de KPI, gráficos y simulador de costos.
```

**Ejecutar el dashboard:**

```bash
streamlit run app.py
```

---

## Comandos útiles

```bash
# Verificar entorno
python -c "import pandas, numpy, sklearn, plotly, streamlit; print('✅ OK')"

# Ejecutar pipeline completo (si existe)
python scripts/run_pipeline.py

# Ejecutar un notebook manualmente
python scripts/run_notebook.py notebooks/01_data_understanding.ipynb

# Validar una fase
python scripts/validate_phase.py data-understanding

# Correr tests
pytest -q

# Dashboard
streamlit run app.py
```
