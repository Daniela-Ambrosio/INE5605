from datetime import date, datetime
from models import Paciente
from .validacoes import RegraNegocioException
from views import PacienteView
from DAOs import PacienteDAO, AtendimentoDAO

class PacienteController:
    def __init__(self):
        self.__paciente_DAO = PacienteDAO()
        self.__atendimento_DAO = AtendimentoDAO()
        self.__paciente_view = PacienteView()

    def abrir_tela_paciente(self):
        while True:
            opcao = self.__paciente_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self.tela_cadastrar_paciente()
            elif opcao == 2: self.tela_alterar_paciente()
            elif opcao == 3: self.listar_pacientes()
            elif opcao == 4: self.tela_excluir_paciente()

    def listar_pacientes(self):
        dados = []
        for p in self.__paciente_DAO.get_all():
            dados.append({
                'nome': p.nome,
                'telefone': p.telefone,
                'cpf': p.cpf
            })
        self.__paciente_view.mostra_paciente(dados)

    def buscar_paciente_por_cpf(self, cpf):
        for p in self.__paciente_DAO.get_all():
            if p.cpf == cpf: return p
        return None

    def tela_cadastrar_paciente(self):
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

    def tela_alterar_paciente(self):
        self.listar_pacientes()
        cpfs = [p.cpf for p in self.__paciente_DAO.get_all()]
        cpf = self.__paciente_view.seleciona_paciente(cpfs)
        if cpf:
            paciente = self.buscar_paciente_por_cpf(cpf)
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

    def tela_excluir_paciente(self):
        self.listar_pacientes()
        cpfs = [p.cpf for p in self.__paciente_DAO.get_all()]
        cpf = self.__paciente_view.seleciona_paciente(cpfs)
        if cpf:
            paciente = self.buscar_paciente_por_cpf(cpf)
            if not paciente:
                self.__paciente_view.mostra_mensagem('Paciente não encontrado.')
                return
            try:
                self.excluir_paciente(paciente)
                self.__paciente_view.mostra_mensagem('Paciente excluído!')
            except RegraNegocioException as e:
                self.__paciente_view.mostra_mensagem(str(e))

    def cadastrar_paciente(self, nome, telefone, cpf, data_nascimento):
        if self.buscar_paciente_por_cpf(cpf):
            raise RegraNegocioException("CPF já cadastrado.")
        p = Paciente(nome, telefone, cpf, data_nascimento)
        self.__paciente_DAO.add(p)
        return p

    def alterar_paciente(self, paciente, nome, telefone, cpf, data_nascimento):
        paciente.nome = nome
        paciente.telefone = telefone
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento

        self.__paciente_DAO.update(paciente)

    def excluir_paciente(self, paciente):
        if any(at.paciente.cpf == paciente.cpf for at in self.__atendimento_DAO.get_all()):
            raise RegraNegocioException("Paciente possui atendimentos e não pode ser excluído.")

        if any(p.cpf == paciente.cpf for p in self.__paciente_DAO.get_all()): self.__paciente_DAO.remove(paciente.cpf)

    