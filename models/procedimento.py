from .pessoa import ProfissionalSaude
from .exceptions import TipoInvalidoException

class Procedimento:
    _proximo_codigo = 1

    def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude, codigo: int = None):
        self.descricao = descricao
        self.custo = custo
        self.profissional = profissional

        if codigo is None:
            self.codigo = Procedimento._proximo_codigo
            Procedimento._proximo_codigo += 1
        else:
            self.codigo = codigo

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


    @property
    def codigo(self): return self.__codigo
    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, int): raise TipoInvalidoException("Código deve ser do tipo int.")
        self.__codigo = codigo
