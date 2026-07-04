from datetime import date, time
from typing import List
from enum import Enum
from .clinica import Clinica
from .pessoa import Paciente, ProfissionalSaude
from .procedimento import Procedimento
from .pagamento import Pagamento
from .exceptions import TipoInvalidoException

class TipoAtendimento(Enum):
    CONSULTA = "Consulta"
    RETORNO = "Retorno"
    EXAME = "Exame"
    PROCEDIMENTO = "Procedimento"

class Atendimento:
    _proximo_codigo = 1

    def __init__(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, data: date, inicio: time, fim: time, tipo: TipoAtendimento, custo: float, codigo: int = None):
        #chama as funções setter ao invés de criar a variável e a criação das variáveis acontece nos setters
        
        self.clinica = clinica 
        self.paciente = paciente
        self.profissional = profissional
        self.data = data
        self.inicio = inicio
        self.fim = fim
        self.tipo = tipo
        self.custo = custo
        self.__procedimentos: List[Procedimento] = []
        self.__pagamento = None
        
        if codigo is None:
            self.codigo = Atendimento._proximo_codigo
            Atendimento._proximo_codigo += 1
        else:
            self.codigo = codigo

    @property
    def clinica(self): return self.__clinica
    @clinica.setter
    def clinica(self, clinica): 
        if not isinstance(clinica, Clinica): raise TipoInvalidoException("Clínica inválida.")
        self.__clinica = clinica 

    @property
    def paciente(self): return self.__paciente
    @paciente.setter
    def paciente(self, paciente):
        if not isinstance(paciente, Paciente): raise TipoInvalidoException("Paciente inválido.")
        self.__paciente = paciente

    @property
    def profissional(self): return self.__profissional
    @profissional.setter
    def profissional(self, profissional):
        if not isinstance(profissional, ProfissionalSaude): raise TipoInvalidoException("Profissional inválido.")
        self.__profissional = profissional

    @property
    def data(self): return self.__data
    @data.setter
    def data(self, data):
        if not isinstance(data, date): raise TipoInvalidoException("Data deve ser do tipo date.")
        self.__data = data

    @property
    def inicio(self): return self.__inicio
    @inicio.setter
    def inicio(self, inicio):
        if not isinstance(inicio, time): raise TipoInvalidoException("Hora início deve ser do tipo time.")
        self.__inicio = inicio

    @property
    def fim(self): return self.__fim
    @fim.setter
    def fim(self, fim):
        if not isinstance(fim, time): raise TipoInvalidoException("Hora fim deve ser do tipo time.")
        self.__fim = fim

    @property
    def tipo(self): return self.__tipo
    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo, TipoAtendimento): raise TipoInvalidoException("Tipo deve ser TipoAtendimento.")
        self.__tipo = tipo

    @property
    def custo(self): return self.__custo
    @custo.setter
    def custo(self, custo):
        if not isinstance(custo, (int, float)): raise TipoInvalidoException("Custo deve ser número.")
        self.__custo = float(custo)

    @property
    def procedimentos(self): return self.__procedimentos
    def adicionar_procedimento(self, procedimento: Procedimento):
        if not isinstance(procedimento, Procedimento): raise TipoInvalidoException("Deve ser um Procedimento.")
        self.__procedimentos.append(procedimento)
        self.custo += procedimento.custo

    @property
    def pagamento(self): return self.__pagamento
    @pagamento.setter
    def pagamento(self, pagamento):
        if pagamento is not None and not isinstance(pagamento, Pagamento): raise TipoInvalidoException("Pagamento inválido.")
        self.__pagamento = pagamento

    @property
    def codigo(self): return self.__codigo
    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, int): raise TipoInvalidoException("Código deve ser do tipo int.")
        self.__codigo = codigo
