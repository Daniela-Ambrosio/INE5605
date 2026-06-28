from .pessoa import ProfissionalSaude

class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude):
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional = profissional

    
    @property
    def descricao(self):
        return self.__descricao
 
    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao
 
    @property
    def custo(self):
        return self.__custo
 
    @custo.setter
    def custo(self, custo):
        self.__custo = custo
 
    @property
    def profissional(self):
        return self.__profissional
 
    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = profissional