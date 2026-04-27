from src.services.sanitize_dataframe import sanitize_dataframe
from src.helpers.helper import get_dataframe
import pandas as pd
import threading
from pathlib import Path

class SanitizeController(threading.Thread):
    """
    Controller para sanitizar um DataFrame.

    Args:
        file_path: Caminho do arquivo Excel a ser sanitizado.

    Returns:
        DataFrame sanitizado.

    Raises:
        ValueError: Se o DataFrame estiver vazio, contiver valores NaN ou espaços em branco.
    """
    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path
        self.result = None
        self.error = None

    def run(self) -> None:

        try:
            dataframe: pd.DataFrame = get_dataframe(self.file_path)

        except ValueError as e:
            self.error = e
            raise
        except FileNotFoundError as e:
            self.error = e
            raise

        try:
            dataframe: pd.DataFrame = sanitize_dataframe(dataframe)
            self.result = dataframe
        except ValueError as e:
            self.error = e
            self.result = dataframe