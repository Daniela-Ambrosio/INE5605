from DAOs.dao import DAO
from models.pessoa import ProfissionalSaude

class ProfissionalDAO(DAO):
    def __init__(self):
            super().__init__("profissional.pkl")
    
    def add(self, profissional: ProfissionalSaude):
        if (
            (profissional is not None)
            and isinstance(profissional, ProfissionalSaude)
            and isinstance(profissional.cpf, str)
        ):
            super().add(profissional.cpf, profissional)

    def update(self, profissional: ProfissionalSaude):
        if (
            (profissional is not None)
            and isinstance(profissional, ProfissionalSaude)
            and isinstance(profissional.cpf, str)
        ):
            super().update(profissional.cpf, profissional)

    def get(self, cpf: str):
        if isinstance(cpf, str):
            return super().get(cpf)

    def remove(self, cpf: str):
        if isinstance(cpf, str):
            return super().remove(cpf)