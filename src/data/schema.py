"""Definición del esquema esperado para el dataset de retiros diarios."""

SCHEMA = {
    "date": {"type": "datetime64[ns]", "nullable": False},
    "total_withdrawals_cop": {"type": "float64", "nullable": False, "min": 0},
    "transaction_count": {"type": "int64", "nullable": False, "min": 0},
    "day_of_week": {"type": "int64", "nullable": False, "min": 0, "max": 6},
    "is_weekend": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_holiday": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_payday": {"type": "int64", "nullable": False, "values": [0, 1]},
    "is_month_end": {"type": "int64", "nullable": False, "values": [0, 1]},
    "days_to_payday": {"type": "int64", "nullable": False, "min": 0, "max": 15},
    "trend": {"type": "float64", "nullable": False, "min": 0.0, "max": 1.0},
    "special_event": {"type": "int64", "nullable": False, "values": [0, 1]},
}

REQUIRED_COLUMNS = list(SCHEMA.keys())
TARGET_COLUMN = "total_withdrawals_cop"
DATE_COLUMN = "date"
