# Requirements: liquidity-data-product

## Descripción general

Producto de datos que genera una recomendación diaria de liquidez para una billetera digital ficticia. Determina cuánto dinero reservar para atender retiros esperados del día siguiente, minimizando el costo total (dinero ocioso + faltante) sin deteriorar el nivel de servicio. Se entrega como repositorio completo para un taller universitario de 2 horas.

---

## Requisitos funcionales

### FR-1: Generación de datos sintéticos

**Descripción:** Script reproducible que genera un dataset de retiros diarios de al menos 2 años con patrones controlados.

**Criterios de aceptación:**
- [ ] El script `scripts/generate_synthetic_data.py` genera `data/raw/daily_withdrawals.csv` con semilla fija (42).
- [ ] El dataset contiene al menos 730 registros diarios consecutivos.
- [ ] Incluye las columnas: `date`, `total_withdrawals_cop`, `transaction_count`, `day_of_week`, `is_weekend`, `is_holiday`, `is_payday`, `is_month_end`, `days_to_payday`, `trend`, `special_event`.
- [ ] Los patrones incluyen: estacionalidad semanal, efecto quincena/fin de mes, festivos colombianos, tendencia moderada, variabilidad aleatoria, días extraordinarios.
- [ ] Incluye problemas controlados de calidad (valores nulos, duplicados, outlier extremo) para ejercicio pedagógico.
- [ ] No contiene nombres, documentos, identificadores personales ni información confidencial.
- [ ] Ejecutar el script dos veces produce resultados idénticos byte a byte.

---

### FR-2: Validación de datos

**Descripción:** Módulo que valida esquema, calidad y completitud del dataset antes de usarlo en el pipeline.

**Criterios de aceptación:**
- [ ] El comando `python -m src.data.validate` ejecuta validación completa.
- [ ] Valida tipos de columnas, rangos esperados y valores nulos.
- [ ] Reporta problemas de calidad encontrados (los inyectados intencionalmente).
- [ ] Retorna exit code 0 si los datos son usables (problemas menores documentados) o exit code 1 si hay errores bloqueantes.
- [ ] Genera un reporte de calidad en `reports/data_quality_report.json`.

---

### FR-3: Ingeniería de features

**Descripción:** Módulo que transforma datos crudos en features aptas para modelado, respetando la separación temporal.

**Criterios de aceptación:**
- [ ] Genera lags de retiros: lag-1, lag-7, lag-14.
- [ ] Genera promedios móviles: ventana 7 y 14 días.
- [ ] Genera features calendario: día de semana, es_quincena, es_fin_de_mes, días_hasta_quincena.
- [ ] Todas las features usan exclusivamente información disponible al cierre del día D para predecir D+1.
- [ ] Existe un test automatizado que valida ausencia de leakage temporal.
- [ ] El output se guarda en `data/processed/features.csv`.

---

### FR-4: Baselines obligatorios

**Descripción:** Implementación de al menos 3 baselines simples como referencia mínima de rendimiento.

**Criterios de aceptación:**
- [ ] Baseline naive lag-1: predicción = retiro del día anterior.
- [ ] Baseline lag-7: predicción = retiro del mismo día de semana anterior.
- [ ] Baseline promedio móvil: predicción = promedio de últimos 7 días.
- [ ] Cada baseline se evalúa con MAE, RMSE, WAPE sobre el conjunto de test.
- [ ] Los resultados se almacenan en `reports/baseline_metrics.json`.
- [ ] Cualquier modelo posterior debe superar los 3 baselines para ser considerado útil.

---

### FR-5: Modelo de machine learning

**Descripción:** Entrenamiento de un modelo de scikit-learn que genere pronóstico central y cuantil superior para soportar la decisión.

**Criterios de aceptación:**
- [ ] El comando `python -m src.models.train` entrena y serializa el modelo.
- [ ] Usa `GradientBoostingRegressor` o `HistGradientBoostingRegressor` de scikit-learn.
- [ ] Genera pronóstico central (media/mediana) y cuantil superior (configurable, default 0.95).
- [ ] La separación train/test es estrictamente cronológica (nunca random split).
- [ ] El modelo serializado se guarda en `artifacts/` con metadata (fecha, versión, parámetros, métricas).
- [ ] Semilla fija 42 garantiza reproducibilidad.
- [ ] No usa Prophet, XGBoost, LightGBM, TensorFlow, PyTorch ni servicios externos.

