"""Modelos baseline para pronóstico de retiros.

Uso:
    python -m src.models.baselines
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.data.schema import TARGET_COLUMN
from src.features.build import build_features, get_feature_columns, split_temporal
from src.data.loader import load_raw_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class NaiveLag1:
    """Baseline: predicción = retiro del día anterior."""

    name = "NaiveLag1"

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predice usando lag_1."""
        return df["lag_1"].values


class NaiveLag7:
    """Baseline: predicción = retiro del mismo día de semana anterior."""

    name = "NaiveLag7"

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predice usando lag_7."""
        return df["lag_7"].values


class MovingAverage7:
    """Baseline: predicción = promedio de los últimos 7 días."""

    name = "MovingAverage7"

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predice usando rolling_mean_7."""
        return df["rolling_mean_7"].values


def evaluate_baseline(
    y_true: np.ndarray, y_pred: np.ndarray
) -> dict[str, float]:
    """Calcula métricas para un baseline.

    Args:
        y_true: Valores reales.
        y_pred: Predicciones del baseline.

    Returns:
        Dict con MAE, RMSE, WAPE.
    """
    errors = y_true - y_pred
    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors**2))
    wape = np.sum(np.abs(errors)) / np.sum(np.abs(y_true))

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "wape": float(wape),
        "mae_billions": float(mae / 1e9),
    }


def main():
    """Evalúa los 3 baselines sobre el conjunto de test."""
    import json

    print("📊 Evaluando baselines...")

    df = load_raw_data()
    df = build_features(df)
    train_df, test_df = split_temporal(df)

    y_test = test_df[TARGET_COLUMN].values

    baselines = [NaiveLag1(), NaiveLag7(), MovingAverage7()]
    results = {}

    for baseline in baselines:
        y_pred = baseline.predict(test_df)
        metrics = evaluate_baseline(y_test, y_pred)
        results[baseline.name] = metrics
        print(f"\n   {baseline.name}:")
        print(f"     MAE:  {metrics['mae_billions']:.2f}B COP")
        print(f"     RMSE: {metrics['rmse']/1e9:.2f}B COP")
        print(f"     WAPE: {metrics['wape']:.4f} ({metrics['wape']*100:.2f}%)")

    # Guardar resultados
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "baseline_metrics.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Métricas guardadas: {report_path}")

    # Mejor baseline
    best = min(results.items(), key=lambda x: x[1]["mae"])
    print(f"\n🏆 Mejor baseline: {best[0]} (MAE: {best[1]['mae_billions']:.2f}B COP)")


if __name__ == "__main__":
    main()
