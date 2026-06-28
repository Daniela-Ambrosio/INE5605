from datetime import date
from enum import Enum

class Especialidade(Enum):
    CLINICO_GERAL = "Clínico Geral"
    PEDIATRIA = "Pediatria"
    CARDIOLOGIA = "Cardiologia"
    DERMATOLOGIA = "Dermatologia"
    ORTOPEDIA = "Ortopedia"
    GINECOLOGIA = "Ginecologia"

class Pessoa:
    def __init__(self, nome: str, telefone: str, cpf: str):
        self.__nome = nome
        self.__telefone = telefone
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

class Paciente(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, data_nascimento: date):
        super().__init__(nome, telefone, cpf)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento

class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int):
        super().__init__(nome, telefone, cpf)
        self.__especialidade = especialidade
        self.__registro = registro

    @property
    def especialidade(self):
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade):
        self.__especialidade = especialidade

    @property
    def registro(self):
        return self.__registro

    @registro.setter
    def registro(self, registro):
        self.__registro = registro
