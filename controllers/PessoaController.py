from datetime import date
from models import Paciente, ProfissionalSaude, Especialidade
from .Context import Context, RegraNegocioException
from .validacoes import validar_obrigatorios, validar_tipo

class PessoaController:
    def __init__(self, context: Context):
        self.context = context

    # Paciente
    def cadastrar_paciente(self, nome: str, telefone: str, cpf: str, data_nascimento: date) -> Paciente:
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        
        if any(p.cpf == cpf for p in self.context.pacientes):
            raise RegraNegocioException(f"Já existe um paciente cadastrado com o CPF {cpf}.")
        
        paciente = Paciente(nome, telefone, cpf, data_nascimento)
        self.context.pacientes.append(paciente)
        return paciente

    def alterar_paciente(self, paciente: Paciente, nome: str, telefone: str, cpf: str, data_nascimento: date):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        
        if any(p.cpf == cpf and p != paciente for p in self.context.pacientes):
            raise RegraNegocioException(f"Já existe outro paciente cadastrado com o CPF {cpf}.")
            
        paciente.nome = nome
        paciente.telefone = telefone
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento

    def excluir_paciente(self, paciente: Paciente):
        if any(at.paciente == paciente for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir este paciente pois ele possui atendimentos agendados.")
        if paciente in self.context.pacientes:
            self.context.pacientes.remove(paciente)

    # Profissional de Saúde
    def cadastrar_profissional(self, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int) -> ProfissionalSaude:
        validar_tipo(especialidade, Especialidade)
        validar_obrigatorios({"Nome": nome, "Registro CRM": registro})
        
        if any(p.registro == registro for p in self.context.profissionais):
            raise RegraNegocioException(f"Já existe um profissional cadastrado com o registro {registro}.")

        profissional = ProfissionalSaude(nome, telefone, cpf, especialidade, registro)
        self.context.profissionais.append(profissional)
        return profissional

    def alterar_profissional(self, profissional: ProfissionalSaude, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int):
        validar_tipo(especialidade, Especialidade)
        validar_obrigatorios({"Nome": nome, "Registro CRM": registro})
        
        if any(p.registro == registro and p != profissional for p in self.context.profissionais):
            raise RegraNegocioException(f"Já existe outro profissional cadastrado com o registro {registro}.")

        profissional.nome = nome
        profissional.telefone = telefone
        profissional.cpf = cpf
        profissional.especialidade = especialidade
        profissional.registro = registro

    def excluir_profissional(self, profissional: ProfissionalSaude):
        if any(at.profissional == profissional for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir este profissional pois ele possui atendimentos vinculados.")
            
        if profissional in self.context.profissionais:
            self.context.profissionais.remove(profissional)
