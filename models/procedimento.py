from .pessoa import ProfissionalSaude

class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude):
        self._descricao = descricao
        self._custo = custo
        self._profissional = profissional

    
    @property
    def descricao(self):
        return self._descricao
 
    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao
 
    @property
    def custo(self):
        return self._custo
 
    @custo.setter
    def custo(self, custo):
        self._custo = custo
 
    @property
    def profissional(self):
        return self._profissional
 
    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self._profissional = profissional