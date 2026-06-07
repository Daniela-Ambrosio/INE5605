from datetime import date
from typing import List
from abc import ABC
from .Parcela import Parcela


class Pagamento(ABC):
    def __init__(self, data: date, custo: float, parcelado: bool = False):
        self._data = data
        self._custo = custo
        self._parcelado = parcelado
        self._parcelas: List[Parcela] = []

    @property
    def data(self):
        return self._data
 
    @data.setter
    def data(self, data):
        self._data = data
 
    @property
    def custo(self):
        return self._custo
 
    @custo.setter
    def custo(self, custo):
        self._custo = custo
 
    @property
    def parcelado(self):
        return self._parcelado
 
    @parcelado.setter
    def parcelado(self, parcelado: bool):
        self._parcelado = parcelado
 
    @property
    def parcelas(self):
        return self._parcelas
 
    def adicionar_parcela(self, numero, custo, vencimento, paga=False):
        nova_parcela = Parcela(numero, custo, vencimento, paga)
        self._parcelas.append(nova_parcela)
    
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
        self._cpf = cpf

    @property
    def cpf(self):
        return self._cpf
 
    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

class Dinheiro(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool):
        super().__init__(data, custo, parcelado)

class Cartao(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool, numero: int, bandeira: str):
        super().__init__(data, custo, parcelado)
        self._numero = numero
        self._bandeira = bandeira

    @property
    def numero(self):
        return self._numero
 
    @numero.setter
    def numero(self, numero):
        self._numero = numero
 
    @property
    def bandeira(self):
        return self._bandeira
 
    @bandeira.setter
    def bandeira(self, bandeira):
        self._bandeira = bandeira
