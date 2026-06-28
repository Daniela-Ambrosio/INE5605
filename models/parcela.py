from datetime import date


class Parcela:
    def __init__(self, numero: int, custo: float, vencimento: date, paga: bool = False):
        self.__numero = numero
        self.__custo = custo
        self.__vencimento = vencimento
        self.__paga = paga

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    @property
    def custo(self):
        return self.__custo

    @custo.setter
    def custo(self, custo):
        self.__custo = custo

    @property
    def vencimento(self):
        return self.__vencimento

    @vencimento.setter
    def vencimento(self, vencimento):
        self.__vencimento = vencimento

    @property
    def paga(self):
        return self.__paga

    @paga.setter
    def paga(self, paga):
        self.__paga = paga