"""
Genera el dataset de trabajo a partir de cajeros_raw.xlsx.

Agrega las filas duplicadas por fecha (hay dos registros por día),
enriquece con variables de calendario y guarda como CSV.

Uso:
    python scripts/generate_synthetic_data.py

Output:
    data/raw/daily_withdrawals.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
INPUT_FILE = RAW_DIR / "cajeros_raw.xlsx"
OUTPUT_FILE = RAW_DIR / "daily_withdrawals.csv"

# Festivos colombianos (aproximados, fechas fijas + algunos móviles)
COLOMBIAN_HOLIDAYS = [
    # 2024
    "2024-01-01", "2024-01-08", "2024-03-25", "2024-03-28", "2024-03-29",
    "2024-05-01", "2024-05-13", "2024-06-03", "2024-06-10", "2024-07-01",
    "2024-07-20", "2024-08-07", "2024-08-19", "2024-10-14", "2024-11-04",
    "2024-11-11", "2024-12-08", "2024-12-25",
    # 2025
    "2025-01-01", "2025-01-06", "2025-03-24", "2025-04-17", "2025-04-18",
    "2025-05-01", "2025-06-02", "2025-06-23", "2025-06-30", "2025-07-20",
    "2025-08-07", "2025-08-18", "2025-10-13", "2025-11-03", "2025-11-17",
    "2025-12-08", "2025-12-25",
    # 2026
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03",
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29",
    "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12", "2026-11-02",
    "2026-11-16", "2026-12-08", "2026-12-25",
]


def load_and_aggregate(path: Path) -> pd.DataFrame:
    """Carga el xlsx y agrega por fecha (suma los registros del mismo día)."""
    df = pd.read_excel(path)

    # Usar solo columnas relevantes
    df = df[["FECHA_CAJEROS", "TOTAL_TRANSACIONES", "VALOR_TOTAL"]].copy()
    df.columns = ["date", "transaction_count", "total_withdrawals_cop"]

    # Parsear fechas
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    # Agregar por fecha (hay 2 registros por día en muchas fechas)
    df = (
        df.groupby("date", as_index=False)
        .agg({"transaction_count": "sum", "total_withdrawals_cop": "sum"})
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega variables de calendario."""
    holidays = set(pd.to_datetime(COLOMBIAN_HOLIDAYS).date)

    df["day_of_week"] = df["date"].dt.dayofweek  # 0=lunes, 6=domingo
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["is_holiday"] = df["date"].dt.date.map(lambda d: int(d in holidays))

    # Quincena: día 15 o último día del mes
    df["is_payday"] = (
        (df["date"].dt.day == 15) | (df["date"].dt.is_month_end)
    ).astype(int)

    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)

    # Días hasta la próxima quincena (15 o fin de mes)
    def days_to_payday(date):
        day = date.day
        if day <= 15:
            return 15 - day
        else:
            # Días hasta fin de mes
            last_day = pd.Timestamp(date.year, date.month, 1) + pd.offsets.MonthEnd(0)
            return (last_day.date() - date).days

    df["days_to_payday"] = df["date"].dt.date.map(days_to_payday)

    return df


def add_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega componente de tendencia normalizada."""
    df["trend"] = np.arange(len(df)) / len(df)
    return df


def add_special_events(df: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """Marca días extraordinarios (picos inusuales)."""
    rng = np.random.default_rng(seed)

    # Identificar valores extremos (por encima del percentil 97)
    threshold = df["total_withdrawals_cop"].quantile(0.97)
    df["special_event"] = (df["total_withdrawals_cop"] > threshold).astype(int)

    return df


def main():
    print("📂 Cargando cajeros_raw.xlsx...")
    df = load_and_aggregate(INPUT_FILE)
    print(f"   {len(df)} días únicos ({df['date'].min().date()} a {df['date'].max().date()})")

    print("📅 Agregando features de calendario...")
    df = add_calendar_features(df)

    print("📈 Agregando tendencia...")
    df = add_trend(df)

    print("⚡ Marcando eventos especiales...")
    df = add_special_events(df)

    # Reordenar columnas según spec
    columns_order = [
        "date",
        "total_withdrawals_cop",
        "transaction_count",
        "day_of_week",
        "is_weekend",
        "is_holiday",
        "is_payday",
        "is_month_end",
        "days_to_payday",
        "trend",
        "special_event",
    ]
    df = df[columns_order]

    # Guardar
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Guardado: {OUTPUT_FILE}")
    print(f"   Shape: {df.shape}")
    print(f"   Columnas: {df.columns.tolist()}")


if __name__ == "__main__":
    main()
