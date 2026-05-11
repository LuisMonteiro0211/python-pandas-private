"""Controller para processamento de planilhas em thread separada."""

from src.models.processcontext import ProcessContext
from src.services.process_spreadsheet import process_spreadsheet
import threading
import logging

logger = logging.getLogger(__name__)


class ProcessController(threading.Thread):
    """Thread que executa o processamento e exportação de relatórios.
    
    Executa em background para não bloquear a interface gráfica.
    Qualquer erro durante o processamento é capturado e armazenado
    no contexto para posterior verificação pela GUI.
    
    Attributes:
        process_context: Contexto com DataFrame, diretório, evento de cancelamento
            e, opcionalmente, ``on_progress`` para reportar exportações concluídas.
    """
    
    def __init__(self, process_context: ProcessContext):
        """Inicializa o controller com o contexto de processamento.
        
        Args:
            process_context: Contexto contendo todos os dados necessários
                para o processamento (DataFrame, diretório, callbacks).
        """
        super().__init__()
        self.process_context = process_context

    def run(self) -> None:
        """Executa o processamento em thread separada.
        
        Chama o serviço de processamento e captura qualquer exceção,
        armazenando-a no contexto para verificação posterior.
        """
        try:
            process_spreadsheet(self.process_context)
            logger.info("Processamento concluído")
        except Exception as e:
            self.process_context.error = e
            logger.exception("Erro ao processar a planilha")
            return