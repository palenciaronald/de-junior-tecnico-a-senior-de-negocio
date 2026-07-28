"""Orquestador de feature engineering.

Uso:
    python -m src.features.build
"""

from pathlib import Path

import pandas as pd

from src.data.loader import load_raw_data
from src.data.schema import DATE_COLUMN, TARGET_COLUMN
from src.features.calendar_features import add_calendar_features
from src.features.lag_features import add_lag_features
from src.features.rolling_features import add_rolling_features

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construye todas las features para modelado.

    Pipeline:
    1. Ordenar cronológicamente.
    2. Agregar lags (1, 7, 14 días).
    3. Agregar ventanas móviles (mean_7, mean_14, std_7).
    4. Agregar features de calendario (month).
    5. Eliminar filas con NaN por warm-up de lags/rolling.

    Args:
        df: DataFrame crudo con columnas del esquema.

    Returns:
        DataFrame con features listas para modelado (sin NaN).
    """
    df = df.sort_values(DATE_COLUMN).reset_index(drop=True)

    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = add_calendar_features(df)

    # Eliminar filas con NaN (warm-up de 14 días para lags + 1 para rolling)
    df = df.dropna().reset_index(drop=True)

    return df


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """Retorna las columnas que son features (excluye date y target)."""
    exclude = {DATE_COLUMN, TARGET_COLUMN}
    return [c for c in df.columns if c not in exclude]


def split_temporal(
    df: pd.DataFrame, train_ratio: float = 0.8
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separación temporal cronológica (NUNCA random).

    Args:
        df: DataFrame ordenado cronológicamente.
        train_ratio: Proporción de datos para entrenamiento.

    Returns:
        Tupla (train_df, test_df).
    """
    n = len(df)
    split_idx = int(n * train_ratio)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    return train_df, test_df


def main():
    """Genera el dataset procesado con features."""
    print("🔧 Construyendo features...")

    df = load_raw_data()
    df = build_features(df)

    # Guardar
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "features.csv"
    df.to_csv(output_path, index=False)

    print(f"   Shape: {df.shape}")
    print(f"   Periodo: {df[DATE_COLUMN].min().date()} a {df[DATE_COLUMN].max().date()}")
    print(f"   Features: {get_feature_columns(df)}")

    # Mostrar separación temporal
    train_df, test_df = split_temporal(df)
    print(f"\n📊 Separación temporal:")
    print(f"   Train: {len(train_df)} días ({train_df[DATE_COLUMN].min().date()} a {train_df[DATE_COLUMN].max().date()})")
    print(f"   Test:  {len(test_df)} días ({test_df[DATE_COLUMN].min().date()} a {test_df[DATE_COLUMN].max().date()})")

    print(f"\n✅ Guardado: {output_path}")


if __name__ == "__main__":
    main()
