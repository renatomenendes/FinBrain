import logging

class Auditoria:
    def __init__(self, arquivo_log='auditoria.log'):
        """Inicializa o sistema de auditoria com um arquivo de log."""
        logging.basicConfig(
            filename=arquivo_log,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def registrar_evento(self, mensagem, nivel="info"):
        """Registra um evento no log."""
        if nivel == "info":
            logging.info(mensagem)
        elif nivel == "warning":
            logging.warning(mensagem)
        elif nivel == "error":
            logging.error(mensagem)
        else:
            logging.info(mensagem)
