from datetime import time


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str, hora_abertura: time, hora_fechamento: time):
        self._nome = nome
        self._cidade = cidade
        self._descricao = descricao
        self._hora_abertura = hora_abertura
        self._hora_fechamento = hora_fechamento
    
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, cidade):
        self._cidade = cidade

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def hora_abertura(self):
        return self._hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura):
        self._hora_fechamento = hora_abertura

    @property
    def hora_fechamento(self):
        return self._hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento):
        self._hora_fechamento = hora_fechamento