---

### FR-6: Evaluación del modelo

**Descripción:** Evaluación comparativa del modelo contra baselines con métricas técnicas y traducción a impacto de negocio.

**Criterios de aceptación:**
- [ ] El comando `python -m src.models.evaluate` genera el reporte completo.
- [ ] Calcula métricas técnicas: MAE, RMSE, WAPE, pinball loss, cobertura del intervalo.
- [ ] Calcula error específico en días de alta demanda (quincena, fin de mes).
- [ ] Compara contra los 3 baselines en todas las métricas.
- [ ] Traduce el error a impacto económico usando la función de costos.
- [ ] Genera reporte en `reports/model_evaluation.json`.
- [ ] El modelo seleccionado supera todos los baselines en métricas relevantes.

---

### FR-7: Capa de decisión

**Descripción:** Módulo que transforma la predicción en una recomendación de liquidez incorporando costos asimétricos y nivel de servicio.

**Criterios de aceptación:**
- [ ] Funciones puras para: calcular dinero ocioso, calcular faltante, calcular costo total, seleccionar monto recomendado.
- [ ] La recomendación ≠ pronóstico promedio; incorpora cuantil, buffer y nivel de servicio.
- [ ] Implementa la función de costo: `C(q,y) = c_ociosidad * max(q-y, 0) + c_faltante * max(y-q, 0)`.
- [ ] Costos por defecto: c_ociosidad = 0.0001 (0.01%), c_faltante = 0.0005 (0.05%), ratio ~1:5.
- [ ] Nivel de servicio configurable (default 95%).
- [ ] Implementa política tradicional de referencia (max últimos 7 días + buffer 10%).
- [ ] Compara política modelo vs. política tradicional en periodo de test.
- [ ] El comando `python -m src.decision.recommend` genera `outputs/daily_recommendation.csv`.

---

### FR-8: Dashboard en Streamlit

**Descripción:** Aplicación web local en español que presenta la recomendación como producto funcional consumible por un analista de liquidez.

**Criterios de aceptación:**
- [ ] `streamlit run app.py` inicia el tablero sin errores.
- [ ] Encabezado: "Recomendación diaria de liquidez".
- [ ] Tarjetas: monto recomendado, pronóstico central, buffer, nivel de servicio, costo esperado, versión del modelo.
- [ ] Visualizaciones: retiros históricos, pronóstico vs real, intervalo/cuantiles, comparación de políticas, dinero ocioso/faltante en backtesting, métricas.
- [ ] Simulador con sliders: costo ociosidad, costo faltante, nivel de servicio — actualiza en tiempo real.
- [ ] Botón de exportación CSV con la recomendación diaria.
- [ ] El tablero es comprensible para una persona no técnica.
- [ ] Interfaz completamente en español.

---

### FR-9: Pipeline completo

**Descripción:** Script que ejecuta el flujo end-to-end sin intervención manual.

**Criterios de aceptación:**
- [ ] `python scripts/run_pipeline.py` ejecuta: generación → validación → features → train → evaluate → recommend.
- [ ] Produce todos los artefactos esperados (datos, modelo, reportes, CSV).
- [ ] Funciona desde una instalación limpia siguiendo README.md.
- [ ] Funciona offline después de instalar dependencias.
- [ ] No requiere API keys, servicios cloud ni GPU.

---

### FR-10: Suite de tests

**Descripción:** Pruebas automatizadas que validan la integridad del pipeline completo.

**Criterios de aceptación:**
- [ ] `pytest -q` ejecuta toda la suite sin fallos.
- [ ] Tests para: esquema de datos, reproducibilidad del generador, orden cronológico, ausencia de leakage, cálculo de lags, separación train/test, cálculo de métricas, función de costos, recomendación no negativa, generación del CSV, carga del modelo, ejecución end-to-end, importación de app.py.
- [ ] Todos los tests producen resultados deterministas con semilla 42.

---

## Requisitos no funcionales

### NFR-1: Documentación del producto de datos

