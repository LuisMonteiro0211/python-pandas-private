from src.controller.process_controller import ProcessController
from src.controller.sanitize_controller import SanitizeController
from threading import Event
from src.models.processcontext import ProcessContext
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.gui.app import App
from src.gui.dialogs import (
    ask_excel_file,
    ask_save_directory,
    show_error,
    show_success,
    show_warning,
)

class AppController():
    def __init__(self, view: App):
        self.view = view
        self.safe_dataframe = None
        self.diretorio_export = None
        self.canceled = None
        self.cancel_event = Event()

        self.process_context = ProcessContext(
            safe_dataframe=self.safe_dataframe,
            diretorio_export=self.diretorio_export,
            cancel_event=self.cancel_event,
        )

    def on_process(self):
        if self.safe_dataframe is None:
            show_warning("Carregue um arquivo para processar")
            return
        
        if self.diretorio_export is None:
            show_warning("Selecione um diretório para exportar")
            return

        self.process_thread = ProcessController(self.process_context) #Cria o objeto de thread
        self.process_thread.start() #Inicia a thread

        self.poll_process()

    def poll_process(self):
        if self.process_thread.is_alive():
            self.view.after(100, self.poll_process)

        if self.process_thread.canceled:
            show_warning("Processo cancelado")

        if self.process_thread.error is not None:
            show_error(str(self.process_thread.error))

        else:
            show_success("Processo concluído com sucesso")

    def on_load_file(self):  
        file_path = ask_excel_file(self.view)

        if file_path is None:
            return

        sanitize = SanitizeController(file_path=file_path)
        sanitize.start()
        sanitize.join()

        if sanitize.error is not None:
            show_error(str(sanitize.error))

            if sanitize.dataframe is not None:
                self.view.tabela.update_data(sanitize.dataframe)

        else:
            show_success("Planilha carregada com sucesso!")
            self.view.tabela.update_data(sanitize.result)
            self.safe_dataframe = sanitize.result

        
    def on_export(self):
        save_directory = ask_save_directory(self.view)

        if save_directory is None:
            show_warning("Diretório não selecionado")
            return

        self.diretorio_export = save_directory


    def on_cancel(self):
        pass
