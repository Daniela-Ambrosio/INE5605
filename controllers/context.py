class RegraNegocioException(Exception):
    pass

class Context:
    def __init__(self):
        self.__clinicas      = []
        self.__pacientes     = []
        self.__profissionais = []
        self.__atendimentos  = []

    @property
    def clinicas(self):
        return self.__clinicas
    
    @property
    def pacientes(self):
        return self.__pacientes
    
    @property
    def profissionais(self):
        return self.__profissionais
    
    @property
    def atendimentos(self):
        return self.__atendimentos