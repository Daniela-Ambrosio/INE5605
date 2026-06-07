from datetime import date, datetime
from enum import Enum
from typing import List
from .Clinica import Clinica
from .Pessoa import Paciente, ProfissionalSaude
from .Procedimento import Procedimento
from .Pagamento import Pagamento

class TipoAtendimento(Enum):
    CONSULTA = "Consulta"
    RETORNO = "Retorno"
    EXAME = "Exame"
    PROCEDIMENTO = "Procedimento"

class Atendimento:
    def __init__(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, data: date, inicio: datetime,
            fim: datetime, tipo: TipoAtendimento, custo: float):
            self._clinica = clinica
            self._paciente = paciente
            self._profissional = profissional
            self._data = data
            self._inicio = inicio  #2025, 5, 19, 9, 0) -> 19/05/2025 às 09:00
            self._fim = fim
            self._tipo = tipo
            self._procedimentos: List[Procedimento] = []
            self._custo = custo

        #só existem se for instanciada uma classe Pagamento:
            self._pagamento = None
            self._parcelado = bool = False
            
        
    @property
    def clinica(self):
        return self._clinica
 
    @clinica.setter
    def clinica(self, clinica: Clinica):
        self._clinica = clinica
 
    @property
    def paciente(self):
        return self._paciente
 
    @paciente.setter
    def paciente(self, paciente: Paciente):
        self._paciente = paciente
 
    @property
    def profissional(self):
        return self._profissional
 
    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self._profissional = profissional
    
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: date):
        self._data = data

    @property
    def inicio(self):
        return self._inicio
 
    @inicio.setter
    def inicio(self, inicio: datetime):
        self._inicio = inicio
 
    @property
    def fim(self):
        return self._fim
 
    @fim.setter
    def fim(self, fim: datetime):
        self._fim = fim
 
    @property
    def tipo(self):
        return self._tipo
 
    @tipo.setter
    def tipo(self, tipo: TipoAtendimento):
        self._tipo = tipo
 
    @property
    def procedimentos(self):
        return self._procedimentos
 
    #agregação pode receber o objeto já instanciado
    def adicionar_procedimento(self, procedimento: Procedimento):
        self._procedimentos.append(procedimento)
        self._custo += procedimento.custo
 
    @property
    def custo(self):
        return self._custo
 
    @custo.setter
    def custo(self, custo):
        self._custo = custo
 
    @property
    def pagamento(self):
        return self._pagamento
 
    # Agregação
    def registrar_pagamento(self, pagamento: Pagamento):
        self._pagamento = pagamento
        self._parcelado = pagamento.parcelado
