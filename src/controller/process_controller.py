import pandas as pd
from pathlib import Path
from src.services.process_spreadsheet import process_spreadsheet
import threading


class ProcessController(threading.Thread):
    def __init__(self, safe_dataframe: pd.DataFrame, diretorio_export: Path):
        super().__init__()
        self.safe_dataframe = safe_dataframe
        self.diretorio_export = diretorio_export
        self.result = None
        self.error = None

    def run(self):
        try:
            self.result = process_spreadsheet(self.safe_dataframe, self.diretorio_export)
        except Exception as e:
            self.error = e