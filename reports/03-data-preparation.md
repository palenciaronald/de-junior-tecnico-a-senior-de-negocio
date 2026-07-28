# 03 — Preparación de Datos y Baselines

## Estado

**GO** ✅

## Resumen

Features construidas sin leakage temporal. Separación train/test cronológica (80/20). Tres baselines evaluados — el mejor (MovingAverage7) tiene MAE de 26.34B COP. El modelo debe superar esta referencia.

## Evidencia revisada

- `data/raw/daily_withdrawals.csv`
- `reports/02-data-understanding.md`
- `.kiro/steering/data-science-standards.md`

## Hallazgos

### Features generadas (16 total)

| Tipo | Features | Disponibilidad |
|------|----------|----------------|
| Lags | lag_1, lag_7, lag_14 | Info pasada (shift) ✅ |
| Rolling | rolling_mean_7, rolling_mean_14, rolling_std_7 | Info pasada (shift+window) ✅ |
| Calendario | day_of_week, is_weekend, is_holiday, is_payday, is_month_end, days_to_payday, month | Conocido de antemano ✅ |
| Contexto | transaction_count, trend, special_event | Disponible al cierre de D ✅ |

### Separación temporal

| Conjunto | Días | Periodo |
|----------|------|---------|
| Train | 572 | 2024-07-15 → 2026-02-06 |
| Test | 144 | 2026-02-07 → 2026-06-30 |

Warm-up de 14 días eliminado (NaN por lags). Total útil: 716 de 730 días.

### Baselines evaluados (sobre test)

| Baseline | MAE (B COP) | RMSE (B COP) | WAPE |
|----------|-------------|--------------|------|
| NaiveLag1 | 39.04 | 48.52 | 24.81% |
| NaiveLag7 | 28.70 | 35.26 | 18.24% |
| **MovingAverage7** | **26.34** | **33.02** | **16.74%** |

### Validación de leakage

- ✅ Todos los lags usan `shift(1)` o mayor — no incluyen info de D+1.
- ✅ Rolling windows usan `shift(1)` antes del rolling — excluyen día actual.
- ✅ Features de calendario de D+1 son válidas (conocidas de antemano).
- ✅ La variable objetivo (`total_withdrawals_cop`) NO aparece como feature.

## Supuestos

1. Train ratio 80% es adecuado (572 días de entrenamiento, 144 de test).
2. El warm-up de 14 días es aceptable (pierde solo 14 de 730 días).
3. `transaction_count` está disponible al cierre del día D (es del mismo día, no de D+1).

## Artefactos

- `src/features/lag_features.py`
- `src/features/rolling_features.py`
- `src/features/calendar_features.py`
- `src/features/build.py`
- `src/models/baselines.py`
- `data/processed/features.csv`
- `reports/baseline_metrics.json`

## Riesgos pendientes

- `transaction_count` podría generar leakage si se refiere al día D+1. Se asume que es del día D (histórico).
- La tendencia creciente puede hacer que el MA7 subestime sistemáticamente.

## Siguiente paso

Ejecutar agente **modeling** para entrenar GradientBoosting y verificar que supera los 3 baselines.
