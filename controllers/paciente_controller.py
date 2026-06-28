from datetime import date, datetime
from models import Paciente
from .validacoes import validar_obrigatorios, RegraNegocioException
from .context import Context
from views.paciente_view import PacienteView

class PacienteController:
    def __init__(self, context):
        self.__context = context
        self.__paciente_view = PacienteView()
        self.__profissional_view = ProfissionalView()

    # ==================== PACIENTES ====================
    def abrir_tela_paciente(self):
        while True:
            opcao = self.__paciente_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_paciente()
            elif opcao == 2: self._alterar_paciente()
            elif opcao == 3: self._listar_pacientes()
            elif opcao == 4: self._excluir_paciente()

    def _listar_pacientes(self):
        dados = []
        for p in self.__context.pacientes:
            dados.append({
                'nome': p.nome,
                'telefone': p.telefone,
                'cpf': p.cpf
            })
        self.__paciente_view.mostra_paciente(dados)

    def _buscar_paciente_por_cpf(self, cpf):
        for p in self.__context.pacientes:
            if p.cpf == cpf: return p
        return None

    def _cadastrar_paciente(self):
        vals = self.__paciente_view.pega_dados_paciente()
        if vals:
            try:
                dt_nasc = datetime.strptime(vals['data_nascimento'], '%d/%m/%Y').date()
                self.cadastrar_paciente(vals['nome'], vals['telefone'], vals['cpf'], dt_nasc)
                self.__paciente_view.mostra_mensagem('Paciente cadastrado!')
            except ValueError:
                self.__paciente_view.mostra_mensagem('Erro na data.')
            except RegraNegocioException as e:
                self.__paciente_view.mostra_mensagem(str(e))

    def _alterar_paciente(self):
        self._listar_pacientes()
        cpf = self.__paciente_view.seleciona_paciente()
        if cpf:
            paciente = self._buscar_paciente_por_cpf(cpf)
            if not paciente:
                self.__paciente_view.mostra_mensagem('Paciente não encontrado.')
                return
            vals = self.__paciente_view.pega_dados_paciente()
            if vals:
                try:
                    dt_nasc = datetime.strptime(vals['data_nascimento'], '%d/%m/%Y').date()
                    self.alterar_paciente(paciente, vals['nome'], vals['telefone'], vals['cpf'], dt_nasc)
                    self.__paciente_view.mostra_mensagem('Paciente alterado!')
                except ValueError:
                    self.__paciente_view.mostra_mensagem('Erro na data.')
                except RegraNegocioException as e:
                    self.__paciente_view.mostra_mensagem(str(e))

    def _excluir_paciente(self):
        self._listar_pacientes()
        cpf = self.__paciente_view.seleciona_paciente()
        if cpf:
            paciente = self._buscar_paciente_por_cpf(cpf)
            if not paciente:
                self.__paciente_view.mostra_mensagem('Paciente não encontrado.')
                return
            try:
                self.excluir_paciente(paciente)
                self.__paciente_view.mostra_mensagem('Paciente excluído!')
            except RegraNegocioException as e:
                self.__paciente_view.mostra_mensagem(str(e))

    def cadastrar_paciente(self, nome, telefone, cpf, data_nascimento):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        if self._buscar_paciente_por_cpf(cpf):
            raise RegraNegocioException("CPF já cadastrado.")
        p = Paciente(nome, telefone, cpf, data_nascimento)
        self.__context.pacientes.append(p)
        return p

    def alterar_paciente(self, paciente, nome, telefone, cpf, data_nascimento):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        paciente.nome = nome
        paciente.telefone = telefone
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento

    def excluir_paciente(self, paciente):
        if any(at.paciente.cpf == paciente.cpf for at in self.__context.atendimentos):
            raise RegraNegocioException("Paciente possui atendimentos e não pode ser excluído.")
        if paciente in self.__context.pacientes: self.__context.pacientes.remove(paciente)

    