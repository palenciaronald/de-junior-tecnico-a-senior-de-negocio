"""Validación de calidad del dataset de retiros diarios.

Uso:
    python -m src.data.validate
"""

import json
import sys
from pathlib import Path

import pandas as pd

from src.data.loader import load_raw_data
from src.data.schema import DATE_COLUMN, REQUIRED_COLUMNS, SCHEMA, TARGET_COLUMN

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def validate_columns(df: pd.DataFrame) -> list[str]:
    """Verifica que todas las columnas requeridas estén presentes."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return [f"Columna faltante: {c}" for c in missing]


def validate_nulls(df: pd.DataFrame) -> list[str]:
    """Detecta valores nulos por columna."""
    issues = []
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            issues.append(f"Nulos en {col}: {count} ({count/len(df)*100:.1f}%)")
    return issues


def validate_duplicates(df: pd.DataFrame) -> list[str]:
    """Detecta fechas duplicadas."""
    dupes = df[DATE_COLUMN].duplicated().sum()
    if dupes > 0:
        return [f"Fechas duplicadas: {dupes}"]
    return []


def validate_chronological_order(df: pd.DataFrame) -> list[str]:
    """Verifica que los datos estén ordenados cronológicamente."""
    if not df[DATE_COLUMN].is_monotonic_increasing:
        return ["Los datos NO están ordenados cronológicamente"]
    return []


def validate_ranges(df: pd.DataFrame) -> list[str]:
    """Verifica rangos esperados de las columnas numéricas."""
    issues = []
    for col, spec in SCHEMA.items():
        if col not in df.columns:
            continue
        if "min" in spec and df[col].min() < spec["min"]:
            issues.append(f"{col}: valor mínimo {df[col].min()} < esperado {spec['min']}")
        if "max" in spec and df[col].max() > spec["max"]:
            issues.append(f"{col}: valor máximo {df[col].max()} > esperado {spec['max']}")
        if "values" in spec:
            invalid = set(df[col].dropna().unique()) - set(spec["values"])
            if invalid:
                issues.append(f"{col}: valores inesperados {invalid}")
    return issues


def validate_continuity(df: pd.DataFrame) -> list[str]:
    """Verifica continuidad temporal (sin gaps)."""
    dates = pd.to_datetime(df[DATE_COLUMN])
    date_range = pd.date_range(start=dates.min(), end=dates.max(), freq="D")
    missing_dates = set(date_range) - set(dates)
    if missing_dates:
        return [f"Días faltantes en la serie: {len(missing_dates)}"]
    return []


def validate_outliers(df: pd.DataFrame) -> list[str]:
    """Detecta outliers extremos en la variable objetivo."""
    issues = []
    target = df[TARGET_COLUMN]
    q1 = target.quantile(0.25)
    q3 = target.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 3 * iqr
    upper = q3 + 3 * iqr

    outliers_low = (target < lower).sum()
    outliers_high = (target > upper).sum()

    if outliers_low > 0:
        issues.append(f"Outliers bajos (< {lower/1e9:.1f}B): {outliers_low}")
    if outliers_high > 0:
        issues.append(f"Outliers altos (> {upper/1e9:.1f}B): {outliers_high}")

    return issues


def run_validation(df: pd.DataFrame) -> dict:
    """Ejecuta todas las validaciones y retorna el reporte."""
    report = {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "date_range": {
            "start": str(df[DATE_COLUMN].min().date()),
            "end": str(df[DATE_COLUMN].max().date()),
            "days": len(df),
        },
        "target_stats": {
            "mean": float(df[TARGET_COLUMN].mean()),
            "median": float(df[TARGET_COLUMN].median()),
            "std": float(df[TARGET_COLUMN].std()),
            "min": float(df[TARGET_COLUMN].min()),
            "max": float(df[TARGET_COLUMN].max()),
        },
        "issues": [],
        "warnings": [],
        "status": "OK",
    }

    # Validaciones bloqueantes
    report["issues"].extend(validate_columns(df))
    report["issues"].extend(validate_duplicates(df))

    # Validaciones de advertencia
    report["warnings"].extend(validate_nulls(df))
    report["warnings"].extend(validate_chronological_order(df))
    report["warnings"].extend(validate_ranges(df))
    report["warnings"].extend(validate_continuity(df))
    report["warnings"].extend(validate_outliers(df))

    if report["issues"]:
        report["status"] = "FAIL"
    elif report["warnings"]:
        report["status"] = "WARNING"

    return report


def main():
    """Punto de entrada para validación desde línea de comandos."""
    print("🔍 Validando datos...")
    df = load_raw_data()
    report = run_validation(df)

    # Guardar reporte
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "data_quality_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    # Mostrar resultados
    print(f"   Shape: {report['shape']}")
    print(f"   Rango: {report['date_range']['start']} a {report['date_range']['end']}")
    print(f"   Media retiros: {report['target_stats']['mean']/1e9:.1f}B COP")

    if report["issues"]:
        print(f"\n❌ ERRORES BLOQUEANTES ({len(report['issues'])}):")
        for issue in report["issues"]:
            print(f"   • {issue}")

    if report["warnings"]:
        print(f"\n⚠️  ADVERTENCIAS ({len(report['warnings'])}):")
        for warning in report["warnings"]:
            print(f"   • {warning}")

    if report["status"] == "OK":
        print("\n✅ Datos válidos — listos para modelado.")
    elif report["status"] == "WARNING":
        print("\n✅ Datos usables con advertencias documentadas.")
    else:
        print("\n❌ Datos NO aptos — resolver errores antes de continuar.")
        sys.exit(1)

    print(f"\n📄 Reporte guardado: {report_path}")


if __name__ == "__main__":
    main()
