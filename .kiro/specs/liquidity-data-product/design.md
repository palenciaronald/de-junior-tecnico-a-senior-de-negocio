# Design: liquidity-data-product

## Visión general de la arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Pipeline Batch Local                          │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌───────┐  ┌─────────┐ │
│  │  Datos   │→ │Validación│→ │Features │→ │Modelo │→ │Predicción│ │
│  │  (raw)   │  │(esquema) │  │(lags,   │  │(train)│  │(forecast)│ │
│  └──────────┘  └──────────┘  │calendar)│  └───────┘  └────┬─────┘ │
│                               └─────────┘                   │       │
│                                                             ▼       │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────────────────┐  │
│  │Monitoreo │← │  CSV /   │← │        Capa de Decisión         │  │
│  │(conceptual)│ │ Tablero  │  │(costos, buffer, recomendación)  │  │
│  └──────────┘  └──────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Diagrama de componentes

```
src/
├── data/
│   ├── __init__.py
│   ├── schema.py          # Definición de esquema esperado
│   ├── loader.py          # Carga de CSV con validación básica
│   └── validate.py        # Validación completa + reporte (__main__)
│
├── features/
│   ├── __init__.py
│   ├── calendar_features.py   # is_payday, is_month_end, day_of_week
│   ├── lag_features.py        # lag-1, lag-7, lag-14
│   ├── rolling_features.py    # Promedios móviles 7d, 14d
│   └── build.py               # Orquestador de feature engineering
│
├── models/
│   ├── __init__.py
│   ├── baselines.py       # NaiveLag1, NaiveLag7, MovingAverage
│   ├── train.py           # Entrenamiento GradientBoosting (__main__)
│   ├── predict.py         # Inferencia desde modelo serializado
│   ├── evaluate.py        # Evaluación y comparación (__main__)
│   └── metrics.py         # MAE, RMSE, WAPE, pinball_loss, cobertura
│
├── decision/
│   ├── __init__.py
│   ├── costs.py           # Funciones puras: ociosidad, faltante, costo_total
│   ├── policies.py        # Política tradicional + política modelo
│   ├── recommend.py       # Generación de recomendación diaria (__main__)
│   └── compare.py         # Comparación política tradicional vs modelo
│
├── monitoring/
│   ├── __init__.py
│   └── checks.py          # Drift, frescura, alertas conceptuales
│
└── visualization/
    ├── __init__.py
    ├── historical.py      # Gráficas de retiros históricos
    ├── forecast.py        # Pronóstico vs real + intervalos
    ├── decision.py        # Comparación de políticas, ocioso/faltante
    └── metrics.py         # Visualización de métricas técnicas y negocio
```

---

## Diseño detallado por componente

### 1. Generador de datos sintéticos

**Archivo:** `scripts/generate_synthetic_data.py`

**Diseño:**

```python
SEED = 42
START_DATE = "2022-01-01"
END_DATE = "2024-06-30"  # ~2.5 años (912 días)

# Componentes del generador:
# 1. Base: media diaria ~15,000M COP
# 2. Tendencia: +0.015% diario (crecimiento moderado)
# 3. Estacionalidad semanal: lunes +8%, viernes +12%, sábado -25%, domingo -40%
# 4. Efecto quincena (día 15): +35%
# 5. Efecto fin de mes (días 28-31): +25%
# 6. Festivos colombianos: -30%
# 7. Ruido: Normal(0, 0.08 * base)
# 8. Días extraordinarios (3-5): spike +60%
# 9. Problemas de calidad: 3 nulos, 2 duplicados, 1 outlier extremo
```

**Patrones de calidad inyectados:**
- 3 valores nulos en `total_withdrawals_cop` (dispersos)
- 2 registros con fecha duplicada
- 1 outlier extremo (10x la media)

**Output:** CSV con 912+ filas, 11 columnas.

---

### 2. Esquema y validación de datos

**Archivo:** `src/data/schema.py`

