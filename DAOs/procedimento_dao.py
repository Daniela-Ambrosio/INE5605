from DAOs.dao import DAO
from models.procedimento import Procedimento

class ProcedimentoDAO(DAO):
    def __init__(self):
            super().__init__("procedimento.pkl")
    
    def add(self, procedimento: Procedimento):
        if (
            (procedimento is not None)
            and isinstance(procedimento, Procedimento)
            and isinstance(procedimento.codigo, int)
        ):
            super().add(procedimento.codigo, procedimento)

    def update(self, procedimento: Procedimento):
        if (
            (procedimento is not None)
            and isinstance(procedimento, Procedimento)
            and isinstance(procedimento.codigo, int)
        ):
            super().update(procedimento.codigo, procedimento)

    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo)

    def remove(self, codigo: int):
        if isinstance(codigo, int):
            return super().remove(codigo)