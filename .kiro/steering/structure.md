# Structure Steering

## Arquitectura del repositorio

```
├── .kiro/                  # Configuración de Kiro (steering, agents, skills, specs)
├── data/
│   ├── raw/                # Datos sin procesar (CSV generado)
│   └── processed/          # Datos preparados para modelado
├── docs/                   # Documentación de producto, arquitectura y taller
├── workshop/               # Guías paso a paso del laboratorio (00-07)
├── src/
│   ├── data/               # Carga, validación y esquema de datos
│   ├── features/           # Ingeniería de features y transformaciones
│   ├── models/             # Entrenamiento, predicción y baselines
│   ├── decision/           # Capa de decisión: costos, recomendación, políticas
│   ├── monitoring/         # Monitoreo conceptual y alertas
│   └── visualization/      # Funciones de visualización reutilizables
├── scripts/                # Scripts ejecutables (generación de datos, pipeline)
├── tests/                  # Tests unitarios e integración
├── artifacts/              # Modelos serializados y metadata
├── outputs/                # CSV de recomendaciones generadas
├── reports/                # Reportes de evaluación generados
├── app.py                  # Punto de entrada de Streamlit
├── requirements.txt        # Dependencias pinneadas
├── Dockerfile              # Imagen de despliegue (opcional)
└── README.md               # Documentación principal
```

## Responsabilidad de cada carpeta

| Carpeta | Responsabilidad | NO debe contener |
|---------|----------------|-----------------|
| `src/data/` | Carga, validación de esquema, calidad | Transformaciones de features |
| `src/features/` | Feature engineering, lags, calendarios | Lógica de modelo |
| `src/models/` | Train, predict, baselines, serialización | Lógica de decisión |
| `src/decision/` | Costos, buffers, recomendación, políticas | Código de modelo |
| `src/monitoring/` | Drift, alertas, métricas de operación | Lógica de negocio |
| `src/visualization/` | Gráficas reutilizables (plotly) | Lógica de datos |

## Reglas de imports

- `src/decision/` puede importar de `src/models/` pero NO al revés.
- `src/models/` puede importar de `src/features/` pero NO al revés.
- `src/features/` puede importar de `src/data/` pero NO al revés.
- `src/visualization/` puede importar de cualquier módulo.
- `src/monitoring/` puede importar de cualquier módulo.
- `scripts/` importa de `src/` libremente.
- `tests/` importa de `src/` libremente.

## Convenciones de nombres

- Módulos: snake_case (ej: `feature_engineering.py`)
- Clases: PascalCase (ej: `LiquidityRecommender`)
- Funciones: snake_case (ej: `calculate_total_cost`)
- Constantes: UPPER_SNAKE_CASE (ej: `DEFAULT_SERVICE_LEVEL`)
- Tests: `test_` + nombre del módulo (ej: `test_decision.py`)

## Archivos de datos

- raw/: Inmutables. Solo se generan una vez con semilla fija.
- processed/: Regenerables. Se producen en el pipeline.
- artifacts/: Modelos .joblib + metadata .json.
- outputs/: CSV de recomendaciones con timestamp.
