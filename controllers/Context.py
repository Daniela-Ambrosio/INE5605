class RegraNegocioException(Exception):
    pass

class Context:
    def __init__(self):
        self.clinicas      = []
        self.pacientes     = []
        self.profissionais = []
        self.atendimentos  = []