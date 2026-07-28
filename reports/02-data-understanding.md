# 02 — Entendimiento de Datos

## Estado

**GO** ✅

## Resumen

El dataset contiene 730 días de retiros diarios (julio 2024 – junio 2026), sin nulos, sin duplicados, ordenado cronológicamente y con patrones claros de estacionalidad. Es apto para modelado temporal.

## Evidencia revisada

- `data/raw/daily_withdrawals.csv`
- `reports/data_quality_report.json`
- `.kiro/steering/data-science-standards.md`

## Hallazgos

### Estructura

| Aspecto | Valor |
|---------|-------|
| Filas | 730 |
| Columnas | 11 |
| Granularidad | Diaria |
| Periodo | 2024-07-01 a 2026-06-30 |
| Variable objetivo | `total_withdrawals_cop` |
| Nulos | 0 |
| Duplicados | 0 |
| Gaps temporales | 0 |

### Estadísticas de la variable objetivo

| Estadística | Valor |
|-------------|-------|
| Media | 140.9B COP |
| Mediana | 138.3B COP |
| Mínimo | 45.3B COP |
| Máximo | 253.8B COP |
| Std | 40.5B COP |
| CV | 28.7% |

### Patrones identificados

| Patrón | Efecto |
|--------|--------|
| Día de semana | Sábado más alto (164.6B), Domingo más bajo (111.8B) |
| Festivos | -28% vs días normales |
| Quincena/fin de mes | +7% vs días normales |
| Tendencia | +42% en 2 años (primer mes: 111.6B → último mes: 159.0B) |
| Eventos especiales | 22 días marcados (> percentil 97) |

### Calidad

- ✅ Sin valores nulos.
- ✅ Sin fechas duplicadas.
- ✅ Orden cronológico correcto.
- ✅ Continuidad temporal completa (730 días sin gaps).
- ✅ Rangos de variables dentro de lo esperado.
- ⚠️ Tendencia creciente significativa (+42%) — el modelo debe capturarla.

### Variables disponibles al momento de decidir (D para D+1)

| Variable | Disponible en D para D+1 | Razón |
|----------|--------------------------|-------|
| Lags de retiros | ✅ | Info pasada |
| day_of_week (D+1) | ✅ | Calendario conocido |
| is_weekend (D+1) | ✅ | Calendario conocido |
| is_holiday (D+1) | ✅ | Calendario conocido |
| is_payday (D+1) | ✅ | Calendario conocido |
| is_month_end (D+1) | ✅ | Calendario conocido |
| days_to_payday (D+1) | ✅ | Calendario conocido |
| total_withdrawals_cop (D+1) | ❌ | Es el target — NO usar |

## Supuestos

1. Los datos ya están agregados por día (la fuente tenía registros duplicados por fecha que fueron sumados).
2. La granularidad diaria es suficiente para la decisión de liquidez D+1.
3. Los 730 días son suficientes para capturar estacionalidad semanal y efectos de calendario.
4. No hay festivos faltantes relevantes en el periodo.

## Artefactos

- `src/data/schema.py` — Definición del esquema esperado
- `src/data/loader.py` — Funciones de carga de datos
- `src/data/validate.py` — Validación completa ejecutable
- `reports/data_quality_report.json` — Reporte JSON de calidad

## Riesgos pendientes

- La tendencia creciente (+42% en 2 años) puede hacer que baselines con lag largo subestimen si no se ajustan.
- Solo 36 festivos en el periodo — muestra pequeña para estimar el efecto festivo con precisión.
- Sin variables exógenas adicionales (campañas, eventos económicos).

## Siguiente paso

Ejecutar agente **data-preparation** para generar features, separar train/test cronológicamente y evaluar baselines.
