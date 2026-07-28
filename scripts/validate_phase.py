"""Valida artefactos de una fase del taller.

Uso:
    python scripts/validate_phase.py business-understanding
    python scripts/validate_phase.py data-understanding
    python scripts/validate_phase.py data-preparation
    python scripts/validate_phase.py modeling-tournament
    python scripts/validate_phase.py evaluation-business
    python scripts/validate_phase.py productization-deployment
"""
import json
import sys
from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = PROJECT_ROOT / "manifests"
SCHEMAS_DIR = PROJECT_ROOT / "schemas"

PHASE_CONFIG = {
    "business-understanding": {
        "manifest": "00_business_understanding.json",
        "report": "reports/00_business_understanding.md",
        "notebook": None,
    },
    "data-understanding": {
        "manifest": "01_data_understanding.json",
        "report": "reports/01_data_understanding.md",
        "notebook": "notebooks/01_data_understanding.ipynb",
    },
    "data-preparation": {
        "manifest": "02_data_preparation.json",
        "report": "reports/02_data_preparation.md",
        "notebook": "notebooks/02_data_preparation.ipynb",
    },
    "modeling-tournament": {
        "manifest": "03_model_tournament.json",
        "report": "reports/03_model_tournament.md",
        "notebook": "notebooks/03_model_tournament.ipynb",
    },
    "evaluation-business": {
        "manifest": "04_evaluation_business.json",
        "report": "reports/04_evaluation_business.md",
        "notebook": "notebooks/04_evaluation_business.ipynb",
    },
    "productization-deployment": {
        "manifest": "05_productization_deployment.json",
        "report": "reports/05_productization_deployment.md",
        "notebook": None,
    },
}


def validate_manifest(manifest_path: Path) -> list[str]:
    """Valida un manifest contra el schema."""
    errors = []
    if not manifest_path.exists():
        return [f"Manifest no existe: {manifest_path}"]

    with open(manifest_path) as f:
        data = json.load(f)

    required = ["phase", "status", "inputs", "outputs", "human_approved", "next_agent"]
    for field in required:
        if field not in data:
            errors.append(f"Campo faltante en manifest: {field}")

    if data.get("status") not in ("GO", "REVISAR", "NO-GO"):
        errors.append(f"Status inválido: {data.get('status')}")

    # Validar que outputs existan
    for output in data.get("outputs", []):
        if not (PROJECT_ROOT / output).exists():
            errors.append(f"Output declarado no existe: {output}")

    return errors


def validate_notebook(nb_path: Path) -> list[str]:
    """Valida que un notebook esté ejecutado sin errores."""
    errors = []
    if not nb_path.exists():
        return [f"Notebook no existe: {nb_path}"]

    nb = nbformat.read(nb_path, as_version=4)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    errors.append(f"Celda {i} tiene error: {output.get('ename')}")
            if not cell.get("outputs") and cell.source.strip():
                errors.append(f"Celda {i} no ejecutada (sin outputs)")

    return errors


def validate_phase(phase_name: str) -> bool:
    """Valida una fase completa."""
    if phase_name not in PHASE_CONFIG:
        print(f"❌ Fase desconocida: {phase_name}")
        print(f"   Opciones: {list(PHASE_CONFIG.keys())}")
        return False

    config = PHASE_CONFIG[phase_name]
    all_errors = []

    print(f"🔍 Validando fase: {phase_name}")

    # Manifest
    manifest_path = MANIFESTS_DIR / config["manifest"]
    manifest_errors = validate_manifest(manifest_path)
    all_errors.extend(manifest_errors)

    # Report
    report_path = PROJECT_ROOT / config["report"]
    if not report_path.exists():
        all_errors.append(f"Reporte no existe: {config['report']}")

    # Notebook (si aplica)
    if config["notebook"]:
        nb_path = PROJECT_ROOT / config["notebook"]
        nb_errors = validate_notebook(nb_path)
        all_errors.extend(nb_errors)

    # Resultado
    if all_errors:
        print(f"❌ {len(all_errors)} errores encontrados:")
        for err in all_errors:
            print(f"   • {err}")
        return False
    else:
        print(f"✅ Fase {phase_name} válida.")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/validate_phase.py <phase-name>")
        print(f"Fases: {list(PHASE_CONFIG.keys())}")
        sys.exit(1)

    success = validate_phase(sys.argv[1])
    sys.exit(0 if success else 1)
