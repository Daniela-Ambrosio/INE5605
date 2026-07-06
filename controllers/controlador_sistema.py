from views.menu_view import MenuView
from controllers.clinica_controller import ClinicaController
from controllers.paciente_controller import PacienteController
from controllers.profissional_controller import ProfissionalController
from controllers.atendimento_controller import AtendimentoController
from controllers.procedimento_controller import ProcedimentoController
from controllers.pagamento_controller import PagamentoController
from controllers.relatorios_controller import RelatoriosController

class ControladorSistema:
    def __init__(self):
        self.__menu_view = MenuView()
        self.__clinica_controller = ClinicaController(None)
        self.__paciente_controller = PacienteController(None)
        self.__profissional_controller = ProfissionalController(None)
        self.__atendimento_controller = AtendimentoController(None)
        self.__procedimento_controller = ProcedimentoController()
        self.__pagamento_controller = PagamentoController(None)
        self.__relatorios_controller = RelatoriosController()

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
