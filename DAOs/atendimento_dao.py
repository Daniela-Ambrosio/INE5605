from DAOs.dao import DAO
from models.atendimento import Atendimento

class AtendimentoDAO(DAO):
    def __init__(self):
            super().__init__("atendimento.pkl")
    
    def add(self, atendimento: Atendimento):
        if (
            (atendimento is not None)
            and isinstance(atendimento, Atendimento)
            and isinstance(atendimento.codigo, int)
        ):
            super().add(atendimento.codigo, atendimento)

    def update(self, atendimento: Atendimento):
        if (
            (atendimento is not None)
            and isinstance(atendimento, Atendimento)
            and isinstance(atendimento.codigo, int)
        ):
            super().update(atendimento.codigo, atendimento)

    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo)

    def remove(self, codigo: int):
        if isinstance(codigo, int):
            return super().remove(codigo)