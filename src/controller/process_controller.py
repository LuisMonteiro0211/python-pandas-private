from src.exceptions import ProcessCancelled
from src.models.processcontext import ProcessContext
from src.services.process_spreadsheet import process_spreadsheet
import threading


class ProcessController(threading.Thread):
    def __init__(self, process_context: ProcessContext):
        super().__init__()
        self.process_context = process_context
        self.result = None
        self.error: Exception | None = None
        self.canceled = False

    def run(self) -> None:
        try:
            self.result = process_spreadsheet(self.process_context)
        except ProcessCancelled:
            self.canceled = True
        except Exception as e:
            self.error = e
