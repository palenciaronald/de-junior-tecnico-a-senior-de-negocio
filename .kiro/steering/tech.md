# Tech Steering

## Stack

- Python 3.11
- pandas >= 2.1, < 3.0
- numpy >= 1.25, < 2.0
- scikit-learn >= 1.3, < 2.0
- plotly >= 5.18, < 6.0
- streamlit >= 1.28, < 2.0
- joblib >= 1.3, < 2.0
- pytest >= 7.4, < 9.0

## Dependencias prohibidas

- Prophet
- XGBoost / LightGBM / CatBoost (requieren compilación extra)
- TensorFlow / PyTorch
- Servicios cloud (AWS, GCP, Azure SDKs)
- Bases de datos externas
- Cualquier paquete que requiera API key

## Versión de Python

Python 3.11.x obligatorio. Documentar instalación para Windows, macOS y Linux.

## Comandos principales

```bash
# Generar datos sintéticos
python scripts/generate_synthetic_data.py

# Validar datos
python -m src.data.validate

# Entrenar modelo
python -m src.models.train

# Evaluar modelo
python -m src.models.evaluate

# Generar recomendación
python -m src.decision.recommend

# Ejecutar dashboard
streamlit run app.py

# Ejecutar tests
pytest -q

# Pipeline completo
python scripts/run_pipeline.py
```

## Convenciones

- Código fuente en inglés (variables, funciones, clases, docstrings).
- UI, documentación y guías del taller en español.
- Usar pathlib para paths. No hardcodear separadores.
- UTF-8 en todos los archivos.
- Type hints en funciones públicas.
- Docstrings en formato Google.
- Semilla fija: 42 para reproducibilidad.
- No usar notebooks como camino principal. Scripts y módulos.

## Estructura de imports

```python
# Estándar
from pathlib import Path

# Terceros
import pandas as pd
import numpy as np

# Local
from src.data.validate import validate_schema
```

## Testing

- pytest como framework.
- Tests en tests/ con prefijo test_.
- Fixtures compartidas en conftest.py.
- Cada módulo debe tener al menos un test.
