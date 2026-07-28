# Tasks: liquidity-data-product

## Bloque 1: Infraestructura base

### Task 1.1: requirements.txt y configuración del proyecto
- [ ] Crear `requirements.txt` con versiones pinneadas:
  ```
  pandas==2.1.4
  numpy==1.26.2
  scikit-learn==1.3.2
  plotly==5.18.0
  streamlit==1.29.0
  joblib==1.3.2
  pytest==7.4.4
  ```
- [ ] Crear `.gitignore` (Python, venv, .env, __pycache__, artifacts/*.joblib, data/processed/)
- [ ] Crear `LICENSE` (MIT)
- [ ] Verificar que `pip install -r requirements.txt` se ejecute sin errores

**Requisito:** NFR-5  
**Verificación:** `pip install -r requirements.txt` exit code 0

---

### Task 1.2: README.md
- [ ] Crear `README.md` con:
  - Título y descripción del taller
  - Requisitos previos (Python 3.11)
  - Instrucciones de instalación (Windows, macOS, Linux)
  - Comandos principales del pipeline
  - Estructura del repositorio
  - Cómo ejecutar el taller (instructor vs participante)
  - Licencia

**Requisito:** NFR-5  
**Verificación:** El README contiene instrucciones reproducibles para los 3 OS

---

## Bloque 2: Datos sintéticos y validación

### Task 2.1: Generador de datos sintéticos
- [ ] Crear `scripts/generate_synthetic_data.py`
- [ ] Implementar generación con semilla 42, rango 2022-01-01 a 2024-06-30
- [ ] Implementar componentes: base, tendencia, estacionalidad semanal, efecto quincena, fin de mes, festivos colombianos, ruido, eventos especiales
- [ ] Inyectar problemas de calidad: 3 nulos, 2 duplicados, 1 outlier extremo
- [ ] Generar `data/raw/daily_withdrawals.csv` con 11 columnas
- [ ] Verificar reproducibilidad: dos ejecuciones producen mismo archivo

**Requisito:** FR-1  
**Verificación:** `python scripts/generate_synthetic_data.py` genera CSV; `md5` de dos ejecuciones es idéntico

---

### Task 2.2: Esquema de datos
- [ ] Crear `src/data/schema.py` con definición de esquema (tipos, rangos, valores permitidos)
- [ ] Crear `src/data/loader.py` con función `load_raw_data()` que carga CSV y parsea fechas

**Requisito:** FR-2  
**Verificación:** `from src.data.schema import SCHEMA` importa sin error

---

### Task 2.3: Módulo de validación
- [ ] Crear `src/data/validate.py` con `__main__` ejecutable
- [ ] Implementar validación de: columnas, tipos, rangos, nulos, duplicados, outliers
- [ ] Generar `reports/data_quality_report.json`
- [ ] Retornar exit code 0 (usable) o 1 (bloqueante)

**Requisito:** FR-2  
**Verificación:** `python -m src.data.validate` produce JSON y exit code 0

---

### Task 2.4: Tests de datos
- [ ] Crear `tests/test_data_schema.py` — valida esquema del CSV generado
- [ ] Crear `tests/test_reproducibility.py` — verifica mismos datos con semilla 42
- [ ] Crear `tests/test_chronological_order.py` — fechas estrictamente ordenadas

**Requisito:** FR-10  
**Verificación:** `pytest tests/test_data_schema.py tests/test_reproducibility.py tests/test_chronological_order.py -q` pasa

---

## Bloque 3: Feature engineering

### Task 3.1: Features de lag
- [ ] Crear `src/features/lag_features.py` con funciones para lag-1, lag-7, lag-14

**Requisito:** FR-3  
**Verificación:** Función retorna columnas con NaN solo en primeras 14 filas

---

### Task 3.2: Features de promedio móvil
- [ ] Crear `src/features/rolling_features.py` con rolling_mean_7, rolling_mean_14, rolling_std_7

**Requisito:** FR-3  
**Verificación:** Valores calculados son correctos para muestra manual

---

### Task 3.3: Features de calendario
- [ ] Crear `src/features/calendar_features.py` con month, is_payday enriched, is_month_end enriched, days_to_payday

**Requisito:** FR-3  
**Verificación:** El 15 de enero tiene `is_payday=1`, el 31 tiene `is_month_end=1`

---

### Task 3.4: Orquestador de features
- [ ] Crear `src/features/build.py` con `build_features(df) -> DataFrame`
- [ ] Integrar lags + rolling + calendar
- [ ] Eliminar filas con NaN por warm-up
- [ ] Guardar resultado en `data/processed/features.csv`

**Requisito:** FR-3  
**Verificación:** `python -c "from src.features.build import build_features"` importa sin error; CSV generado tiene todas las columnas

---

### Task 3.5: Tests de features y leakage
- [ ] Crear `tests/test_lag_features.py` — verifica cálculo correcto de lags
- [ ] Crear `tests/test_leakage.py` — verifica que ninguna feature usa datos del día target (D+1)

**Requisito:** FR-3, FR-10  
**Verificación:** `pytest tests/test_lag_features.py tests/test_leakage.py -q` pasa

---

## Bloque 4: Baselines y modelo

### Task 4.1: Baselines
- [ ] Crear `src/models/baselines.py` con clases: `NaiveLag1`, `NaiveLag7`, `MovingAverage7`
- [ ] Cada clase implementa método `predict(df) -> np.ndarray`

**Requisito:** FR-4  
**Verificación:** Cada baseline retorna array del mismo largo que el input de test

---

### Task 4.2: Métricas
- [ ] Crear `src/models/metrics.py` con funciones: `mae`, `rmse`, `wape`, `pinball_loss`, `interval_coverage`, `high_demand_error`
- [ ] Todas son funciones puras (arrays → escalar)

**Requisito:** FR-6  
**Verificación:** `pytest tests/test_metrics.py -q` pasa (crear test en Task 4.5)

---

### Task 4.3: Entrenamiento del modelo
- [ ] Crear `src/models/train.py` con `__main__` ejecutable
- [ ] Implementar separación temporal (80/20 cronológica)
- [ ] Entrenar `GradientBoostingRegressor` central (loss="squared_error")
- [ ] Entrenar `GradientBoostingRegressor` cuantil (loss="quantile", alpha=0.95)
- [ ] Serializar en `artifacts/model_v1.0.0.joblib`
- [ ] Guardar metadata en `artifacts/model_v1.0.0_metadata.json`

**Requisito:** FR-5  
**Verificación:** `python -m src.models.train` genera archivos en artifacts/; metadata JSON parseable

---

### Task 4.4: Evaluación del modelo
- [ ] Crear `src/models/evaluate.py` con `__main__` ejecutable
- [ ] Evaluar baselines y modelo con todas las métricas
- [ ] Calcular error en días de alta demanda
- [ ] Generar `reports/baseline_metrics.json` y `reports/model_evaluation.json`
- [ ] Verificar que modelo supera los 3 baselines

**Requisito:** FR-6  
**Verificación:** `python -m src.models.evaluate` genera JSONs; modelo supera baselines en MAE

---

### Task 4.5: Tests de modelo
- [ ] Crear `tests/test_metrics.py` — funciones de métricas con valores conocidos
- [ ] Crear `tests/test_train_test_split.py` — separación cronológica correcta
- [ ] Crear `tests/test_model_load.py` — modelo se carga y predice sin error

**Requisito:** FR-10  
**Verificación:** `pytest tests/test_metrics.py tests/test_train_test_split.py tests/test_model_load.py -q` pasa

---

## Bloque 5: Capa de decisión

### Task 5.1: Funciones de costos
- [ ] Crear `src/decision/costs.py` con: `calculate_idle_money`, `calculate_shortage`, `calculate_total_cost`
- [ ] Constantes: `DEFAULT_COST_IDLE = 0.0001`, `DEFAULT_COST_SHORTAGE = 0.0005`, `DEFAULT_SERVICE_LEVEL = 0.95`

**Requisito:** FR-7  
**Verificación:** `calculate_total_cost(100, 80, 0.0001, 0.0005) == 0.0001 * 20` (solo ocioso)

---

### Task 5.2: Políticas de reserva
- [ ] Crear `src/decision/policies.py` con: `traditional_policy`, `model_policy`
- [ ] Política tradicional: max(últimos 7 días) * 1.10
- [ ] Política modelo: usa cuantil 95 como recomendación

**Requisito:** FR-7  
**Verificación:** Ambas funciones retornan valores positivos y razonables

---

### Task 5.3: Generador de recomendación
- [ ] Crear `src/decision/recommend.py` con `__main__` ejecutable
- [ ] Generar `outputs/daily_recommendation.csv` con columnas: date, forecast_central, forecast_quantile_95, recommended_amount, buffer, service_level, risk_shortage_pct, cost_idle_expected, cost_shortage_expected, model_version

**Requisito:** FR-7  
**Verificación:** `python -m src.decision.recommend` genera CSV con esquema correcto

---

### Task 5.4: Comparación de políticas
- [ ] Crear `src/decision/compare.py` con `compare_policies()` que retorna dict con métricas comparativas
- [ ] Calcular: costo_total, dinero_ocioso_promedio, faltante_promedio, nivel_servicio, dias_con_faltante

**Requisito:** FR-7  
**Verificación:** La política modelo tiene menor costo total que la tradicional

---

### Task 5.5: Tests de decisión
- [ ] Crear `tests/test_costs.py` — función de costos con valores conocidos
- [ ] Crear `tests/test_recommendation.py` — recomendación siempre ≥ 0, coherente con inputs
- [ ] Crear `tests/test_csv_output.py` — CSV tiene esquema correcto y valores no negativos

**Requisito:** FR-10  
**Verificación:** `pytest tests/test_costs.py tests/test_recommendation.py tests/test_csv_output.py -q` pasa

---

## Bloque 6: Visualización y dashboard

### Task 6.1: Funciones de visualización
- [ ] Crear `src/visualization/historical.py` — gráfica de retiros históricos con marcas de quincena/fin de mes
- [ ] Crear `src/visualization/forecast.py` — pronóstico vs real con banda de cuantiles
- [ ] Crear `src/visualization/decision.py` — comparación de políticas, dinero ocioso/faltante
- [ ] Crear `src/visualization/metrics.py` — tabla/gráfica de métricas técnicas y de negocio

**Requisito:** FR-8  
**Verificación:** Cada función retorna un `plotly.graph_objects.Figure`

---

### Task 6.2: Aplicación Streamlit
- [ ] Crear `app.py` con layout completo en español
- [ ] Implementar tarjetas: monto recomendado, pronóstico, buffer, nivel servicio, costo, versión modelo
- [ ] Implementar tabs: Histórico, Pronóstico, Decisión
- [ ] Implementar sidebar con simulador (sliders de costos y nivel de servicio)
- [ ] Implementar recálculo en tiempo real al mover sliders
- [ ] Implementar botón de descarga CSV

**Requisito:** FR-8  
**Verificación:** `streamlit run app.py` inicia sin errores; `pytest tests/test_app_import.py -q` pasa

---

### Task 6.3: Test de importación de app
- [ ] Crear `tests/test_app_import.py` — verifica que `app.py` importa sin error de módulos faltantes

**Requisito:** FR-10  
**Verificación:** `pytest tests/test_app_import.py -q` pasa

---

## Bloque 7: Pipeline y monitoreo

### Task 7.1: Pipeline completo
- [ ] Crear `scripts/run_pipeline.py` que ejecuta secuencialmente: generate → validate → train → evaluate → recommend
- [ ] Reportar progreso por paso
- [ ] Detenerse si un paso falla

**Requisito:** FR-9  
**Verificación:** `python scripts/run_pipeline.py` termina sin error y produce todos los artefactos

---

### Task 7.2: Monitoreo conceptual
- [ ] Crear `src/monitoring/checks.py` con funciones: `check_data_freshness`, `check_distribution_drift`, `check_recent_error`, `check_coverage`, `check_service_level`, `check_total_cost_trend`
- [ ] Cada función retorna un dict con `status` (ok/warning/critical) y `message`

**Requisito:** NFR-1  
**Verificación:** Las funciones se importan y ejecutan con datos de ejemplo

---

### Task 7.3: Test end-to-end
- [ ] Crear `tests/test_pipeline_e2e.py` — ejecuta pipeline mini y verifica que todos los artefactos se producen
- [ ] Crear `tests/conftest.py` con fixtures compartidas

**Requisito:** FR-10  
**Verificación:** `pytest tests/test_pipeline_e2e.py -q` pasa

---

## Bloque 8: Documentación del producto

### Task 8.1: Product brief
- [ ] Crear `docs/product-brief.md` con: Problema, Decisión, Usuario, Owner, Producto, Frecuencia, Consumo, KPIs, Métricas

**Requisito:** NFR-1  
**Verificación:** Archivo existe y contiene todas las secciones del contrato

---

### Task 8.2: Arquitectura y diagramas
- [ ] Crear `docs/architecture.md` con diagramas de contexto, componentes y flujo de datos (formato texto/mermaid)
- [ ] Crear `docs/context-diagram.md` con diagrama de contexto del sistema

**Requisito:** NFR-1  
**Verificación:** Archivos existen y son coherentes con el diseño

---

### Task 8.3: Model card
- [ ] Crear `docs/model-card.md` con: modelo utilizado, datos de entrenamiento, métricas, limitaciones, uso previsto, información ética

**Requisito:** NFR-1  
**Verificación:** Archivo completo según template estándar

---

### Task 8.4: Plan de monitoreo
- [ ] Crear `docs/monitoring-plan.md` con: qué monitorear, umbrales, frecuencia, responsable, acciones correctivas

**Requisito:** NFR-1  
**Verificación:** Plan cubre al menos 8 señales (calidad, drift, error, cobertura, ocioso, faltante, servicio, costo)

---

## Bloque 9: Documentación del taller

### Task 9.1: Prework e instalación
- [ ] Crear `docs/prework.md` con instrucciones detalladas para Windows, macOS y Linux
- [ ] Incluir: instalación Python 3.11, creación de venv, pip install, clonación del repo, verificación

**Requisito:** NFR-2  
**Verificación:** Un usuario nuevo puede seguir las instrucciones sin ambigüedad

---

### Task 9.2: Guía del instructor
- [ ] Crear `docs/facilitator-guide.md` con: timing por fase, puntos clave a enfatizar, preguntas esperadas, troubleshooting, checklist de ensayo

**Requisito:** NFR-2  
**Verificación:** Archivo cubre las 8 fases del laboratorio con tiempos

---

### Task 9.3: Guía del participante
- [ ] Crear `docs/participant-guide.md` con: flujo resumido, comandos a ejecutar, qué observar, preguntas de reflexión

**Requisito:** NFR-2  
**Verificación:** Guía es ejecutable en 60 minutos siguiendo secuencialmente

---

### Task 9.4: Workshop paso a paso (8 archivos)
- [ ] Crear `workshop/00-setup.md` — Verificación de entorno
- [ ] Crear `workshop/01-business-gate.md` — Revisión de product-brief, GO/NO-GO
- [ ] Crear `workshop/02-data-understanding.md` — Ejecutar validación, revisar calidad
- [ ] Crear `workshop/03-data-preparation.md` — Features, separación temporal, baselines
- [ ] Crear `workshop/04-modeling.md` — Entrenar modelo, serializar
- [ ] Crear `workshop/05-evaluation.md` — Métricas técnicas y de negocio, comparación
- [ ] Crear `workshop/06-decision-product.md` — Capa de decisión, recomendación, CSV
- [ ] Crear `workshop/07-deployment-monitoring.md` — Streamlit, monitoreo, cierre
- [ ] Cada archivo incluye: objetivo, tiempo, pregunta de negocio, prompt Kiro, comando, archivos generados, resultado esperado, GO/NO-GO, recuperación, checkpoint

**Requisito:** NFR-2  
**Verificación:** Los 8 archivos existen y siguen la estructura definida

---

## Bloque 10: Agentes y skills de Kiro

### Task 10.1: Agentes
- [ ] Crear `.kiro/agents/business-understanding.md`
- [ ] Crear `.kiro/agents/data-understanding.md`
- [ ] Crear `.kiro/agents/data-preparation.md`
- [ ] Crear `.kiro/agents/modeling.md`
- [ ] Crear `.kiro/agents/evaluation.md`
- [ ] Crear `.kiro/agents/deployment-reviewer.md`
- [ ] Cada agente tiene: description (frontmatter), responsabilidad, contexto que lee, artefactos que produce, criterios de terminación, restricciones, decisión GO/REVISAR/NO-GO

**Requisito:** NFR-3  
**Verificación:** Los 6 archivos existen y siguen el formato de agente de Kiro

---

### Task 10.2: Skills
- [ ] Crear `.kiro/skills/frame-data-product/SKILL.md`
- [ ] Crear `.kiro/skills/audit-time-series/SKILL.md`
- [ ] Crear `.kiro/skills/build-forecast-baseline/SKILL.md`
- [ ] Crear `.kiro/skills/evaluate-business-impact/SKILL.md`
- [ ] Crear `.kiro/skills/build-decision-interface/SKILL.md`
- [ ] Crear `.kiro/skills/review-mlops/SKILL.md`
- [ ] Cada skill tiene: description (frontmatter), cuándo usarla, pasos, output esperado, validación

**Requisito:** NFR-3  
**Verificación:** Los 6 directorios con SKILL.md existen y siguen formato válido

---

## Bloque 11: Integración y validación final

### Task 11.1: Ejecución completa del pipeline
- [ ] Ejecutar `python scripts/run_pipeline.py` desde cero
- [ ] Verificar que produce: data/raw/daily_withdrawals.csv, data/processed/features.csv, artifacts/model_*.joblib, reports/*.json, outputs/daily_recommendation.csv

**Requisito:** FR-9  
**Verificación:** Todos los artefactos existen y tienen contenido válido

---

### Task 11.2: Suite completa de tests
- [ ] Ejecutar `pytest -q` y verificar que todos los tests pasan
- [ ] Verificar cobertura de los 13 casos requeridos

**Requisito:** FR-10  
**Verificación:** `pytest -q` exit code 0, 13+ tests pasando

---

### Task 11.3: Verificación del dashboard
- [ ] Ejecutar `streamlit run app.py` y verificar que carga sin errores
- [ ] Verificar tarjetas, gráficas, simulador y exportación CSV

**Requisito:** FR-8  
**Verificación:** Dashboard accesible en localhost, todas las secciones funcionales

---

### Task 11.4: AGENTS.md
- [ ] Crear `AGENTS.md` en raíz con instrucciones para agentes externos (Codex, Copilot) que trabajen en el repo
- [ ] Incluir: estructura, convenciones, cómo ejecutar tests, qué no modificar

**Requisito:** NFR-5  
**Verificación:** Archivo existe y es coherente con la estructura real

---

### Task 11.5: Dockerfile (opcional)
- [ ] Crear `Dockerfile` basado en python:3.11-slim
- [ ] Instalar dependencias y copiar código
- [ ] Exponer puerto 8501 para Streamlit
- [ ] Documentar que NO es requerido para el taller

**Requisito:** NFR-5  
**Verificación:** `docker build .` funciona (no bloqueante si Docker no está disponible)

---

## Orden de ejecución

```
Bloque 1 (Infra)
    → Bloque 2 (Datos)
        → Bloque 3 (Features)
            → Bloque 4 (Modelo)
                → Bloque 5 (Decisión)
                    → Bloque 6 (Dashboard)
                        → Bloque 7 (Pipeline + Monitoreo)
Bloque 8 (Docs producto)     ← puede ejecutarse en paralelo desde Bloque 5
Bloque 9 (Docs taller)       ← puede ejecutarse en paralelo desde Bloque 7
Bloque 10 (Agentes/Skills)   ← puede ejecutarse en paralelo desde Bloque 1
Bloque 11 (Validación final) ← requiere todos los anteriores
```

Total: **11 bloques, 27 tasks**, cada una verificable independientemente.
