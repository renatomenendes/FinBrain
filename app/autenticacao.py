import hashlib

class Autenticacao:
    """
    Classe para gerenciamento de autenticação de senhas utilizando hash SHA-256.

    Esta classe oferece métodos para gerar o hash de uma senha e verificar se uma senha fornecida
    corresponde ao hash armazenado.
    """

    @staticmethod
    def hash_senha(senha):
        """
        Gera o hash SHA-256 para uma senha fornecida.

        Parâmetros:
        ----------
        senha : str
            A senha em texto plano que será convertida em um hash.

        Retorna:
        --------
        str
            O hash SHA-256 da senha fornecida, no formato hexadecimal.
        """
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def verificar_senha(senha, senha_hash):
        """
        Verifica se o hash da senha fornecida corresponde ao hash armazenado.

        Este método compara o hash da senha em texto plano com o hash armazenado 
        para verificar se a senha é válida.

        Parâmetros:
        ----------
        senha : str
            A senha em texto plano a ser verificada.
        senha_hash : str
            O hash armazenado que será comparado com o hash da senha fornecida.

        Retorna:
        --------
        bool
            Retorna True se o hash da senha fornecida corresponder ao hash armazenado, 
            caso contrário, retorna False.
        """
        return Autenticacao.hash_senha(senha) == senha_hash