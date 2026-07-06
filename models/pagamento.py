from datetime import date
from typing import List
from abc import ABC
from .parcela import Parcela
from .exceptions import TipoInvalidoException, ValorVazioException

class Pagamento(ABC):
    _proximo_codigo = 1

    def __init__(self, data: date, custo: float, parcelado: bool = False, codigo: int = None):
        self.data = data
        self.custo = custo
        self.parcelado = parcelado
        self.__parcelas: List[Parcela] = []

        if codigo is None:
            self.codigo = Pagamento._proximo_codigo
            Pagamento._proximo_codigo += 1
        else:
            self.codigo = codigo
            
    @property
    def data(self): return self.__data
    @data.setter
    def data(self, data):
        if not isinstance(data, date): raise TipoInvalidoException("Data deve ser do tipo date.")
        self.__data = data

    @property
    def custo(self): return self.__custo
    @custo.setter
    def custo(self, custo):
        if not isinstance(custo, (int, float)): raise TipoInvalidoException("Custo deve ser número.")
        self.__custo = float(custo)

    @property
    def parcelado(self): return self.__parcelado
    @parcelado.setter
    def parcelado(self, parcelado: bool):
        if not isinstance(parcelado, bool): raise TipoInvalidoException("Parcelado deve ser booleano.")
        self.__parcelado = parcelado

    @property
    def parcelas(self): return self.__parcelas

    @property
    def codigo(self): return self.__codigo
    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, int): raise TipoInvalidoException("Código deve ser do tipo int.")
        self.__codigo = codigo

    
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
        self.cpf = cpf

    @property
    def cpf(self): return self.__cpf
    @cpf.setter
    def cpf(self, cpf):
        if not isinstance(cpf, str): raise TipoInvalidoException("CPF deve ser texto.")
        if not cpf.strip(): raise ValorVazioException("CPF não pode ser vazio.")
        self.__cpf = cpf


class Dinheiro(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool):
        super().__init__(data, custo, parcelado)


class Cartao(Pagamento):
    def __init__(self, data: date, custo: float, parcelado: bool, numero: int, bandeira: str):
        super().__init__(data, custo, parcelado)
        self.numero = numero
        self.bandeira = bandeira

    @property
    def numero(self): return self.__numero
    @numero.setter
    def numero(self, numero):
        if not isinstance(numero, int): raise TipoInvalidoException("Número do cartão deve ser inteiro.")
        self.__numero = numero

    @property
    def bandeira(self): return self.__bandeira
    @bandeira.setter
    def bandeira(self, bandeira):
        if not isinstance(bandeira, str): raise TipoInvalidoException("Bandeira deve ser texto.")
        if not bandeira.strip(): raise ValorVazioException("Bandeira não pode ser vazia.")
        self.__bandeira = bandeira
