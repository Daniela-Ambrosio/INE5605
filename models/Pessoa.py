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
        self._nome = nome
        self._telefone = telefone
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, telefone):
        self._telefone = telefone

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

class Paciente(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, data_nascimento: date):
        super().__init__(nome, telefone, cpf)
        self._data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int):
        super().__init__(nome, telefone, cpf)
        self._especialidade = especialidade
        self._registro = registro

    @property
    def especialidade(self):
        return self._especialidade

    @especialidade.setter
    def especialidade(self, especialidade):
        self._especialidade = especialidade

    @property
    def registro(self):
        return self._registro

    @registro.setter
    def registro(self, registro):
        self._registro = registro
