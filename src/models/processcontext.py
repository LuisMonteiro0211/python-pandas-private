from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Callable

import pandas as pd

ProgressCallback = Callable[[int, int], None]


@dataclass
class ProcessContext:
    safe_dataframe: pd.DataFrame | None
    diretorio_export: Path
    cancel_event: Event
    total_jobs: int = 0
    completed_jobs: int = 0
    canceled: bool = False
    error: Exception | None = None
    on_progress: ProgressCallback | None = None

    def reset_for_new_run(self) -> None:
        """Estado limpo antes de cada execução em thread (cancelamento/erro/evento)."""
        self.safe_dataframe = None
        self.diretorio_export = None
        self.canceled = False
        self.error = None
        self.cancel_event.clear()
        self.total_jobs = 0
        self.completed_jobs = 0