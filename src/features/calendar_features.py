"""Features de calendario (ya existen en el dataset, este módulo las enriquece)."""

import pandas as pd

from src.data.schema import DATE_COLUMN


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega features de calendario adicionales.

    Las features base (day_of_week, is_weekend, is_holiday, is_payday,
    is_month_end, days_to_payday) ya vienen del script de generación.
    Este módulo agrega el mes como feature adicional.

    Todas las features de calendario del día D+1 son válidas porque
    se conocen de antemano.

    Args:
        df: DataFrame con columna date.

    Returns:
        DataFrame con columna month agregada.
    """
    df = df.copy()
    df["month"] = df[DATE_COLUMN].dt.month
    return df
