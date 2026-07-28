"""Features basadas en ventanas móviles."""

import pandas as pd

from src.data.schema import TARGET_COLUMN


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega promedios móviles y desviación estándar.

    Todas las ventanas se calculan con información estrictamente pasada
    (shift(1) para excluir el día actual que aún no ha cerrado).

    Args:
        df: DataFrame ordenado cronológicamente con columna target.

    Returns:
        DataFrame con columnas rolling_mean_7, rolling_mean_14, rolling_std_7.
    """
    df = df.copy()
    target_shifted = df[TARGET_COLUMN].shift(1)

    df["rolling_mean_7"] = target_shifted.rolling(window=7, min_periods=7).mean()
    df["rolling_mean_14"] = target_shifted.rolling(window=14, min_periods=14).mean()
    df["rolling_std_7"] = target_shifted.rolling(window=7, min_periods=7).std()

    return df
