from views.menu_view import MenuView
from controllers.clinica_controller import ClinicaController
from controllers.paciente_controller import PacienteController
from controllers.profissional_controller import ProfissionalController
from controllers.atendimento_controller import AtendimentoController
from controllers.procedimento_controller import ProcedimentoController
from controllers.pagamento_controller import PagamentoController
from controllers.relatorios_controller import RelatoriosController
from controllers.context import Context

class ControladorSistema:
    def __init__(self):
        self.context = Context()
        self.__menu_view = MenuView()
        self.__clinica_controller = ClinicaController(self.context)
        self.__paciente_controller = PacienteController(self.context)
        self.__profissional_controller = ProfissionalController(self.context)
        self.__atendimento_controller = AtendimentoController(self.context)
        self.__procedimento_controller = ProcedimentoController(self.context)
        self.__pagamento_controller = PagamentoController(self.context)
        self.__relatorios_controller = RelatoriosController(self.context)

    def iniciar(self):
        while True:
            opcao = self.__menu_view.tela_opcoes()
            if opcao == 0:
                break
            elif opcao == 1:
                self.__clinica_controller.abrir_tela()
            elif opcao == 2:
                self.__paciente_controller.abrir_tela_paciente()
            elif opcao == 3:
                self.__profissional_controller.abrir_tela_profissional()
            elif opcao == 4:
                self.__atendimento_controller.abrir_tela_atendimento()
            elif opcao == 5:
                self.__procedimento_controller.abrir_tela_procedimento()
            elif opcao == 6:
                self.__pagamento_controller.abrir_tela()
            elif opcao == 7:
                self.__relatorios_controller.abrir_tela()
