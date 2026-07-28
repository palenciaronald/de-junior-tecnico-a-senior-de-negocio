"""Inferencia desde modelo serializado."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def load_model(path: Path | None = None) -> dict:
    """Carga el modelo serializado.

    Args:
        path: Ruta al archivo .joblib. Si None, usa la ruta por defecto.

    Returns:
        Dict con model_central, model_quantile, feature_names, version.
    """
    if path is None:
        path = ARTIFACTS_DIR / "model.joblib"
    return joblib.load(path)


def predict(
    df: pd.DataFrame,
    model_dict: dict | None = None,
) -> dict[str, np.ndarray]:
    """Genera predicciones central y cuantil.

    Args:
        df: DataFrame con las features necesarias.
        model_dict: Modelo cargado. Si None, carga el default.

    Returns:
        Dict con 'central' y 'quantile_95' como arrays.
    """
    if model_dict is None:
        model_dict = load_model()

    feature_names = model_dict["feature_names"]
    X = df[feature_names].values

    y_central = model_dict["model_central"].predict(X)
    y_quantile = model_dict["model_quantile"].predict(X)

    return {
        "central": y_central,
        "quantile_95": y_quantile,
    }