**Criterios de aceptación:**
- [ ] `docs/product-brief.md` documenta: problema, decisión, usuario, owner, entregable, KPIs, frecuencia, forma de consumo.
- [ ] `docs/architecture.md` incluye diagramas de contexto, componentes y flujo de datos.
- [ ] `docs/model-card.md` documenta: modelo, datos, métricas, limitaciones, uso previsto.
- [ ] `docs/monitoring-plan.md` describe qué monitorear y umbrales de alerta.

---

### NFR-2: Documentación del taller

**Criterios de aceptación:**
- [ ] `docs/prework.md` con instrucciones de instalación para Windows, macOS y Linux.
- [ ] `docs/facilitator-guide.md` con guía del instructor (timing, puntos clave, troubleshooting).
- [ ] `docs/participant-guide.md` con flujo resumido del participante.
- [ ] `workshop/00-setup.md` a `workshop/07-deployment-monitoring.md` con guías paso a paso completas.
- [ ] Cada guía incluye: objetivo, tiempo, pregunta de negocio, prompt exacto, comando, archivos generados, resultado esperado, GO/NO-GO, recuperación.

---

### NFR-3: Agentes y skills de Kiro

**Criterios de aceptación:**
- [ ] 6 agentes en `.kiro/agents/`: business-understanding, data-understanding, data-preparation, modeling, evaluation, deployment-reviewer.
- [ ] Cada agente tiene responsabilidad acotada, lee steering, produce artefacto verificable, propone GO/REVISAR/NO-GO.
- [ ] 6 skills en `.kiro/skills/`: frame-data-product, audit-time-series, build-forecast-baseline, evaluate-business-impact, build-decision-interface, review-mlops.
- [ ] No duplican contenido del steering; referencian contexto compartido.
- [ ] Los agentes no fijan modelo de lenguaje específico.

---

### NFR-4: Estrategia de ramas y checkpoints

**Criterios de aceptación:**
- [ ] Rama `main` contiene solución completa, ejecutable y probada.
- [ ] Rama `workshop-start` contiene configuración, datos, docs, steering, skills, agentes, specs, tests y esqueletos — sin la implementación completa.
- [ ] Checkpoints por fase: `checkpoint-00-setup` a `checkpoint-06-final`.
- [ ] Cada checkpoint permite recuperación si el estudiante se atrasa.

---

### NFR-5: Reproducibilidad y portabilidad

**Criterios de aceptación:**
- [ ] `requirements.txt` con versiones pinneadas exactas.
- [ ] Funciona en Python 3.11.x en Windows, macOS y Linux.
- [ ] No requiere Docker para el taller (Dockerfile opcional como artefacto de despliegue).
- [ ] No requiere internet después de instalar dependencias.
- [ ] Semilla fija en todo el pipeline.

---

### NFR-6: Separación predicción vs. decisión

**Criterios de aceptación:**
- [ ] `src/models/` contiene exclusivamente lógica de predicción.
- [ ] `src/decision/` contiene exclusivamente lógica de decisión.
- [ ] La documentación y el tablero hacen explícita esta separación.
- [ ] El taller incluye un gate donde el estudiante articula la diferencia antes de continuar.

---

## Restricciones

| Restricción | Razón |
|-------------|-------|
| Datos 100% sintéticos | Ética, privacidad, independencia de empresa |
| Sin Prophet/XGBoost/DL | Facilidad de instalación en aula |
| Sin API keys ni cloud | Funciona offline, sin costos |
| Sin notebooks como camino principal | Reproducibilidad, pipeline ejecutable |
| Laboratorio individual | Elimina dependencia de equipos |
| 60 minutos exactos | Restricción de tiempo real del taller |
| Stack cerrado (pandas, numpy, sklearn, plotly, streamlit, joblib, pytest) | Mínima superficie de dependencias |

---

## Fuera de alcance

- Modelo de deep learning o NLP.
- Datos reales de cualquier empresa.
- Despliegue en cloud.
- Entrenamiento online / streaming.
- Multimoneda o multibilletera.
- Interfaz de usuario más allá de Streamlit.
- CI/CD pipeline real (se documenta conceptualmente).
- Integración con bases de datos externas.