```python
SCHEMA = {
    "date": {"type": "datetime64", "nullable": False},
    "total_withdrawals_cop": {"type": "float64", "nullable": True, "min": 0},
    "transaction_count": {"type": "int64", "nullable": False, "min": 0},
    "day_of_week": {"type": "int64", "nullable": False, "min": 0, "max": 6},
    "is_weekend": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_holiday": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_payday": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_month_end": {"type": "int64", "nullable": False, "values": [0, 1]},
    "days_to_payday": {"type": "int64", "nullable": False, "min": 0, "max": 15},
    "trend": {"type": "float64", "nullable": False},
    "special_event": {"type": "int64", "nullable": False, "values": [0, 1]},
}
```

**Archivo:** `src/data/validate.py` (ejecutable como `__main__`)

Flujo:
1. Cargar CSV.
2. Validar columnas presentes.
3. Validar tipos.
4. Validar rangos y valores permitidos.
5. Detectar nulos, duplicados, outliers.
6. Generar `reports/data_quality_report.json` con hallazgos.
7. Retornar exit code 0 (usable con advertencias) o 1 (bloqueante).

---

### 3. Feature engineering

**Diseño de features:**

| Feature | Fuente | Disponibilidad temporal |
|---------|--------|------------------------|
| `lag_1` | Retiros D-1 | Al cierre de D-1 ✓ |
| `lag_7` | Retiros D-7 | Al cierre de D-7 ✓ |
| `lag_14` | Retiros D-14 | Al cierre de D-14 ✓ |
| `rolling_mean_7` | Media últimos 7 días | Al cierre de D-1 ✓ |
| `rolling_mean_14` | Media últimos 14 días | Al cierre de D-1 ✓ |
| `rolling_std_7` | Std últimos 7 días | Al cierre de D-1 ✓ |
| `day_of_week` | Calendario | Conocido de antemano ✓ |
| `is_weekend` | Calendario | Conocido de antemano ✓ |
| `is_payday` | Calendario | Conocido de antemano ✓ |
| `is_month_end` | Calendario | Conocido de antemano ✓ |
| `days_to_payday` | Calendario | Conocido de antemano ✓ |
| `is_holiday` | Calendario festivos | Conocido de antemano ✓ |
| `month` | Calendario | Conocido de antemano ✓ |

**Regla de leakage:** Ninguna feature usa información del día D+1 (target) ni del día D después del momento de decisión (cierre D-1).

**Archivo:** `src/features/build.py`

```python
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construye todas las features. Elimina filas con NaN por lags iniciales."""
    df = add_lag_features(df)      # lag_1, lag_7, lag_14
    df = add_rolling_features(df)  # rolling_mean_7, rolling_mean_14, rolling_std_7
    df = add_calendar_features(df) # month, enriched calendar
    df = df.dropna().reset_index(drop=True)
    return df
```

---

### 4. Separación temporal

**Diseño:**

```
|←————— Train (80%) ————→|←— Test (20%) —→|
2022-01-15        ~2024-01-01        2024-06-30
     (después de lags)     punto de corte
```

- Train: primeros ~80% de los datos (después de warm-up de 14 días para lags).
- Test: últimos ~20% de los datos.
- El punto de corte simula el momento de decisión: el modelo solo ve datos anteriores.
- No se usa validación cruzada estándar. Si se necesita tuning, usar TimeSeriesSplit.

---

### 5. Baselines

**Archivo:** `src/models/baselines.py`

```python
class BaselineModel(Protocol):
    def predict(self, df: pd.DataFrame) -> np.ndarray: ...

class NaiveLag1:
    """Predicción = retiro del día anterior."""

class NaiveLag7:
    """Predicción = retiro del mismo día de semana anterior."""

class MovingAverage7:
    """Predicción = promedio de los últimos 7 días."""
```

Cada baseline se evalúa sobre el mismo conjunto de test que el modelo ML.

---

### 6. Modelo de machine learning

**Archivo:** `src/models/train.py`

**Modelo central:**
```python
GradientBoostingRegressor(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    random_state=42,
    loss="squared_error"  # Pronóstico central
)
```

**Modelo cuantil (para límite superior):**
```python
GradientBoostingRegressor(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    random_state=42,
    loss="quantile",
    alpha=0.95  # Cuantil 95 por defecto
)
```

