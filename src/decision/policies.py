"""Políticas de reserva de liquidez."""

import numpy as np


def traditional_policy(history_7d: np.ndarray, buffer_pct: float = 0.10) -> float:
    """Política tradicional: max(últimos 7 días) * (1 + buffer).

    Args:
        history_7d: Array con retiros de los últimos 7 días.
        buffer_pct: Porcentaje de buffer (default 10%).

    Returns:
        Monto recomendado para reservar.
    """
    return float(np.max(history_7d) * (1 + buffer_pct))


def model_policy(
    forecast_central: float,
    forecast_quantile: float,
    service_level: float = 0.95,
) -> float:
    """Política basada en modelo: usa cuantil como recomendación.

    Args:
        forecast_central: Pronóstico central (media).
        forecast_quantile: Pronóstico del cuantil superior.
        service_level: Nivel de servicio deseado.

    Returns:
        Monto recomendado para reservar.
    """
    return float(forecast_quantile)


def buffer_policy(forecast_central: float, buffer_pct: float = 0.20) -> float:
    """Política de buffer fijo sobre pronóstico central.

    Args:
        forecast_central: Pronóstico central.
        buffer_pct: Porcentaje de buffer.

    Returns:
        Monto recomendado.
    """
    return float(forecast_central * (1 + buffer_pct))
