import logging

class Auditoria:
    """
    Classe para registrar eventos de auditoria em um arquivo de log.

    Esta classe configura um sistema de auditoria para registrar mensagens em 
    diferentes níveis de severidade (info, warning, error). O arquivo de log pode 
    ser especificado durante a inicialização.

    Attributes:
        arquivo_log (str): Caminho para o arquivo onde os logs serão armazenados.
    """
    
    def __init__(self, arquivo_log='auditoria.log'):
        """
        Inicializa o sistema de auditoria configurando o arquivo de log.

        Parâmetros:
        ---------------
        arquivo_log : str, opcional
            O caminho e o nome do arquivo de log. O padrão é 'auditoria.log'.
        """
        logging.basicConfig(
            filename=arquivo_log,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def registrar_evento(self, mensagem, nivel="info"):
        """
        Registra um evento no log com o nível de severidade especificado.

        Parâmetros:
        ---------------
        mensagem : str
            A mensagem a ser registrada no log.
        nivel : str, opcional
            O nível de severidade do log. Pode ser "info", "warning", ou "error".
            O padrão é "info".

        Exceções:
        ---------------
        Se o nível fornecido não for "info", "warning" ou "error", a mensagem será 
        registrada como "info" por padrão.
        """
        if nivel == "info":
            logging.info(mensagem)
        elif nivel == "warning":
            logging.warning(mensagem)
        elif nivel == "error":
            logging.error(mensagem)
        else:
            logging.info(mensagem)
