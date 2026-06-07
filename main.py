from controllers.Context import Context
from controllers.AtendimentoController import AtendimentoController
from controllers.ClinicaController import ClinicaController
from controllers.PessoaController import PessoaController
from controllers.PagamentoController import PagamentoController
from controllers.RelatoriosController import RelatoriosController

from views.MenuView import MenuView
from views.ClinicaView import ClinicaView
from views.PacienteView import PacienteView
from views.ProfissionalView import ProfissionalView
from views.AtendimentoView import AtendimentoView
from views.ProcedimentoView import ProcedimentoView
from views.PagamentoView import PagamentoView
from views.RelatorioView import RelatorioView

if __name__ == "__main__":
    context = Context()
    
    c_controller = ClinicaController(context)
    clinica_view = ClinicaView(c_controller)

    pessoa_controller = PessoaController(context)
    paciente_view = PacienteView(pessoa_controller)
    profissional_view = ProfissionalView(pessoa_controller)

    a_controller = AtendimentoController(context)
    atendimento_view = AtendimentoView(a_controller, context)

    procedimento_view = ProcedimentoView(a_controller, context)

    pag_controller = PagamentoController(context)
    pagamento_view = PagamentoView(pag_controller, context)
    
    r_controller = RelatoriosController(context)
    relatorio_view = RelatorioView(r_controller)

    app = MenuView(context, clinica_view, paciente_view, profissional_view, atendimento_view, procedimento_view, pagamento_view, relatorio_view)
    app.exibir_menu_principal()
