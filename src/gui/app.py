import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._configurar_tela()
        self._configurar_widgets()

    def _configurar_tela(self):
        self.title("Python Pandas Analyzer")
        self.geometry("500x400")
        self.configure(fg_color="#212121")
        self.resizable(False, False)
    
    def _configurar_widgets(self):
        #Chama cada widget e configura
        self._criar_sidebar()
        self._criar_meio()
        self._criar_tabela()
        self._criar_barra_de_progresso()
        self._criar_rodape()
        
    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=100, fg_color="#1d1d1c")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        self.sidebar._border_color = "#3b3b38"
        self.sidebar._border_width = 1
        self.sidebar.pack_propagate(False)

    def _criar_meio(self):
        self.meio = ctk.CTkFrame(
            self, 
            width=500, 
            height=400, 
            fg_color="#1f1f1e",
            corner_radius=10)

        self.frame_botoes = ctk.CTkFrame(self.meio, fg_color="transparent")
        self.frame_botoes.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=8)

        self.meio.pack(side=ctk.LEFT, fill=ctk.Y)
        self.meio.pack_propagate(False)

        #Cria botão de carregar arquivo
        self.btn_carregar_arquivo = ctk.CTkButton(
            self.frame_botoes, 
            text="Carregar Arquivo",
            fg_color="#383836",
            hover_color="#2e2e2d",
            text_color="#fff",
            border_width=1,
            border_color="#3b3b38",
            font=ctk.CTkFont(family="Monospace", size=12, weight="bold"))

        #Cria botão de caminho de salvar
        self.btn_caminho_salvar = ctk.CTkButton(
            self.frame_botoes, 
            text="Exportar para",
            fg_color="#383836",
            hover_color="#2e2e2d",
            text_color="#fff",
            border_width=1,
            border_color="#3b3b38",
            font=ctk.CTkFont(family="Monospace", size=12, weight="bold"))

        self.btn_carregar_arquivo.pack(side=ctk.LEFT, padx=(0, 5))
        self.btn_caminho_salvar.pack(side=ctk.LEFT, padx=(20, 0))

    def _criar_tabela(self):
        self.tabela = ctk.CTkFrame(
            self.meio, 
            width = 360, 
            height = 250, 
            fg_color="#2c2c2a")

        self.tabela.pack_propagate(False)
        self.tabela.pack(expand=True)
        self.tabela._border_color = "#313130"
        self.tabela._border_width = 1

    def _criar_barra_de_progresso(self):
        self.frame_barra_de_progresso = ctk.CTkFrame(
           self.meio,
           width = 350,
           height = 20,
           fg_color="transparent")
        self.frame_barra_de_progresso.pack_propagate(False)
        self.frame_barra_de_progresso.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=8)

    def _criar_rodape(self):
        self.rodape = ctk.CTkFrame(
            self.meio, height=50, 
            width=500 ,fg_color="#2e2e2d", 
            corner_radius=0)
            
        self.rodape.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.rodape.pack_propagate(False)

        self.frame_botoes_rodape = ctk.CTkFrame(self.rodape, fg_color="transparent")
        self.frame_botoes_rodape.propagate(False)
        self.frame_botoes_rodape.pack(fill=ctk.X, padx=10, pady=8)
        

        self.btn_gerar_relatorio = ctk.CTkButton(
            self.frame_botoes_rodape, 
            text="Gerar", 
            fg_color="#383836", 
            hover_color="#2e2e2d", 
            text_color="#fff", 
            border_width=1, 
            border_color="#3b3b38",
            font=ctk.CTkFont(family="Monospace", size=12, weight="bold")
            )

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes_rodape, 
            text="Cancelar", 
            fg_color="#383836", 
            hover_color="#2e2e2d", 
            text_color="#fff", 
            border_width=1, 
            border_color="#3b3b38",
            font=ctk.CTkFont(family="Monospace", size=12, weight="bold"))

        self.btn_gerar_relatorio.pack(side=ctk.RIGHT, padx=(0, 10))
        self.btn_cancelar.pack(side=ctk.LEFT, padx=(10, 0))


if __name__ == "__main__":
    app = App()
    app.mainloop()