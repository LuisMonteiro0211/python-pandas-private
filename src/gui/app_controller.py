"""Orquestra ações da interface: carregar, exportar, processar e cancelar.

Conecta a :class:`~src.gui.app.App` aos controllers em thread, agenda
atualizações da barra de progresso na thread principal do Tk via ``after``,
e mantém estado (DataFrame seguro, pasta de destino, estimativa de jobs).
"""

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
        self.cancel_event = Event()
        self.process_context = None
        self.sanitize_context = False
        self.estimated_jobs = 0

    def on_process(self):
        if self.safe_dataframe is None:
            show_warning("Carregue um arquivo para processar")
            return
        
        if self.diretorio_export is None:
            show_warning("Selecione um diretório para exportar")
            return

        if not self.sanitize_context:
            show_warning("Arquivo não sanitizado")
            return

        if self.process_context is not None:
            self.process_context.reset_for_new_run()

        self.process_context = ProcessContext(
            safe_dataframe=self.safe_dataframe,
            diretorio_export=self.diretorio_export,
            cancel_event=self.cancel_event,
            total_jobs=self.estimated_jobs,
            completed_jobs=0,
            error=None,
            on_progress=self._on_export_progress,
        )

        self.view.barra_de_progresso.reset_progress()
        self.view.barra_de_progresso.update_progress(0, self.estimated_jobs)

        self.process_thread = ProcessController(self.process_context)
        self.process_thread.start()

        self.view.baseboard.set_processing_locked("disabled")

        self.poll_process()

    def poll_process(self):
        if self.process_thread.is_alive():
            self.view.after(100, self.poll_process)
            return

        if self.process_context.canceled:
            show_warning("Processo cancelado")
            self.view.baseboard.set_processing_locked("normal")
            return

        if self.process_context.error is not None:
            show_error(str(self.process_context.error))
            self.view.baseboard.set_processing_locked("normal")
            return

        show_success("Processo concluído com sucesso")
        self.view.baseboard.set_processing_locked("normal")
        self.view.barra_de_progresso.update_progress(
            self.process_context.completed_jobs,
            self.process_context.total_jobs,
        )

    def _on_export_progress(self, completed: int, total: int) -> None:
        """Chamado na worker; agenda atualização da barra na thread da GUI."""
        self.view.after(
            0,
            lambda c=completed, t=total: self.view.barra_de_progresso.update_progress(c, t),
        )

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
            self.estimated_jobs = sanitize.estimated_jobs
            self.sanitize_context = True
        
    def on_export(self):
        save_directory = ask_save_directory(self.view)

        if save_directory is None:
            show_warning("Diretório não selecionado")
            return

        self.diretorio_export = save_directory

    def on_cancel(self):
        if self.cancel_event is not None:
            self.cancel_event.set()
