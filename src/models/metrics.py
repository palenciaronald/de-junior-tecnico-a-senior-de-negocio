"""Funciones de métricas para evaluación de modelos."""

import numpy as np


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Error absoluto medio.

    Args:
        y_true: Valores reales.
        y_pred: Predicciones.

    Returns:
        MAE en las mismas unidades que y.
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Raíz del error cuadrático medio.

    Args:
        y_true: Valores reales.
        y_pred: Predicciones.

    Returns:
        RMSE en las mismas unidades que y.
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Error porcentual absoluto ponderado.

    Args:
        y_true: Valores reales.
        y_pred: Predicciones.

    Returns:
        WAPE como proporción (0-1).
    """
    return float(np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)))


def pinball_loss(y_true: np.ndarray, y_pred: np.ndarray, alpha: float = 0.95) -> float:
    """Pinball loss para evaluación de cuantiles.

    Args:
        y_true: Valores reales.
        y_pred: Predicción del cuantil.
        alpha: Nivel del cuantil (0-1).

    Returns:
        Pinball loss promedio.
    """
    errors = y_true - y_pred
    loss = np.where(errors >= 0, alpha * errors, (alpha - 1) * errors)
    return float(np.mean(loss))


def interval_coverage(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    """Cobertura del intervalo de predicción.

    Args:
        y_true: Valores reales.
        lower: Límite inferior del intervalo.
        upper: Límite superior del intervalo.

    Returns:
        Proporción de observaciones dentro del intervalo (0-1).
    """
    within = (y_true >= lower) & (y_true <= upper)
    return float(np.mean(within))


def high_demand_error(
    y_true: np.ndarray, y_pred: np.ndarray, mask: np.ndarray
) -> float:
    """Error en días de alta demanda.

    Args:
        y_true: Valores reales.
        y_pred: Predicciones.
        mask: Máscara booleana de días de alta demanda.

    Returns:
        MAE solo en días de alta demanda.
    """
    if mask.sum() == 0:
        return 0.0
    return float(np.mean(np.abs(y_true[mask] - y_pred[mask])))
