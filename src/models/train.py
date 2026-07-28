"""Entrenamiento del modelo de pronóstico de retiros.

Uso:
    python -m src.models.train
"""

import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from src.data.loader import load_raw_data
from src.data.schema import TARGET_COLUMN
from src.features.build import build_features, get_feature_columns, split_temporal
from src.models.metrics import mae, rmse, wape

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

SEED = 42
MODEL_VERSION = "1.0.0"


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    feature_names: list[str],
) -> dict:
    """Entrena modelo central y cuantil.

    Args:
        X_train: Features de entrenamiento.
        y_train: Target de entrenamiento.
        feature_names: Nombres de las features.

    Returns:
        Dict con modelo central, modelo cuantil y metadata.
    """
    # Modelo central (pronóstico promedio)
    model_central = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        random_state=SEED,
        loss="squared_error",
    )
    model_central.fit(X_train, y_train)

    # Modelo cuantil 95 (límite superior para decisión)
    model_quantile = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        random_state=SEED,
        loss="quantile",
        alpha=0.95,
    )
    model_quantile.fit(X_train, y_train)

    return {
        "model_central": model_central,
        "model_quantile": model_quantile,
        "feature_names": feature_names,
        "version": MODEL_VERSION,
    }


def main():
    """Entrena y serializa el modelo."""
    print("🤖 Entrenando modelo...")

    # Cargar y preparar datos
    df = load_raw_data()
    df = build_features(df)
    train_df, test_df = split_temporal(df)

    feature_cols = get_feature_columns(df)
    X_train = train_df[feature_cols].values
    y_train = train_df[TARGET_COLUMN].values
    X_test = test_df[feature_cols].values
    y_test = test_df[TARGET_COLUMN].values

    print(f"   Train: {X_train.shape[0]} muestras, {X_train.shape[1]} features")
    print(f"   Test:  {X_test.shape[0]} muestras")

    # Entrenar
    result = train_model(X_train, y_train, feature_cols)
    model_central = result["model_central"]
    model_quantile = result["model_quantile"]

    # Evaluar en test
    y_pred_central = model_central.predict(X_test)
    y_pred_q95 = model_quantile.predict(X_test)

    metrics = {
        "mae": mae(y_test, y_pred_central),
        "rmse": rmse(y_test, y_pred_central),
        "wape": wape(y_test, y_pred_central),
        "mae_billions": mae(y_test, y_pred_central) / 1e9,
    }

    print(f"\n📈 Métricas en test (modelo central):")
    print(f"     MAE:  {metrics['mae_billions']:.2f}B COP")
    print(f"     RMSE: {metrics['rmse']/1e9:.2f}B COP")
    print(f"     WAPE: {metrics['wape']*100:.2f}%")

    # Serializar modelo
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = ARTIFACTS_DIR / "model.joblib"
    joblib.dump(result, model_path)
    print(f"\n💾 Modelo guardado: {model_path}")

    # Metadata
    metadata = {
        "version": MODEL_VERSION,
        "trained_at": datetime.now().isoformat(),
        "train_period": {
            "start": str(train_df["date"].min().date()),
            "end": str(train_df["date"].max().date()),
            "samples": len(train_df),
        },
        "test_period": {
            "start": str(test_df["date"].min().date()),
            "end": str(test_df["date"].max().date()),
            "samples": len(test_df),
        },
        "features": feature_cols,
        "hyperparameters": {
            "n_estimators": 200,
            "max_depth": 4,
            "learning_rate": 0.05,
            "random_state": SEED,
            "quantile_alpha": 0.95,
        },
        "metrics_test": metrics,
        "seed": SEED,
    }

    metadata_path = ARTIFACTS_DIR / "model_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"📄 Metadata guardada: {metadata_path}")

    print("\n✅ Entrenamiento completado.")


if __name__ == "__main__":
    main()
