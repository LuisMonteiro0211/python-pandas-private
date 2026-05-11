"""Cria diretórios de dados na raiz do projeto (logs, exports)."""

from src.utils.paths import (
    LOGS_DIR,
    EXPORTS_DIR,
)


def setup_environment() -> None:
    """
    Configura o ambiente do projeto.
    """

    directories = [LOGS_DIR, EXPORTS_DIR]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)