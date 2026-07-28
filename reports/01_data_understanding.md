# 01 — Entendimiento de Datos

## Estado: GO ✅

## Resumen

Dataset de 730 días de retiros diarios (julio 2024 – junio 2026), sin nulos, sin duplicados, con patrones claros de estacionalidad y tendencia. Apto para modelado temporal.

## Evidencia

- Notebook ejecutado: `notebooks/01_data_understanding.ipynb`
- Dataset: `data/raw/daily_withdrawals.csv`
- Manifest: `manifests/01_data_understanding.json`

## Hallazgos

| Aspecto | Resultado |
|---------|-----------|
| Filas | 730 |
| Nulos | 0 |
| Duplicados | 0 |
| Gaps temporales | 0 |
| Media retiros | 140.9B COP |
| CV | 29% |
| Tendencia | +42% en 2 años |
| Efecto sábado | +17% |
| Efecto domingo | -21% |
| Efecto festivo | -28% |
| Efecto quincena | +7% |

## Viabilidad predictiva

| Variable | Disponible en D para D+1 |
|----------|--------------------------|
| lag_1, lag_7, lag_14 | ✅ Info pasada |
| rolling_mean_7, rolling_mean_14 | ✅ Con shift(1) |
| day_of_week, is_weekend, is_holiday, is_payday | ✅ Calendario |
| total_withdrawals_cop D+1 | ❌ TARGET |

## Riesgos

- Tendencia creciente puede hacer que baselines subestimen.
- Solo 36 festivos en la muestra.
- Sin variables exógenas.

## Siguiente paso

Agente: **data-preparation**
