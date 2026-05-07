import customtkinter as ctk
from src.controller.sanitize_controller import SanitizeController
from src.controller.process_controller import ProcessController
from src.gui.components import DataTable, Sidebar, ProgressBar, Baseboard, Header
import pandas as pd
from src.gui.theme import COLORS, FONTS
from src.gui.dialogs import (
    ask_excel_file,
    ask_save_directory,
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._configurar_tela()
        self._configurar_widgets()

    def _configurar_tela(self):
        self.title("Python Pandas Analyzer")
        self.geometry("500x400")
        self.configure(fg_color=COLORS.app_background)
        self.resizable(False, False)
    
    def _configurar_widgets(self):
        #Chama cada widget e configura
        self._criar_sidebar()
        self._criar_meio()
        self._criar_header()
        self._criar_tabela()
        self._criar_barra_de_progresso()
        self._criar_rodape()
        
    def _criar_sidebar(self):
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)

    def _criar_meio(self):
        self.meio = ctk.CTkFrame(
            self, 
            width=500, 
            height=400, 
            fg_color=COLORS.center_background,
            corner_radius=10)

        self.meio.pack(side=ctk.LEFT, fill=ctk.Y)
        self.meio.pack_propagate(False)

    def _criar_header(self):
        self.header = Header(self.meio, on_load_file=self._handle_file_uploaded, on_export=lambda: ask_save_directory(self))
        self.header.pack(fill=ctk.X, padx=10, pady=8)
        self.header.pack_propagate(False)

    def _criar_tabela(self):
        self.tabela = DataTable(self.meio)
        self.tabela.pack(padx=5, pady=5)

    def _criar_barra_de_progresso(self):
        self.barra_de_progresso = ProgressBar(self.meio)
        self.barra_de_progresso.pack(padx=5, pady=5)

    def _criar_rodape(self):
        self.baseboard = Baseboard(self.meio, on_process=self._run_process_thread, on_cancel=self._handle_cancel)
        self.baseboard.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.baseboard.pack_propagate(False)

##Função da Interface abaixo
    def _run_sanitize_thread(self):
        file_path = ask_excel_file(self)
        if file_path is None:
            return None
        try:
            dataframe_sanitized = SanitizeController(file_path)
            dataframe_sanitized.start()
            dataframe_sanitized.join()

            if dataframe_sanitized.error is not None:
                raise dataframe_sanitized.error
            
            return dataframe_sanitized.result
        except Exception as e:
            raise e

    def _handle_file_uploaded(self):
        dataframe = self._run_sanitize_thread()
        if dataframe is None:
            return
        self.tabela.update_data(dataframe)

    def _run_process_thread(self):
        """
        Função para executar o thread de processamento e criar a nova thread
        """
        thread = self.process_controller
        thread.start()

    def _handle_cancel(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()