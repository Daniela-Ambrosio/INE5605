from DAOs.dao import DAO
from models.clinica import Clinica

class ClinicaDAO(DAO):
    def __init__(self):
            super().__init__("clinica.pkl")
    
    def add(self, clinica: Clinica):
        if (
            (clinica is not None)
            and isinstance(clinica, Clinica)
            and isinstance(clinica.nome, str)
        ):
            super().add(clinica.nome, clinica)

    def update(self, clinica: Clinica):
        if (
            (clinica is not None)
            and isinstance(clinica, Clinica)
            and isinstance(clinica.nome, str)
        ):
            super().update(clinica.nome, clinica)

    def get(self, nome: str):
        if isinstance(nome, str):
            return super().get(nome)

    def remove(self, nome: str):
        if isinstance(nome, str):
            return super().remove(nome)