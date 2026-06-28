from datetime import date
from typing import List
from abc import ABC
from .parcela import Parcela


class Pagamento(ABC):
    def __init__(self, data: date, custo: float, parcelado: bool = False):
        self.__data = data
        self.__custo = custo
        self.__parcelado = parcelado
        self.__parcelas: List[Parcela] = []

    @property
    def data(self):
        return self.__data
 
    @data.setter
    def data(self, data):
        self.__data = data
 
    @property
    def custo(self):
        return self.__custo
 
    @custo.setter
    def custo(self, custo):
        self.__custo = custo
 
    @property
    def parcelado(self):
        return self.__parcelado
 
    @parcelado.setter
    def parcelado(self, parcelado: bool):
        self.__parcelado = parcelado
 
    @property
    def parcelas(self):
        return self.__parcelas
 
    def adicionar_parcela(self, numero, custo, vencimento, paga=False):
        nova_parcela = Parcela(numero, custo, vencimento, paga)
        self.__parcelas.append(nova_parcela)
    
    def obter_valor_pago(self):
        if not self.parcelado:
            return self.custo
        else:
            return sum(parcela.custo for parcela in self.parcelas if parcela.paga)

    def obter_valor_restante(self):
        return self.custo - self.obter_valor_pago()

class PIX(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool, cpf: str):
        super().__init__(data, custo, parcelado)
        self.__cpf = cpf

    @property
    def cpf(self):
        return self.__cpf
 
    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

class Dinheiro(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool):
        super().__init__(data, custo, parcelado)

class Cartao(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool, numero: int, bandeira: str):
        super().__init__(data, custo, parcelado)
        self.__numero = numero
        self.__bandeira = bandeira

    @property
    def numero(self):
        return self.__numero
 
    @numero.setter
    def numero(self, numero):
        self.__numero = numero
 
    @property
    def bandeira(self):
        return self.__bandeira
 
    @bandeira.setter
    def bandeira(self, bandeira):
        self.__bandeira = bandeira
