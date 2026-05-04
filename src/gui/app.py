import customtkinter as ctk
from src.controller.sanitize_controller import SanitizeController
from src.controller.process_controller import ProcessController
from src.gui.components import DataTable
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
        self._criar_tabela()
        #self._criar_barra_de_progresso()
        self._criar_rodape()
        
    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=100, fg_color=COLORS.sidebar_background)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        self.sidebar._border_color = COLORS.sidebar_border
        self.sidebar._border_width = 1
        self.sidebar.pack_propagate(False)

    def _criar_meio(self):
        self.meio = ctk.CTkFrame(
            self, 
            width=500, 
            height=400, 
            fg_color=COLORS.center_background,
            corner_radius=10)

        self.frame_botoes = ctk.CTkFrame(self.meio, fg_color=COLORS.frame_transparent)
        self.frame_botoes.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=8)

        self.meio.pack(side=ctk.LEFT, fill=ctk.Y)
        self.meio.pack_propagate(False)

        #Cria botão de carregar arquivo
        self.btn_carregar_arquivo = ctk.CTkButton(
            self.frame_botoes, 
            text="Carregar Arquivo",
            fg_color=COLORS.button_background,
            hover_color=COLORS.button_hover,
            text_color=COLORS.button_text,
            border_width=1,
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight))

        #Cria botão de caminho de salvar
        self.btn_caminho_salvar = ctk.CTkButton(
            self.frame_botoes, 
            text="Exportar para",
            fg_color=COLORS.button_background,
            hover_color=COLORS.button_hover,
            text_color=COLORS.button_text,
            border_width=1,
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight))

        self.btn_carregar_arquivo.pack(side=ctk.LEFT, padx=(0, 5))
        self.btn_caminho_salvar.pack(side=ctk.LEFT, padx=(20, 0))

        self.btn_carregar_arquivo.configure(command=self._handle_file_uploaded)
        self.btn_caminho_salvar.configure(command=lambda: ask_save_directory(self))

    def _criar_tabela(self):
        self.tabela = DataTable(self.meio)
        self.tabela.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

    def _criar_rodape(self):
        self.rodape = ctk.CTkFrame(
            self.meio, height=50, 
            width=500 ,fg_color=COLORS.footer_background, 
            corner_radius=0)
        self.rodape.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.rodape.pack_propagate(False)

        self.frame_botoes_rodape = ctk.CTkFrame(self.rodape, fg_color=COLORS.frame_transparent)
        self.frame_botoes_rodape.propagate(False)
        self.frame_botoes_rodape.pack(fill=ctk.X, padx=10, pady=8)
        

        self.btn_gerar_relatorio = ctk.CTkButton(
            self.frame_botoes_rodape, 
            text="Gerar", 
            fg_color=COLORS.button_background, 
            hover_color=COLORS.button_hover, 
            text_color=COLORS.button_text, 
            border_width=1, 
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight)
            )

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes_rodape, 
            text="Cancelar", 
            fg_color=COLORS.button_background, 
            hover_color=COLORS.button_hover, 
            text_color=COLORS.button_text, 
            border_width=1,
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight))

        self.btn_gerar_relatorio.pack(side=ctk.RIGHT, padx=(0, 10))
        self.btn_cancelar.pack(side=ctk.LEFT, padx=(10, 0))

        self.btn_gerar_relatorio.configure(command=self._run_process_thread)

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

if __name__ == "__main__":
    app = App()
    app.mainloop()