from datetime import date


class Parcela:
    def __init__(self, numero: int, custo: float, vencimento: date, paga: bool = False):
        self._numero = numero
        self._custo = custo
        self._vencimento = vencimento
        self._paga = paga

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def custo(self):
        return self._custo

    @custo.setter
    def custo(self, custo):
        self._custo = custo

    @property
    def vencimento(self):
        return self._vencimento

    @vencimento.setter
    def vencimento(self, vencimento):
        self._vencimento = vencimento

    @property
    def paga(self):
        return self._paga

    @paga.setter
    def paga(self, paga):
        self._paga = paga