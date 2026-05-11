from dataclasses import dataclass
from pathlib import Path
from threading import Event
import pandas as pd

@dataclass
class ProcessContext:
    safe_dataframe: pd.DataFrame | None
    diretorio_export: Path
    cancel_event: Event
    canceled: bool = False
    error: Exception | None = None

    def reset_for_new_run(self) -> None:
        """Estado limpo antes de cada execução em thread (cancelamento/erro/evento)."""
        self.safe_dataframe = None
        self.diretorio_export = None
        self.canceled = False
        self.error = None
        self.cancel_event.clear()