"""Ejecuta un notebook y guarda la versión ejecutada.

Uso:
    python scripts/run_notebook.py notebooks/01_data_understanding.ipynb
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def run_notebook(path: str, timeout: int = 600) -> bool:
    """Ejecuta un notebook in-place.

    Args:
        path: Ruta al notebook.
        timeout: Timeout por celda en segundos.

    Returns:
        True si ejecutó sin errores.
    """
    nb_path = Path(path)
    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(nb_path.parent)}},
    )
    try:
        client.execute()
        nbformat.write(nb, nb_path)
        print(f"✅ Notebook ejecutado: {nb_path}")
        return True
    except Exception as e:
        nbformat.write(nb, nb_path)
        print(f"❌ Error en notebook {nb_path}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/run_notebook.py <path_to_notebook>")
        sys.exit(1)
    success = run_notebook(sys.argv[1])
    sys.exit(0 if success else 1)