**Serialización:**
```python
artifact = {
    "model_central": model_central,      # joblib
    "model_quantile": model_quantile,    # joblib
    "metadata": {
        "version": "1.0.0",
        "trained_at": "2024-06-30T23:59:00",
        "train_end_date": "2024-01-01",
        "features": [...],
        "hyperparameters": {...},
        "metrics": {...},
        "seed": 42
    }
}
# Guardado en: artifacts/model_v1.0.0.joblib + artifacts/model_v1.0.0_metadata.json
```

---

### 7. Métricas

**Archivo:** `src/models/metrics.py`

```python
def mae(y_true, y_pred) -> float: ...
def rmse(y_true, y_pred) -> float: ...
def wape(y_true, y_pred) -> float: ...
def pinball_loss(y_true, y_pred, alpha=0.95) -> float: ...
def interval_coverage(y_true, lower, upper) -> float: ...
def high_demand_error(y_true, y_pred, mask_high_demand) -> float: ...
```

Todas son funciones puras que reciben arrays y retornan escalares.

---

### 8. Capa de decisión

**Archivo:** `src/decision/costs.py`

```python
DEFAULT_COST_IDLE = 0.0001      # 0.01% del exceso por día
DEFAULT_COST_SHORTAGE = 0.0005  # 0.05% del faltante por día
DEFAULT_SERVICE_LEVEL = 0.95

def calculate_idle_money(reserved: float, actual: float) -> float:
    """max(reserved - actual, 0)"""

def calculate_shortage(reserved: float, actual: float) -> float:
    """max(actual - reserved, 0)"""

def calculate_total_cost(
    reserved: float,
    actual: float,
    cost_idle: float = DEFAULT_COST_IDLE,
    cost_shortage: float = DEFAULT_COST_SHORTAGE,
) -> float:
    """C(q,y) = cost_idle * max(q-y, 0) + cost_shortage * max(y-q, 0)"""
```

**Archivo:** `src/decision/policies.py`

```python
def traditional_policy(history_7d: np.ndarray, buffer_pct: float = 0.10) -> float:
    """Política tradicional: max(últimos 7 días) * (1 + buffer)."""

def model_policy(
    forecast_central: float,
    forecast_quantile: float,
    service_level: float = 0.95,
) -> float:
    """Política modelo: usa cuantil como techo, ajusta por nivel de servicio."""
```

**Archivo:** `src/decision/recommend.py` (ejecutable como `__main__`)

Output: `outputs/daily_recommendation.csv`

```csv
date,forecast_central,forecast_quantile_95,recommended_amount,buffer,service_level,risk_shortage_pct,cost_idle_expected,cost_shortage_expected,model_version
2024-06-30,15234000000,17890000000,17890000000,2656000000,0.95,0.05,178900,0,1.0.0
```

**Archivo:** `src/decision/compare.py`

```python
def compare_policies(
    y_true: np.ndarray,
    traditional_reserves: np.ndarray,
    model_reserves: np.ndarray,
    cost_idle: float,
    cost_shortage: float,
) -> dict:
    """Compara costo total, dinero ocioso, faltantes, nivel de servicio."""
```

---

### 9. Dashboard Streamlit

**Archivo:** `app.py`

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│         Recomendación diaria de liquidez             │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│  Monto   │Pronóstico│  Buffer  │  Nivel   │  Costo  │
│Recomendado│ Central │Seguridad │ Servicio │Esperado │
├──────────┴──────────┴──────────┴──────────┴─────────┤
│                                                     │
│  [Tab: Histórico] [Tab: Pronóstico] [Tab: Decisión] │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │          Gráfica principal (plotly)          │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
├─────────────────────────────────────────────────────┤
│  SIDEBAR:                                           │
│  ─────────                                          │
│  Simulador de parámetros:                           │
│  • Costo ociosidad [slider 0.0001 - 0.001]         │
│  • Costo faltante  [slider 0.0001 - 0.005]         │
│  • Nivel servicio  [slider 0.80 - 0.99]            │
│  ─────────                                          │
│  [Descargar CSV]                                    │
│  ─────────                                          │
│  Versión modelo: v1.0.0                             │
│  Última actualización: 2024-06-30                   │
└─────────────────────────────────────────────────────┘
```

**Tabs principales:**
1. **Histórico**: Serie temporal de retiros, con marcas en quincena/fin de mes.
2. **Pronóstico**: Predicción vs real en test, con banda de cuantiles.
3. **Decisión**: Comparación de políticas, dinero ocioso/faltante diario, métricas de negocio.

**Interactividad:**
- Los sliders del sidebar recalculan la recomendación y métricas en tiempo real.
- Plotly para gráficas interactivas (hover, zoom).
- Botón de descarga genera CSV con `st.download_button`.

---

### 10. Pipeline completo

**Archivo:** `scripts/run_pipeline.py`

```python
"""Pipeline completo ejecutable con: python scripts/run_pipeline.py"""

