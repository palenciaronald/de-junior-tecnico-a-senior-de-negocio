"""Evaluación del modelo contra baselines.

Uso:
    python -m src.models.evaluate
"""

import json
from pathlib import Path

import numpy as np

from src.data.loader import load_raw_data
from src.data.schema import TARGET_COLUMN
from src.features.build import build_features, get_feature_columns, split_temporal
from src.models.baselines import MovingAverage7, NaiveLag1, NaiveLag7
from src.models.metrics import (
    high_demand_error,
    interval_coverage,
    mae,
    pinball_loss,
    rmse,
    wape,
)
from src.models.predict import load_model, predict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def main():
    """Evalúa modelo y compara contra baselines."""
    print("📊 Evaluando modelo vs baselines...")

    # Cargar datos y modelo
    df = load_raw_data()
    df = build_features(df)
    _, test_df = split_temporal(df)

    model_dict = load_model()
    feature_cols = get_feature_columns(df)

    y_test = test_df[TARGET_COLUMN].values

    # Predicciones del modelo
    predictions = predict(test_df, model_dict)
    y_pred_central = predictions["central"]
    y_pred_q95 = predictions["quantile_95"]

    # Máscara de alta demanda (quincena + fin de mes)
    high_demand_mask = (test_df["is_payday"].values == 1) | (test_df["is_month_end"].values == 1)

    # Métricas del modelo
    model_metrics = {
        "mae": mae(y_test, y_pred_central),
        "rmse": rmse(y_test, y_pred_central),
        "wape": wape(y_test, y_pred_central),
        "pinball_loss_95": pinball_loss(y_test, y_pred_q95, alpha=0.95),
        "coverage_95": interval_coverage(y_test, np.zeros_like(y_test), y_pred_q95),
        "high_demand_mae": high_demand_error(y_test, y_pred_central, high_demand_mask),
        "mae_billions": mae(y_test, y_pred_central) / 1e9,
    }

    print(f"\n🤖 Modelo GradientBoosting:")
    print(f"     MAE:  {model_metrics['mae_billions']:.2f}B COP")
    print(f"     RMSE: {model_metrics['rmse']/1e9:.2f}B COP")
    print(f"     WAPE: {model_metrics['wape']*100:.2f}%")
    print(f"     Pinball Loss (Q95): {model_metrics['pinball_loss_95']/1e9:.2f}B")
    print(f"     Cobertura Q95: {model_metrics['coverage_95']*100:.1f}%")
    print(f"     MAE alta demanda: {model_metrics['high_demand_mae']/1e9:.2f}B COP")

    # Baselines
    baselines = [NaiveLag1(), NaiveLag7(), MovingAverage7()]
    baseline_metrics = {}

    print(f"\n📏 Baselines:")
    for baseline in baselines:
        y_baseline = baseline.predict(test_df)
        metrics = {
            "mae": mae(y_test, y_baseline),
            "rmse": rmse(y_test, y_baseline),
            "wape": wape(y_test, y_baseline),
            "mae_billions": mae(y_test, y_baseline) / 1e9,
        }
        baseline_metrics[baseline.name] = metrics
        print(f"     {baseline.name}: MAE = {metrics['mae_billions']:.2f}B COP")

    # Comparación
    best_baseline_mae = min(m["mae"] for m in baseline_metrics.values())
    model_beats_all = model_metrics["mae"] < best_baseline_mae
    improvement_pct = (1 - model_metrics["mae"] / best_baseline_mae) * 100

    print(f"\n{'✅' if model_beats_all else '❌'} Modelo {'SUPERA' if model_beats_all else 'NO supera'} el mejor baseline")
    print(f"   Mejora vs MovingAverage7: {improvement_pct:.1f}%")

    # Guardar reporte
    report = {
        "model": {
            "name": "GradientBoostingRegressor",
            "version": model_dict["version"],
            "metrics": model_metrics,
        },
        "baselines": baseline_metrics,
        "comparison": {
            "beats_all_baselines": model_beats_all,
            "improvement_vs_best_baseline_pct": improvement_pct,
            "best_baseline": "MovingAverage7",
        },
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "model_evaluation.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Reporte guardado: {report_path}")

    if not model_beats_all:
        print("\n⚠️  ADVERTENCIA: El modelo no supera todos los baselines.")
        print("   Revisar features o hiperparámetros antes de continuar.")


if __name__ == "__main__":
    main()
