import os

replacements = [
    # DAO imports -> Context import
    ('from dao import ClinicaDAO, AtendimentoDAO', 'from .context import Context'),
    ('from dao import PacienteDAO, ProfissionalDAO', 'from .context import Context'),
    ('from dao import AtendimentoDAO, ClinicaDAO, PacienteDAO, ProfissionalDAO', 'from .context import Context'),
    ('from dao import AtendimentoDAO', 'from .context import Context'),
    
    # Remove specific DAO initializations
    ('        self.clinica_dao = ClinicaDAO()\n', ''),
    ('        self.atendimento_dao = AtendimentoDAO()\n', ''),
    ('        self.paciente_dao = PacienteDAO()\n', ''),
    ('        self.profissional_dao = ProfissionalDAO()\n', ''),

    # Controller __init__ signature updates
    ('def __init__(self):', 'def __init__(self, context):'),
    ('        self.clinica_view = ClinicaView()', '        self.context = context\n        self.clinica_view = ClinicaView()'),
    ('        self.paciente_view = PacienteView()', '        self.context = context\n        self.paciente_view = PacienteView()'),
    ('        self.atendimento_view = AtendimentoView()', '        self.context = context\n        self.atendimento_view = AtendimentoView()'),
    ('        self.pagamento_view = PagamentoView()', '        self.context = context\n        self.pagamento_view = PagamentoView()'),
    ('        self.relatorio_view = RelatorioView()', '        self.context = context\n        self.relatorio_view = RelatorioView()'),

    # get_all()
    ('self.clinica_dao.get_all()', 'self.context.clinicas'),
    ('self.paciente_dao.get_all()', 'self.context.pacientes'),
    ('self.profissional_dao.get_all()', 'self.context.profissionais'),
    ('self.atendimento_dao.get_all()', 'self.context.atendimentos'),

    # add()
    ('self.clinica_dao.add(clinica)', 'if clinica not in self.context.clinicas: self.context.clinicas.append(clinica)'),
    ('self.paciente_dao.add(paciente)', 'if paciente not in self.context.pacientes: self.context.pacientes.append(paciente)'),
    ('self.profissional_dao.add(profissional)', 'if profissional not in self.context.profissionais: self.context.profissionais.append(profissional)'),
    ('self.atendimento_dao.add(atendimento)', 'if atendimento not in self.context.atendimentos: self.context.atendimentos.append(atendimento)'),

    # remove()
    ('self.clinica_dao.remove(clinica)', 'if clinica in self.context.clinicas: self.context.clinicas.remove(clinica)'),
    ('self.paciente_dao.remove(paciente)', 'if paciente in self.context.pacientes: self.context.pacientes.remove(paciente)'),
    ('self.profissional_dao.remove(profissional)', 'if profissional in self.context.profissionais: self.context.profissionais.remove(profissional)'),
    ('self.atendimento_dao.remove(at)', 'if at in self.context.atendimentos: self.context.atendimentos.remove(at)'),
    ('self.atendimento_dao.remove(atendimento)', 'if atendimento in self.context.atendimentos: self.context.atendimentos.remove(atendimento)'),

    # specific updates
    ('self.atendimento_dao.update(atendimento)', ''),
    ('self.atendimento_dao.update(at)', '')
]

for f in os.listdir('controllers'):
    if f.endswith('_controller.py') and f != 'controlador_sistema.py':
        path = os.path.join('controllers', f)
        with open(path, 'r') as file:
            content = file.read()
        
        for old_str, new_str in replacements:
            content = content.replace(old_str, new_str)
            
        with open(path, 'w') as file:
            file.write(content)
print("Controllers updated.")
