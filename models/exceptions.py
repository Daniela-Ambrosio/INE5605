class TipoInvalidoException(Exception):
    def __init__(self, mensagem):
        super().__init__(mensagem)

class ValorVazioException(Exception):
    def __init__(self, mensagem):
        super().__init__(mensagem)
