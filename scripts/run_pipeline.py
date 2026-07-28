"""Pipeline completo ejecutable.

Uso:
    python scripts/run_pipeline.py
"""

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("Generando datos", [sys.executable, "scripts/generate_synthetic_data.py"]),
    ("Validando datos", [sys.executable, "-m", "src.data.validate"]),
    ("Construyendo features", [sys.executable, "-m", "src.features.build"]),
    ("Entrenando modelo", [sys.executable, "-m", "src.models.train"]),
    ("Evaluando modelo", [sys.executable, "-m", "src.models.evaluate"]),
    ("Generando recomendación", [sys.executable, "-m", "src.decision.recommend"]),
]


def main():
    print("🚀 Pipeline completo de liquidez")
    print("=" * 50)

    start = time.time()

    for i, (name, cmd) in enumerate(STEPS, 1):
        print(f"\n[{i}/{len(STEPS)}] {name}...")
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ ERROR en paso {i}: {name}")
            print(result.stderr)
            sys.exit(1)
        else:
            # Mostrar última línea del output
            lines = result.stdout.strip().split("\n")
            if lines:
                print(f"   {lines[-1]}")

    elapsed = time.time() - start
    print(f"\n{'=' * 50}")
    print(f"✅ Pipeline completo en {elapsed:.1f}s")
    print(f"\nArtefactos generados:")
    print(f"  - data/raw/daily_withdrawals.csv")
    print(f"  - data/processed/features.csv")
    print(f"  - artifacts/model.joblib")
    print(f"  - outputs/daily_recommendation.csv")
    print(f"\nPara ver el dashboard: streamlit run app.py")


if __name__ == "__main__":
    main()
