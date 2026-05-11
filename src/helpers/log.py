"""Configuração centralizada de logging (arquivo + console)."""

import logging as lg
from pathlib import Path


def setup_logging(log_dir: Path) -> None:
    """
    Configura o logging para arquivo e console.

    Args:
        log_dir: Diretório onde o arquivo de log será gravado.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    file_handler = lg.FileHandler(
        filename=log_dir / "app.log",
        mode="a",
        encoding="utf-8",
    )
    file_handler.setLevel(lg.INFO)
    file_handler.setFormatter(lg.Formatter(log_format, datefmt=date_format))

    console_handler = lg.StreamHandler()
    console_handler.setLevel(lg.INFO)
    console_handler.setFormatter(lg.Formatter(log_format, datefmt=date_format))

    lg.basicConfig(
        level=lg.INFO,
        handlers=[file_handler, console_handler],
    )