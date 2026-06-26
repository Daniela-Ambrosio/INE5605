import os
import re

renames = {
    # Models
    'models/Clinica.py': 'models/clinica.py',
    'models/Pessoa.py': 'models/pessoa.py',
    'models/Atendimento.py': 'models/atendimento.py',
    'models/Procedimento.py': 'models/procedimento.py',
    'models/Pagamento.py': 'models/pagamento.py',
    'models/Parcela.py': 'models/parcela.py',

    # Views
    'views/ClinicaView.py': 'views/clinica_view.py',
    'views/PacienteView.py': 'views/paciente_view.py',
    'views/ProfissionalView.py': 'views/profissional_view.py',
    'views/AtendimentoView.py': 'views/atendimento_view.py',
    'views/ProcedimentoView.py': 'views/procedimento_view.py',
    'views/PagamentoView.py': 'views/pagamento_view.py',
    'views/RelatorioView.py': 'views/relatorio_view.py',
    'views/MenuView.py': 'views/menu_view.py',
    'views/ViewBase.py': 'views/view_base.py',

    # Controllers
    'controllers/ClinicaController.py': 'controllers/clinica_controller.py',
    'controllers/PessoaController.py': 'controllers/pessoa_controller.py',
    'controllers/AtendimentoController.py': 'controllers/atendimento_controller.py',
    'controllers/PagamentoController.py': 'controllers/pagamento_controller.py',
    'controllers/RelatoriosController.py': 'controllers/relatorios_controller.py',
    'controllers/ControladorMenu.py': 'controllers/controlador_sistema.py',
    'controllers/Context.py': 'controllers/context.py'
}

# Perform renames
for old, new in renames.items():
    if os.path.exists(old):
        os.rename(old, new)

# Update imports inside all python files
import_replacements = [
    # Models
    ('models.Clinica', 'models.clinica'),
    ('from models.Clinica', 'from models.clinica'),
    ('models.Pessoa', 'models.pessoa'),
    ('from models.Pessoa', 'from models.pessoa'),
    ('models.Atendimento', 'models.atendimento'),
    ('from models.Atendimento', 'from models.atendimento'),
    ('models.Procedimento', 'models.procedimento'),
    ('from models.Procedimento', 'from models.procedimento'),
    ('models.Pagamento', 'models.pagamento'),
    ('from models.Pagamento', 'from models.pagamento'),
    ('models.Parcela', 'models.parcela'),
    ('from models.Parcela', 'from models.parcela'),
    
    # Views
    ('views.ClinicaView', 'views.clinica_view'),
    ('views.PacienteView', 'views.paciente_view'),
    ('views.ProfissionalView', 'views.profissional_view'),
    ('views.AtendimentoView', 'views.atendimento_view'),
    ('views.ProcedimentoView', 'views.procedimento_view'),
    ('views.PagamentoView', 'views.pagamento_view'),
    ('views.RelatorioView', 'views.relatorio_view'),
    ('views.MenuView', 'views.menu_view'),
    ('views.ViewBase', 'views.view_base'),

    # Controllers
    ('controllers.ClinicaController', 'controllers.clinica_controller'),
    ('controllers.PessoaController', 'controllers.pessoa_controller'),
    ('controllers.AtendimentoController', 'controllers.atendimento_controller'),
    ('controllers.PagamentoController', 'controllers.pagamento_controller'),
    ('controllers.RelatoriosController', 'controllers.relatorios_controller'),
    ('controllers.ControladorMenu', 'controllers.controlador_sistema'),
    ('controllers.Context', 'controllers.context'),

    # Specific names
    ('ControladorMenu', 'ControladorSistema'),
    ('.Clinica ', '.clinica '),
    ('.Pessoa ', '.pessoa '),
    ('.Atendimento ', '.atendimento '),
    ('.Procedimento ', '.procedimento '),
    ('.Pagamento ', '.pagamento '),
    ('.Parcela ', '.parcela '),
    ('.Context ', '.context ')
]

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py') and f != 'rename_script.py':
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            new_content = content
            for old_str, new_str in import_replacements:
                new_content = new_content.replace(old_str, new_str)
            
            if new_content != content:
                with open(path, 'w') as file:
                    file.write(new_content)

print("Renaming and import updating complete.")
