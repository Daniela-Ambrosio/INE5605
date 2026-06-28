from datetime import date
from enum import Enum
from .exceptions import TipoInvalidoException, ValorVazioException

class Especialidade(Enum):
    CLINICO_GERAL = "Clínico Geral"
    PEDIATRIA = "Pediatria"
    CARDIOLOGIA = "Cardiologia"
    DERMATOLOGIA = "Dermatologia"
    ORTOPEDIA = "Ortopedia"
    GINECOLOGIA = "Ginecologia"

class Pessoa:
    def __init__(self, nome: str, telefone: str, cpf: str):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if not isinstance(nome, str):
            raise TipoInvalidoException("O nome deve ser um texto.")
        if not nome.strip():
            raise ValorVazioException("O nome não pode ser vazio.")
        self.__nome = nome

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        if not isinstance(telefone, str):
            raise TipoInvalidoException("O telefone deve ser um texto.")
        if not telefone.strip():
            raise ValorVazioException("O telefone não pode ser vazio.")
        self.__telefone = telefone

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if not isinstance(cpf, str):
            raise TipoInvalidoException("O CPF deve ser um texto.")
        if not cpf.strip():
            raise ValorVazioException("O CPF não pode ser vazio.")
        self.__cpf = cpf

class Paciente(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, data_nascimento: date):
        super().__init__(nome, telefone, cpf)
        self.data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        if not isinstance(data_nascimento, date):
            raise TipoInvalidoException("A data de nascimento deve ser do tipo date.")
        self.__data_nascimento = data_nascimento

class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int):
        super().__init__(nome, telefone, cpf)
        self.especialidade = especialidade
        self.registro = registro

    @property
    def especialidade(self):
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade):
        if not isinstance(especialidade, Especialidade):
            raise TipoInvalidoException("A especialidade deve ser do tipo Especialidade (Enum).")
        self.__especialidade = especialidade

    @property
    def registro(self):
        return self.__registro

    @registro.setter
    def registro(self, registro):
        if not isinstance(registro, int):
            raise TipoInvalidoException("O registro deve ser um número inteiro.")
        self.__registro = registro