STEPS = [
    ("Generando datos sintéticos", "scripts/generate_synthetic_data.py"),
    ("Validando datos", "-m src.data.validate"),
    ("Entrenando modelo", "-m src.models.train"),
    ("Evaluando modelo", "-m src.models.evaluate"),
    ("Generando recomendación", "-m src.decision.recommend"),
]
```

Ejecuta cada paso secuencialmente. Si uno falla, reporta el error y se detiene.

---

### 11. Monitoreo conceptual

**Archivo:** `src/monitoring/checks.py`

```python
def check_data_freshness(last_date: date, today: date, max_lag_days: int = 2) -> Alert: ...
def check_distribution_drift(recent: np.ndarray, historical: np.ndarray) -> Alert: ...
def check_recent_error(recent_mae: float, threshold: float) -> Alert: ...
def check_coverage(coverage: float, expected: float = 0.95) -> Alert: ...
def check_service_level(achieved: float, target: float = 0.95) -> Alert: ...
def check_total_cost_trend(costs: list[float], window: int = 7) -> Alert: ...
```

No se ejecuta en producción real — es un artefacto pedagógico que muestra qué monitorear.

---

### 12. Testing strategy

**Archivo:** `tests/conftest.py` — fixtures compartidas (datos de ejemplo, modelo dummy)

| Test file | Qué valida | FR/NFR |
|-----------|-----------|--------|
| `test_data_schema.py` | Esquema y tipos del CSV | FR-1, FR-2 |
| `test_reproducibility.py` | Generador produce mismos datos con semilla 42 | FR-1 |
| `test_chronological_order.py` | Datos ordenados por fecha | FR-2 |
| `test_leakage.py` | Ninguna feature usa datos futuros | FR-3 |
| `test_lag_features.py` | Lags calculados correctamente | FR-3 |
| `test_train_test_split.py` | Separación temporal correcta | FR-5 |
| `test_metrics.py` | Funciones de métricas son correctas | FR-6 |
| `test_costs.py` | Función de costos correcta | FR-7 |
| `test_recommendation.py` | Recomendación no negativa y coherente | FR-7 |
| `test_csv_output.py` | CSV de recomendación tiene esquema correcto | FR-7 |
| `test_model_load.py` | Modelo se carga y predice | FR-5 |
| `test_pipeline_e2e.py` | Pipeline completo termina sin error | FR-9 |
| `test_app_import.py` | app.py importa sin error | FR-8 |

---

### 13. Agentes de Kiro

**Formato de agente:** `.kiro/agents/{name}.md`

```markdown
---
description: <una línea describiendo responsabilidad>
---

# Agente: {name}

## Responsabilidad
...

## Contexto que lee
- .kiro/steering/product.md
- .kiro/steering/data-science-standards.md
- (otros según fase)

## Artefactos que produce
...

## Criterios de terminación
...

## Restricciones
- No alterar problem statement sin aprobación.
- No inventar resultados.
- Detenerse si faltan datos.
- Reportar archivos creados/modificados.
- Proponer: GO / REVISAR / NO-GO.
```

**Agentes:**

| Agente | Responsabilidad | Input principal | Output |
|--------|----------------|-----------------|--------|
| business-understanding | Validar product-brief, confirmar problema/decisión/KPI | docs/product-brief.md | Decisión GO/NO-GO |
| data-understanding | Perfilar datos, reportar calidad, granularidad | data/raw/*.csv | reports/data_quality_report.json |
| data-preparation | Generar features, validar leakage, separar train/test | data/raw/ | data/processed/features.csv |
| modeling | Entrenar baselines + modelo, serializar | data/processed/ | artifacts/model_*.joblib |
| evaluation | Comparar métricas, traducir a negocio | artifacts/, data/processed/ | reports/model_evaluation.json |
| deployment-reviewer | Revisar arquitectura, monitoreo, versionamiento | docs/, src/monitoring/ | Checklist de operación |

---

### 14. Skills de Kiro

**Formato de skill:** `.kiro/skills/{name}/SKILL.md`

```markdown
---
description: <una línea>
---

