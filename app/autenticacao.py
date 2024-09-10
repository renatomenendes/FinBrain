import hashlib

class Autenticacao:
    @staticmethod
    def hash_senha(senha):
        """Gera o hash da senha."""
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def verificar_senha(senha, senha_hash):
        """Verifica se o hash da senha fornecida corresponde ao hash armazenado."""
        return Autenticacao.hash_senha(senha) == senha_hash

