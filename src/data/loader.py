"""Funciones de carga de datos."""

from pathlib import Path

import pandas as pd

from src.data.schema import DATE_COLUMN

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw_data(path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset de retiros diarios desde CSV.

    Args:
        path: Ruta al CSV. Si es None, usa la ruta por defecto.

    Returns:
        DataFrame con columna date parseada como datetime.
    """
    if path is None:
        path = RAW_DIR / "daily_withdrawals.csv"

    df = pd.read_csv(path, parse_dates=[DATE_COLUMN])
    return df


def load_processed_data(path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset procesado con features.

    Args:
        path: Ruta al CSV. Si es None, usa la ruta por defecto.

    Returns:
        DataFrame con features listas para modelado.
    """
    if path is None:
        path = PROCESSED_DIR / "features.csv"

    df = pd.read_csv(path, parse_dates=[DATE_COLUMN])
    return df
