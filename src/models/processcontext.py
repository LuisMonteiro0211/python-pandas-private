from dataclasses import dataclass
from pathlib import Path
from threading import Event
import pandas as pd

@dataclass
class ProcessContext:
    safe_dataframe: pd.DataFrame | None
    diretorio_export: Path
    cancel_event: Event