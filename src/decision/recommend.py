"""Generación de recomendación diaria de liquidez.

Uso:
    python -m src.decision.recommend
"""

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.loader import load_processed_data
from src.decision.costs import DEFAULT_COST_IDLE, DEFAULT_COST_SHORTAGE, DEFAULT_SERVICE_LEVEL
from src.models.predict import load_model, predict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def generate_recommendation(
    df: pd.DataFrame,
    model_dict: dict | None = None,
    cost_idle: float = DEFAULT_COST_IDLE,
    cost_shortage: float = DEFAULT_COST_SHORTAGE,
    service_level: float = DEFAULT_SERVICE_LEVEL,
) -> pd.DataFrame:
    """Genera recomendación diaria.

    Args:
        df: DataFrame con features.
        model_dict: Modelo cargado.
        cost_idle: Costo de ociosidad.
        cost_shortage: Costo de faltante.
        service_level: Nivel de servicio.

    Returns:
        DataFrame con la recomendación.
    """
    if model_dict is None:
        model_dict = load_model()

    predictions = predict(df, model_dict)
    forecast_central = predictions["central"]
    forecast_q95 = predictions["quantile_95"]

    recommended = forecast_q95  # Usar cuantil como recomendación
    buffer = recommended - forecast_central

    rec_df = pd.DataFrame({
        "date": df["date"],
        "forecast_central": forecast_central,
        "forecast_quantile_95": forecast_q95,
        "recommended_amount": recommended,
        "buffer": buffer,
        "service_level": service_level,
        "risk_shortage_pct": 1 - service_level,
        "cost_idle_expected": cost_idle * np.maximum(recommended - forecast_central, 0),
        "cost_shortage_expected": cost_shortage * np.maximum(forecast_central - recommended, 0),
        "model_version": model_dict["version"],
    })

    return rec_df


def main():
    """Genera y guarda la recomendación diaria."""
    print("📋 Generando recomendación diaria...")

    # Cargar datos procesados (usar test como ejemplo)
    test_path = PROJECT_ROOT / "data" / "processed" / "test.csv"
    df = pd.read_csv(test_path, parse_dates=["date"])

    rec_df = generate_recommendation(df)

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUTS_DIR / "daily_recommendation.csv"
    rec_df.to_csv(output_path, index=False)

    print(f"   Días: {len(rec_df)}")
    print(f"   Monto recomendado promedio: {rec_df['recommended_amount'].mean()/1e9:.1f}B COP")
    print(f"   Buffer promedio: {rec_df['buffer'].mean()/1e9:.1f}B COP")
    print(f"✅ Guardado: {output_path}")


if __name__ == "__main__":
    main()
