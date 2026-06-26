from datetime import date, datetime
from models import Paciente, ProfissionalSaude, Especialidade
from .validacoes import validar_obrigatorios, RegraNegocioException
from .context import Context
from views.paciente_view import PacienteView
from views.profissional_view import ProfissionalView

class PessoaController:
    def __init__(self, context):
        self.context = context
        self.paciente_view = PacienteView()
        self.profissional_view = ProfissionalView()

    # ================================================================
    #  PACIENTES - UI
    # ================================================================
    def abrir_tela_paciente(self):
        while True:
            botao, valores = self.paciente_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_pacientes()
            elif botao == 'Cadastrar':
                self._cadastrar_paciente()
            elif botao == 'Alterar':
                self._alterar_paciente()
            elif botao == 'Excluir':
                self._excluir_paciente()

    def _listar_pacientes(self):
        pacientes = self.context.pacientes
        if not pacientes:
            self.paciente_view.mostra_mensagem(
                'Aviso', 'Nenhum paciente cadastrado.')
            return
        dados = []
        for p in pacientes:
            dados.append({
                'nome': p.nome,
                'cpf': p.cpf,
                'telefone': p.telefone,
                'data_nascimento': p.data_nascimento.strftime('%d/%m/%Y')
            })
        self.paciente_view.tela_listagem(dados)

    def _cadastrar_paciente(self):
        botao, vals = self.paciente_view.tela_formulario()
        if botao == 'Confirmar':
            try:
                dt = datetime.strptime(
                    vals['data_nascimento'], '%d/%m/%Y').date()
                self.cadastrar_paciente(
                    vals['nome'], vals['telefone'], vals['cpf'], dt
                )
                self.paciente_view.mostra_mensagem(
                    'Sucesso', 'Paciente cadastrado com sucesso!')
            except ValueError:
                self.paciente_view.mostra_mensagem(
                    'Erro',
                    'Formato de data inválido! Use DD/MM/AAAA.')
            except RegraNegocioException as e:
                self.paciente_view.mostra_mensagem('Erro', str(e))

    def _alterar_paciente(self):
        pacientes = self.context.pacientes
        if not pacientes:
            self.paciente_view.mostra_mensagem(
                'Aviso', 'Nenhum paciente cadastrado.')
            return
        nomes = [f"{p.nome} (CPF: {p.cpf})" for p in pacientes]
        idx = self.paciente_view.mostra_lista_selecao(
            'Selecionar Paciente para Alterar', nomes)
        if idx is None:
            return
        paciente = pacientes[idx]
        dados = {
            'nome': paciente.nome,
            'telefone': paciente.telefone,
            'cpf': paciente.cpf,
            'data_nascimento': paciente.data_nascimento.strftime('%d/%m/%Y')
        }
        botao, vals = self.paciente_view.tela_formulario(dados)
        if botao == 'Confirmar':
            try:
                dt = datetime.strptime(
                    vals['data_nascimento'], '%d/%m/%Y').date()
                self.alterar_paciente(
                    paciente, vals['nome'], vals['telefone'],
                    vals['cpf'], dt
                )
                self.paciente_view.mostra_mensagem(
                    'Sucesso', 'Paciente alterado com sucesso!')
            except ValueError:
                self.paciente_view.mostra_mensagem(
                    'Erro',
                    'Formato de data inválido! Use DD/MM/AAAA.')
            except RegraNegocioException as e:
                self.paciente_view.mostra_mensagem('Erro', str(e))

    def _excluir_paciente(self):
        pacientes = self.context.pacientes
        if not pacientes:
            self.paciente_view.mostra_mensagem(
                'Aviso', 'Nenhum paciente cadastrado.')
            return
        nomes = [f"{p.nome} (CPF: {p.cpf})" for p in pacientes]
        idx = self.paciente_view.mostra_lista_selecao(
            'Selecionar Paciente para Excluir', nomes)
        if idx is None:
            return
        paciente = pacientes[idx]
        try:
            self.excluir_paciente(paciente)
            self.paciente_view.mostra_mensagem(
                'Sucesso', 'Paciente excluído com sucesso!')
        except RegraNegocioException as e:
            self.paciente_view.mostra_mensagem('Erro', str(e))


    # ================================================================
    #  PROFISSIONAIS - UI
    # ================================================================
    def abrir_tela_profissional(self):
        while True:
            botao, valores = self.profissional_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_profissionais()
            elif botao == 'Cadastrar':
                self._cadastrar_profissional()
            elif botao == 'Alterar':
                self._alterar_profissional()
            elif botao == 'Excluir':
                self._excluir_profissional()

    def _obter_lista_especialidades(self):
        return [esp.value for esp in Especialidade]

    def _listar_profissionais(self):
        profissionais = self.context.profissionais
        if not profissionais:
            self.profissional_view.mostra_mensagem(
                'Aviso', 'Nenhum profissional cadastrado.')
            return
        dados = []
        for p in profissionais:
            dados.append({
                'nome': p.nome,
                'registro': str(p.registro),
                'especialidade': p.especialidade.value,
                'telefone': p.telefone
            })
        self.profissional_view.tela_listagem(dados)

    def _cadastrar_profissional(self):
        especialidades = self._obter_lista_especialidades()
        botao, vals = self.profissional_view.tela_formulario(especialidades)
        if botao == 'Confirmar':
            try:
                especialidade = None
                for esp in Especialidade:
                    if esp.value == vals['especialidade']:
                        especialidade = esp
                        break
                if especialidade is None:
                    self.profissional_view.mostra_mensagem(
                        'Erro', 'Selecione uma especialidade válida.')
                    return
                registro = int(vals['registro'])
                self.cadastrar_profissional(
                    vals['nome'], vals['telefone'], vals['cpf'],
                    especialidade, registro
                )
                self.profissional_view.mostra_mensagem(
                    'Sucesso', 'Profissional cadastrado com sucesso!')
            except ValueError:
                self.profissional_view.mostra_mensagem(
                    'Erro', 'Registro CRM deve ser um número inteiro.')
            except RegraNegocioException as e:
                self.profissional_view.mostra_mensagem('Erro', str(e))

    def _alterar_profissional(self):
        profissionais = self.context.profissionais
        if not profissionais:
            self.profissional_view.mostra_mensagem(
                'Aviso', 'Nenhum profissional cadastrado.')
            return
        nomes = [f"{p.nome} (CRM: {p.registro})" for p in profissionais]
        idx = self.profissional_view.mostra_lista_selecao(
            'Selecionar Profissional para Alterar', nomes)
        if idx is None:
            return
        profissional = profissionais[idx]
        dados = {
            'nome': profissional.nome,
            'telefone': profissional.telefone,
            'cpf': profissional.cpf,
            'especialidade': profissional.especialidade.value,
            'registro': str(profissional.registro)
        }
        especialidades = self._obter_lista_especialidades()
        botao, vals = self.profissional_view.tela_formulario(
            especialidades, dados)
        if botao == 'Confirmar':
            try:
                especialidade = None
                for esp in Especialidade:
                    if esp.value == vals['especialidade']:
                        especialidade = esp
                        break
                if especialidade is None:
                    self.profissional_view.mostra_mensagem(
                        'Erro', 'Selecione uma especialidade válida.')
                    return
                registro = int(vals['registro'])
                self.alterar_profissional(
                    profissional, vals['nome'], vals['telefone'],
                    vals['cpf'], especialidade, registro
                )
                self.profissional_view.mostra_mensagem(
                    'Sucesso', 'Profissional alterado com sucesso!')
            except ValueError:
                self.profissional_view.mostra_mensagem(
                    'Erro', 'Registro CRM deve ser um número inteiro.')
            except RegraNegocioException as e:
                self.profissional_view.mostra_mensagem('Erro', str(e))

    def _excluir_profissional(self):
        profissionais = self.context.profissionais
        if not profissionais:
            self.profissional_view.mostra_mensagem(
                'Aviso', 'Nenhum profissional cadastrado.')
            return
        nomes = [f"{p.nome} (CRM: {p.registro})" for p in profissionais]
        idx = self.profissional_view.mostra_lista_selecao(
            'Selecionar Profissional para Excluir', nomes)
        if idx is None:
            return
        profissional = profissionais[idx]
        try:
            self.excluir_profissional(profissional)
            self.profissional_view.mostra_mensagem(
                'Sucesso', 'Profissional excluído com sucesso!')
        except RegraNegocioException as e:
            self.profissional_view.mostra_mensagem('Erro', str(e))

    # ================================================================
    #  REGRAS DE NEGÓCIO - PACIENTE
    # ================================================================
    def cadastrar_paciente(self, nome: str, telefone: str, cpf: str, data_nascimento: date) -> Paciente:
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        if self.paciente_dao.get(cpf) is not None:
            raise RegraNegocioException(f"Já existe um paciente cadastrado com o CPF {cpf}.")
        paciente = Paciente(nome, telefone, cpf, data_nascimento)
        if paciente not in self.context.pacientes: self.context.pacientes.append(paciente)
        return paciente

    def alterar_paciente(self, paciente: Paciente, nome: str, telefone: str, cpf: str, data_nascimento: date):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        existente = self.paciente_dao.get(cpf)
        if existente is not None and existente.cpf != paciente.cpf:
            raise RegraNegocioException(f"Já existe outro paciente cadastrado com o CPF {cpf}.")
        if paciente.cpf != cpf:
            if paciente in self.context.pacientes: self.context.pacientes.remove(paciente)
        paciente.nome = nome
        paciente.telefone = telefone
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento
        if paciente not in self.context.pacientes: self.context.pacientes.append(paciente)

    def excluir_paciente(self, paciente: Paciente):
        if any(at.paciente.cpf == paciente.cpf for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir este paciente pois ele possui atendimentos agendados.")
        if paciente in self.context.pacientes: self.context.pacientes.remove(paciente)

    # ================================================================
    #  REGRAS DE NEGÓCIO - PROFISSIONAL
    # ================================================================
    def cadastrar_profissional(self, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int) -> ProfissionalSaude:
        validar_obrigatorios({"Nome": nome, "CPF": cpf, "Registro CRM": registro})
        if self.profissional_dao.get(cpf) is not None:
            raise RegraNegocioException(f"Já existe um profissional cadastrado com o CPF {cpf}.")
        if any(p.registro == registro for p in self.context.profissionais):
            raise RegraNegocioException(f"Já existe um profissional cadastrado com o registro {registro}.")
        profissional = ProfissionalSaude(nome, telefone, cpf, especialidade, registro)
        if profissional not in self.context.profissionais: self.context.profissionais.append(profissional)
        return profissional

    def alterar_profissional(self, profissional: ProfissionalSaude, nome: str, telefone: str, cpf: str, especialidade: Especialidade, registro: int):
        validar_obrigatorios({"Nome": nome, "CPF": cpf, "Registro CRM": registro})
        existente = self.profissional_dao.get(cpf)
        if existente is not None and existente.cpf != profissional.cpf:
            raise RegraNegocioException(f"Já existe outro profissional cadastrado com o CPF {cpf}.")
        if any(p.registro == registro and p.cpf != profissional.cpf for p in self.context.profissionais):
            raise RegraNegocioException(f"Já existe outro profissional cadastrado com o registro {registro}.")
        if profissional.cpf != cpf:
            if profissional in self.context.profissionais: self.context.profissionais.remove(profissional)
        profissional.nome = nome
        profissional.telefone = telefone
        profissional.cpf = cpf
        profissional.especialidade = especialidade
        profissional.registro = registro
        if profissional not in self.context.profissionais: self.context.profissionais.append(profissional)

    def excluir_profissional(self, profissional: ProfissionalSaude):
        if any(at.profissional.cpf == profissional.cpf for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir este profissional pois ele possui atendimentos vinculados.")
        if profissional in self.context.profissionais: self.context.profissionais.remove(profissional)
