from models import ProfissionalSaude, Especialidade
from .validacoes import RegraNegocioException
from views import ProfissionalView
from DAOs import ProfissionalDAO, AtendimentoDAO


class ProfissionalController:
    def __init__(self):
        self.__profissional_DAO = ProfissionalDAO()
        self.__atendimento_DAO = AtendimentoDAO()
        self.__profissional_view = ProfissionalView()

    def abrir_tela_profissional(self):
        while True:
            opcao = self.__profissional_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self.tela_cadastrar_profissional()
            elif opcao == 2: self.tela_alterar_profissional()
            elif opcao == 3: self.listar_profissionais()
            elif opcao == 4: self.tela_excluir_profissional()

    def listar_profissionais(self):
        dados = []
        for p in self.__profissional_DAO.get_all():
            dados.append({
                'nome': p.nome,
                'telefone': p.telefone,
                'cpf': p.cpf,
                'registro': str(p.registro),
                'especialidade': p.especialidade.value
            })
        self.__profissional_view.mostra_profissional(dados)

    def buscar_profissional_por_cpf(self, cpf):
        for p in self.__profissional_DAO.get_all():
            if p.cpf == cpf: return p
        return None

    def tela_cadastrar_profissional(self):
        vals = self.__profissional_view.pega_dados_profissional()
        if vals:
            try:
                esp = None
                for e in Especialidade:
                    if e.value == vals['especialidade']: esp = e
                if not esp: raise ValueError("Especialidade inválida")
                self.cadastrar_profissional(vals['nome'], vals['telefone'], vals['cpf'], esp, int(vals['registro']))
                self.__profissional_view.mostra_mensagem('Profissional cadastrado!')
            except ValueError:
                self.__profissional_view.mostra_mensagem('Erro nos dados.')
            except RegraNegocioException as e:
                self.__profissional_view.mostra_mensagem(str(e))

    def tela_alterar_profissional(self):
        self.listar_profissionais()
        cpfs = [p.cpf for p in self.__profissional_DAO.get_all()]
        cpf = self.__profissional_view.seleciona_profissional(cpfs)
        if cpf:
            profissional = self.buscar_profissional_por_cpf(cpf)
            if not profesional:
                self.__profissional_view.mostra_mensagem('Profissional não encontrado.')
                return
            vals = self.__profissional_view.pega_dados_profissional()
            if vals:
                try:
                    esp = None
                    for e in Especialidade:
                        if e.value == vals['especialidade']: esp = e
                    if not esp: raise ValueError("Especialidade inválida")
                    self.alterar_profissional(profissional, vals['nome'], vals['telefone'], vals['cpf'], esp, int(vals['registro']))
                    self.__profissional_view.mostra_mensagem('Profissional alterado!')
                except ValueError:
                    self.__profissional_view.mostra_mensagem('Erro nos dados.')
                except RegraNegocioException as e:
                    self.__profissional_view.mostra_mensagem(str(e))

    def tela_excluir_profissional(self):
        self.listar_profissionais()
        cpfs = [p.cpf for p in self.__profissional_DAO.get_all()]
        cpf = self.__profissional_view.seleciona_profissional(cpfs)
        if cpf:
            profissional = self.buscar_profissional_por_cpf(cpf)
            if not profissional:
                self.__profissional_view.mostra_mensagem('Profissional não encontrado.')
                return
            try:
                self.excluir_profissional(profissional)
                self.__profissional_view.mostra_mensagem('Profissional excluído!')
            except RegraNegocioException as e:
                self.__profissional_view.mostra_mensagem(str(e))

    def cadastrar_profissional(self, nome, telefone, cpf, especialidade, registro):
        if self.buscar_profissional_por_cpf(cpf):
            raise RegraNegocioException("CPF já cadastrado.")
        p = ProfissionalSaude(nome, telefone, cpf, especialidade, registro)
        self.__profissional_DAO.add(p)
        return p

    def alterar_profissional(self, profissional, nome, telefone, cpf, especialidade, registro):
        profissional.nome = nome
        profissional.telefone = telefone
        profissional.cpf = cpf
        profissional.especialidade = especialidade
        profissional.registro = registro

        self.__profissional_DAO.update(profissional)

    def excluir_profissional(self, profissional):
        if any(at.profissional.cpf == profissional.cpf for at in self.__atendimento_DAO.get_all()):
            raise RegraNegocioException("Profissional possui atendimentos agendados.")

        if any(p.cpf == profissional.cpf for p in self.__profissional_DAO.get_all()): self.__profissional_DAO.remove(profissional.cpf)
