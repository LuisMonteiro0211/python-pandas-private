"""Configuração de logging da aplicação (arquivo em ``logs/app.log``)."""

import logging

from src.utils.paths import LOGS_DIR


def setup_logger() -> None:
    """Registra handler de arquivo na raiz do logger; idempotente se já houver handlers."""
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        LOGS_DIR / "app.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(file_handler)