# Skill: {name}

## Cuándo usarla
...

## Pasos
1. ...
2. ...

## Output esperado
...

## Validación
...
```

| Skill | Propósito | Pasos clave |
|-------|-----------|-------------|
| frame-data-product | Estructurar el product-brief desde una solicitud ambigua | Problema → Decisión → Usuario → KPI → Entregable |
| audit-time-series | Perfilar serie temporal y detectar problemas | Estadísticas → Estacionalidad → Nulos → Outliers → Reporte |
| build-forecast-baseline | Implementar y evaluar baselines | Lag-1 → Lag-7 → MA-7 → Métricas → Comparación |
| evaluate-business-impact | Traducir métricas técnicas a impacto económico | Costo total → Ocioso → Faltante → Nivel servicio → Comparación |
| build-decision-interface | Construir la capa de decisión con Streamlit | Costos → Buffer → Simulador → CSV → Dashboard |
| review-mlops | Auditar operabilidad del producto | Monitoreo → Versionamiento → Owner → Actualización → Checklist |

---

### 15. Estrategia de ramas

```
main (solución completa)
│
├── workshop-start (esqueletos + config + datos + docs + steering + tests)
│
├── checkpoint-00-setup
├── checkpoint-01-business
├── checkpoint-02-data
├── checkpoint-03-model
├── checkpoint-04-evaluation
├── checkpoint-05-product
└── checkpoint-06-final (= main)
```

Cada checkpoint es un tag o rama que permite `git checkout checkpoint-XX-name` para recuperarse.

---

## Decisiones de diseño clave

| Decisión | Justificación |
|----------|---------------|
| GradientBoosting sobre HistGradientBoosting | Soporte nativo de `loss="quantile"` sin workarounds |
| Cuantil 0.95 como default | Alineado con nivel de servicio 95% |
| Costos ratio 1:5 (ociosidad:faltante) | Refleja asimetría real: faltante es más costoso |
| Política tradicional = max(7d) + 10% | Simple, conservadora, representativa de reglas manuales |
| Plotly sobre matplotlib | Interactividad nativa en Streamlit, hover, zoom |
| Módulos con `__main__` | Permiten ejecución directa (`python -m src.models.train`) |
| JSON para reportes | Fácil de parsear en tests y en dashboard |
| 2.5 años de datos | Suficiente para patrones anuales + test robusto |

---

## Flujo de datos

```
generate_synthetic_data.py
        │
        ▼
data/raw/daily_withdrawals.csv
        │
        ▼
src.data.validate  ──→  reports/data_quality_report.json
        │
        ▼
src.features.build  ──→  data/processed/features.csv
        │
        ▼
src.models.train  ──→  artifacts/model_v1.0.0.joblib
        │                artifacts/model_v1.0.0_metadata.json
        ▼
src.models.evaluate  ──→  reports/baseline_metrics.json
        │                  reports/model_evaluation.json
        ▼
src.decision.recommend  ──→  outputs/daily_recommendation.csv
        │
        ▼
app.py (Streamlit)  ←── Lee: artifacts/, outputs/, data/
```

---

## Dependencias entre módulos (reglas de import)

```
src.data ←── src.features ←── src.models ←── src.decision
                                                    │
                                              src.monitoring
                                              src.visualization (lee de todos)
```

- `decision/` puede importar de `models/` (para obtener predicciones).
- `models/` puede importar de `features/` (para construir features antes de predecir).
- `features/` puede importar de `data/` (para cargar datos).
- **Nunca** al revés.
- `visualization/` y `monitoring/` pueden importar de cualquiera.
