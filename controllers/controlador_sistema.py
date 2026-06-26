from views.menu_view import MenuView
from controllers.clinica_controller import ClinicaController
from controllers.pessoa_controller import PessoaController
from controllers.atendimento_controller import AtendimentoController
from controllers.pagamento_controller import PagamentoController
from controllers.relatorios_controller import RelatoriosController
from controllers.context import Context

class ControladorSistema:
    def __init__(self):
        self.context = Context()
        self.menu_view = MenuView()
        self.clinica_controller = ClinicaController(self.context)
        self.pessoa_controller = PessoaController(self.context)
        self.atendimento_controller = AtendimentoController(self.context)
        self.pagamento_controller = PagamentoController(self.context)
        self.relatorios_controller = RelatoriosController(self.context)

    def iniciar(self):
        while True:
            botao, valores = self.menu_view.open()
            if botao in (None, 'Sair'):
                break
            elif botao == 'Clínicas':
                self.clinica_controller.abrir_tela()
            elif botao == 'Pacientes':
                self.pessoa_controller.abrir_tela_paciente()
            elif botao == 'Profissionais':
                self.pessoa_controller.abrir_tela_profissional()
            elif botao == 'Atendimentos':
                self.atendimento_controller.abrir_tela_atendimento()
            elif botao == 'Procedimentos':
                self.atendimento_controller.abrir_tela_procedimento()
            elif botao == 'Pagamentos':
                self.pagamento_controller.abrir_tela()
            elif botao == 'Relatórios':
                self.relatorios_controller.abrir_tela()
