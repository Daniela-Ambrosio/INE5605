from views.relatorio_view import RelatorioView
from views.clinica_view import ClinicaView
from views.paciente_view import PacienteView
from views.profissional_view import ProfissionalView

class RelatoriosController:
    def __init__(self, context):
        self.context = context
        self.relatorio_view = RelatorioView()
        self.clinica_view = ClinicaView()
        self.paciente_view = PacienteView()
        self.profissional_view = ProfissionalView()

    def abrir_tela(self):
        while True:
            opcao = self.relatorio_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._relatorio_clinica()
            elif opcao == 2: self._relatorio_paciente()
            elif opcao == 3: self._relatorio_profissional()

    def _formata_atendimento(self, at):
        pago = 'Pago' if at.pagamento else 'Pendente'
        return (f"DATA: {at.data.strftime('%d/%m/%Y')} INÍCIO: {at.inicio.strftime('%H:%M')} FIM: {at.fim.strftime('%H:%M')}\n"
                f"CLÍNICA: {at.clinica.nome} PACIENTE: {at.paciente.nome} PROFISSIONAL: {at.profissional.nome}\n"
                f"TIPO: {at.tipo.value} CUSTO: R$ {at.custo:.2f} STATUS: {pago}\n\n")

    def _relatorio_clinica(self):
        nome = self.clinica_view.seleciona_clinica()
        if not nome: return
        achou = False
        relatorio = f"-------- RELATÓRIO DE ATENDIMENTOS DA CLÍNICA {nome.upper()} --------\n\n"
        for at in self.context.atendimentos:
            if at.clinica.nome == nome:
                relatorio += self._formata_atendimento(at)
                achou = True
        if not achou:
            relatorio = f"Nenhum atendimento encontrado para a clínica {nome}."
        self.relatorio_view.mostra_mensagem(relatorio)

    def _relatorio_paciente(self):
        cpf = self.paciente_view.seleciona_paciente()
        if not cpf: return
        achou = False
        relatorio = f"-------- RELATÓRIO DE ATENDIMENTOS DO PACIENTE {cpf} --------\n\n"
        for at in self.context.atendimentos:
            if at.paciente.cpf == cpf:
                relatorio += self._formata_atendimento(at)
                achou = True
        if not achou:
            relatorio = f"Nenhum atendimento encontrado para o paciente {cpf}."
        self.relatorio_view.mostra_mensagem(relatorio)

    def _relatorio_profissional(self):
        cpf = self.profissional_view.seleciona_profissional()
        if not cpf: return
        achou = False
        relatorio = f"-------- RELATÓRIO DE ATENDIMENTOS DO PROFISSIONAL {cpf} --------\n\n"
        for at in self.context.atendimentos:
            if at.profissional.cpf == cpf:
                relatorio += self._formata_atendimento(at)
                achou = True
        if not achou:
            relatorio = f"Nenhum atendimento encontrado para o profissional {cpf}."
        self.relatorio_view.mostra_mensagem(relatorio)
