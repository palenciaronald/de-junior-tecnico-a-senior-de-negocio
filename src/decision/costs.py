"""Funciones puras de costos para la capa de decisión."""

import numpy as np

DEFAULT_COST_IDLE = 0.0001      # 0.01% del exceso por día
DEFAULT_COST_SHORTAGE = 0.0005  # 0.05% del faltante por día
DEFAULT_SERVICE_LEVEL = 0.95


def calculate_idle_money(reserved: float, actual: float) -> float:
    """Dinero ocioso: max(reservado - real, 0)."""
    return max(reserved - actual, 0.0)


def calculate_shortage(reserved: float, actual: float) -> float:
    """Faltante: max(real - reservado, 0)."""
    return max(actual - reserved, 0.0)


def calculate_total_cost(
    reserved: float,
    actual: float,
    cost_idle: float = DEFAULT_COST_IDLE,
    cost_shortage: float = DEFAULT_COST_SHORTAGE,
) -> float:
    """Costo total: C(q,y) = c_idle * max(q-y,0) + c_shortage * max(y-q,0)."""
    idle = calculate_idle_money(reserved, actual)
    shortage = calculate_shortage(reserved, actual)
    return cost_idle * idle + cost_shortage * shortage


def calculate_costs_array(
    reserved: np.ndarray,
    actual: np.ndarray,
    cost_idle: float = DEFAULT_COST_IDLE,
    cost_shortage: float = DEFAULT_COST_SHORTAGE,
) -> dict:
    """Calcula costos para arrays completos."""
    idle = np.maximum(reserved - actual, 0)
    shortage = np.maximum(actual - reserved, 0)
    cost_idle_arr = cost_idle * idle
    cost_shortage_arr = cost_shortage * shortage
    total = cost_idle_arr + cost_shortage_arr

    return {
        "idle_daily_mean": float(np.mean(idle)),
        "shortage_daily_mean": float(np.mean(shortage)),
        "days_with_shortage_pct": float(np.mean(shortage > 0) * 100),
        "service_level_pct": float(np.mean(reserved >= actual) * 100),
        "cost_total_period": float(np.sum(total)),
        "cost_daily_mean": float(np.mean(total)),
    }
