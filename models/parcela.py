from datetime import date
from .exceptions import TipoInvalidoException

class Parcela:
    def __init__(self, numero: int, custo: float, vencimento: date, paga: bool = False):
        self.numero = numero
        self.custo = custo
        self.vencimento = vencimento
        self.paga = paga

    @property
    def numero(self): return self.__numero
    @numero.setter
    def numero(self, numero):
        if not isinstance(numero, int): raise TipoInvalidoException("Número da parcela deve ser inteiro.")
        self.__numero = numero

    @property
    def custo(self): return self.__custo
    @custo.setter
    def custo(self, custo):
        if not isinstance(custo, (int, float)): raise TipoInvalidoException("Custo da parcela deve ser número.")
        self.__custo = float(custo)

    @property
    def vencimento(self): return self.__vencimento
    @vencimento.setter
    def vencimento(self, vencimento):
        if not isinstance(vencimento, date): raise TipoInvalidoException("Vencimento deve ser do tipo date.")
        self.__vencimento = vencimento

    @property
    def paga(self): return self.__paga
    @paga.setter
    def paga(self, paga):
        if not isinstance(paga, bool): raise TipoInvalidoException("Status de paga deve ser booleano.")
        self.__paga = paga
