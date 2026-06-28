from datetime import time
from .exceptions import TipoInvalidoException, ValorVazioException

class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str, hora_abertura: time, hora_fechamento: time):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao
        self.hora_abertura = hora_abertura
        self.hora_fechamento = hora_fechamento
    
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if not isinstance(nome, str):
            raise TipoInvalidoException("O nome da clínica deve ser um texto.")
        if not nome.strip():
            raise ValorVazioException("O nome da clínica não pode ser vazio.")
        self.__nome = nome

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        if not isinstance(cidade, str):
            raise TipoInvalidoException("A cidade deve ser um texto.")
        if not cidade.strip():
            raise ValorVazioException("A cidade não pode ser vazia.")
        self.__cidade = cidade

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TipoInvalidoException("A descrição deve ser um texto.")
        self.__descricao = descricao

    @property
    def hora_abertura(self):
        return self.__hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura):
        if not isinstance(hora_abertura, time):
            raise TipoInvalidoException("A hora de abertura deve ser do tipo time.")
        self.__hora_abertura = hora_abertura

    @property
    def hora_fechamento(self):
        return self.__hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento):
        if not isinstance(hora_fechamento, time):
            raise TipoInvalidoException("A hora de fechamento deve ser do tipo time.")
        self.__hora_fechamento = hora_fechamento
