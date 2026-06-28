from .pessoa import ProfissionalSaude
from .exceptions import TipoInvalidoException

class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude):
        self.descricao = descricao
        self.custo = custo
        self.profissional = profissional

    @property
    def descricao(self):
        return self.__descricao
        
    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TipoInvalidoException("A descrição do procedimento deve ser texto.")
        self.__descricao = descricao

    @property
    def custo(self):
        return self.__custo
        
    @custo.setter
    def custo(self, custo):
        if not isinstance(custo, (int, float)):
            raise TipoInvalidoException("O custo deve ser um número.")
        self.__custo = float(custo)

    @property
    def profissional(self):
        return self.__profissional
        
    @profissional.setter
    def profissional(self, profissional):
        if not isinstance(profissional, ProfissionalSaude):
            raise TipoInvalidoException("O profissional do procedimento deve ser da classe ProfissionalSaude.")
        self.__profissional = profissional
