"""Diretórios base do projeto (logs, exports).

Em desenvolvimento, a raiz é o diretório do repositório (onde está ``run_gui.py``).
Em executável empacotado (PyInstaller), a raiz é a pasta do executável.
"""

import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # PyInstaller: gravar ao lado do .exe (pasta do usuário / instalador).
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # src/utils/paths.py -> parent=utils, parent.parent=src, parent.parent.parent=raiz do repo
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGS_DIR = BASE_DIR / "logs"
EXPORTS_DIR = BASE_DIR / "exports"
