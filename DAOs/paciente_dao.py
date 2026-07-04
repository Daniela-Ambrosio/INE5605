from DAOs.dao import DAO
from models.pessoa import Paciente

class PacienteDAO(DAO):
    def __init__(self):
            super().__init__("paciente.pkl")
    
    def add(self, paciente: Paciente):
        if (
            (paciente is not None)
            and isinstance(paciente, Paciente)
            and isinstance(paciente.cpf, str)
        ):
            super().add(paciente.cpf, paciente)

    def update(self, paciente: Paciente):
        if (
            (paciente is not None)
            and isinstance(paciente, Paciente)
            and isinstance(paciente.cpf, str)
        ):
            super().update(paciente.cpf, paciente)

    def get(self, cpf: str):
        if isinstance(cpf, str):
            return super().get(cpf)

    def remove(self, cpf: str):
        if isinstance(cpf, str):
            return super().remove(cpf)