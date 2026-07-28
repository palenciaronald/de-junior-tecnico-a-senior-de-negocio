"""Features basadas en lags temporales."""

import pandas as pd

from src.data.schema import TARGET_COLUMN


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega lags de la variable objetivo.

    Lags disponibles al cierre del día D para predecir D+1:
    - lag_1: retiro de ayer (D)
    - lag_7: retiro del mismo día de semana anterior (D-6)
    - lag_14: retiro de hace 2 semanas (D-13)

    Args:
        df: DataFrame ordenado cronológicamente con columna target.

    Returns:
        DataFrame con columnas lag_1, lag_7, lag_14 agregadas.
    """
    df = df.copy()
    df["lag_1"] = df[TARGET_COLUMN].shift(1)
    df["lag_7"] = df[TARGET_COLUMN].shift(7)
    df["lag_14"] = df[TARGET_COLUMN].shift(14)
    return df
