from datetime import date, datetime, time
from enum import Enum
from typing import List
from .clinica import Clinica
from .pessoa import Paciente, ProfissionalSaude
from .procedimento import Procedimento
from .pagamento import Pagamento

class TipoAtendimento(Enum):
    CONSULTA = "Consulta"
    RETORNO = "Retorno"
    EXAME = "Exame"
    PROCEDIMENTO = "Procedimento"

class Atendimento:
    def __init__(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, data: date, inicio: time,
            fim: time, tipo: TipoAtendimento, custo: float):
            self.___clinica = clinica
            self.___paciente = paciente
            self.__profissional = profissional
            self.__data = data
            self.__inicio = inicio  #2025, 5, 19, 9, 0) -> 19/05/2025 às 09:00
            self.__fim = fim
            self.__tipo = tipo
            self.__procedimentos: List[Procedimento] = []
            self.__custo = custo

        #só existem se for instanciada uma classe Pagamento:
            self.__pagamento = None
            self.__parcelado = bool = False
            
        
    @property
    def clinica(self):
        return self.___clinica
 
    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.___clinica = clinica
 
    @property
    def paciente(self):
        return self.___paciente
 
    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.___paciente = paciente
 
    @property
    def profissional(self):
        return self.__profissional
 
    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = profissional
    
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def inicio(self):
        return self.__inicio
 
    @inicio.setter
    def inicio(self, inicio: datetime):
        self.__inicio = inicio
 
    @property
    def fim(self):
        return self.__fim
 
    @fim.setter
    def fim(self, fim: datetime):
        self.__fim = fim
 
    @property
    def tipo(self):
        return self.__tipo
 
    @tipo.setter
    def tipo(self, tipo: TipoAtendimento):
        self.__tipo = tipo
 
    @property
    def procedimentos(self):
        return self.__procedimentos
 
    #agregação recebe o objeto já instanciado
    def adicionar_procedimento(self, procedimento: Procedimento):
        self.__procedimentos.append(procedimento)
        self.__custo += procedimento.custo
 
    @property
    def custo(self):
        return self.__custo
 
    @custo.setter
    def custo(self, custo):
        self.__custo = custo
 
    @property
    def pagamento(self):
        return self.__pagamento

    @pagamento.setter
    def pagamento(self, pagamento):
        self.__pagamento = pagamento

    @property
    def parcelado(self):
        return self.__parcelado

    @parcelado.setter
    def parcelado(self, parcelado: bool):
        self.__parcelado = parcelado

    # Agregação
    def registrar_pagamento(self, pagamento: Pagamento):
        self.__pagamento = pagamento
        self.__parcelado = pagamento.parcelado
