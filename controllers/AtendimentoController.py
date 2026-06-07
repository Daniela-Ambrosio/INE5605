from datetime import date, time
from models import Clinica, Paciente, ProfissionalSaude, Atendimento, TipoAtendimento, Procedimento
from .Context import Context, RegraNegocioException
from .validacoes import validar_tipo

class AtendimentoController:
    def __init__(self, context: Context):
        self.context = context

    def agendar_atendimento(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, 
                            data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float = 0.0) -> Atendimento:
        # Validação das classes
        validar_tipo(clinica, Clinica)
        validar_tipo(paciente, Paciente)
        validar_tipo(profissional, ProfissionalSaude)
        validar_tipo(tipo, TipoAtendimento)

        # verificação se é de maior
        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18:
            raise RegraNegocioException("Somente pacientes com mais de 18 anos podem realizar atendimentos de forma independente.")

        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("O horário do atendimento está fora do horário de funcionamento da clínica")

        for at in self.context.atendimentos:
            if at.profissional == profissional and at.data == data:
                if not (hora_fim <= at.fim or hora_inicio >= at.inicio):
                    raise RegraNegocioException(
                        f"O profissional {profissional.nome} já possui um atendimento agendado "
                        f"das {at.inicio.strftime('%H:%M')} às {at.fim.strftime('%H:%M')} neste dia."
                    )

        atendimento = Atendimento(clinica, paciente, profissional, data, hora_inicio, hora_fim, tipo, custo)
        self.context.atendimentos.append(atendimento)

        return atendimento

    def alterar_atendimento(self, atendimento: Atendimento, clinica: Clinica, paciente: Paciente, 
                            profissional: ProfissionalSaude, data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float):
        # Validação das classes
        validar_tipo(clinica, Clinica)
        validar_tipo(paciente, Paciente)
        validar_tipo(profissional, ProfissionalSaude)
        validar_tipo(tipo, TipoAtendimento)

        # Verificação da idade e do horário de funcionamento
        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18:
            raise RegraNegocioException("Somente pacientes com mais de 18 anos podem realizar atendimentos de forma independente.")

        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("O horário del atendimento está fora do horário de funcionamento da clínica")

        atendimento.clinica = clinica
        atendimento.paciente = paciente
        atendimento.profissional = profissional
        atendimento.data = data
        atendimento.inicio = hora_inicio
        atendimento.fim = hora_fim
        atendimento.tipo = tipo
        atendimento.custo = custo

    def excluir_atendimento(self, atendimento: Atendimento):
        if atendimento in self.context.atendimentos:
            self.context.atendimentos.remove(atendimento)

    def adicionar_procedimento_a_atendimento(self, atendimento: Atendimento, descricao: str, custo: float, profissional: ProfissionalSaude) -> Procedimento:
        validar_tipo(atendimento, Atendimento)
        validar_tipo(profissional, ProfissionalSaude)
        
        procedimento = Procedimento(descricao, custo, profissional)
        atendimento.adicionar_procedimento(procedimento)
        return procedimento

    def alterar_procedimento(self, atendimento: Atendimento, procedimento: Procedimento, descricao: str, custo: float, profissional: ProfissionalSaude):
        validar_tipo(atendimento, Atendimento)
        validar_tipo(profissional, ProfissionalSaude)

        atendimento.custo -= procedimento.custo
        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.profissional = profissional
        atendimento.custo += custo

    def excluir_procedimento(self, atendimento: Atendimento, procedimento: Procedimento):
        validar_tipo(atendimento, Atendimento)
        if procedimento in atendimento.procedimentos:
            atendimento.custo -= procedimento.custo
            atendimento.procedimentos.remove(procedimento)