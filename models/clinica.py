from datetime import time


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str, hora_abertura: time, hora_fechamento: time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento
    
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def hora_abertura(self):
        return self.__hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura):
        self.__hora_fechamento = hora_abertura

    @property
    def hora_fechamento(self):
        return self.__hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento):
        self.__hora_fechamento = hora_fechamento
