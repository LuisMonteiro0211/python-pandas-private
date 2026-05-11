from src.models.processcontext import ProcessContext
from src.services.process_spreadsheet import process_spreadsheet
import threading

class ProcessController(threading.Thread):
    def __init__(self, process_context: ProcessContext):
        super().__init__()
        self.process_context = process_context

    def run(self) -> None:
        try:
            process_spreadsheet(self.process_context)
        except Exception as e:
            self.process_context.error = e
            return