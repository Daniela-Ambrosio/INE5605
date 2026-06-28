from models import ProfissionalSaude, Especialidade
from .validacoes import validar_obrigatorios, RegraNegocioException
from .context import Context
from views.profissional_view import ProfissionalView

class ProfissionalController:
    def __init__(self, context):
        self.__context = context
        self.__profissional_view = ProfissionalView()

    # ==================== PROFISSIONAIS ====================
    def abrir_tela_profissional(self):
        while True:
            opcao = self.__profissional_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_profissional()
            elif opcao == 2: self._alterar_profissional()
            elif opcao == 3: self._listar_profissionais()
            elif opcao == 4: self._excluir_profissional()

    def _listar_profissionais(self):
        dados = []
        for p in self.__context.profissionais:
            dados.append({
                'nome': p.nome,
                'telefone': p.telefone,
                'cpf': p.cpf,
                'registro': str(p.registro),
                'especialidade': p.especialidade.value
            })
        self.__profissional_view.mostra_profissional(dados)

    def _buscar_profissional_por_cpf(self, cpf):
        for p in self.__context.profissionais:
            if p.cpf == cpf: return p
        return None

    def _cadastrar_profissional(self):
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

    def _alterar_profissional(self):
        self._listar_profissionais()
        cpf = self.__profissional_view.seleciona_profissional()
        if cpf:
            profissional = self._buscar_profissional_por_cpf(cpf)
            if not profissional:
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

    def _excluir_profissional(self):
        self._listar_profissionais()
        cpf = self.__profissional_view.seleciona_profissional()
        if cpf:
            profissional = self._buscar_profissional_por_cpf(cpf)
            if not profissional:
                self.__profissional_view.mostra_mensagem('Profissional não encontrado.')
                return
            try:
                self.excluir_profissional(profissional)
                self.__profissional_view.mostra_mensagem('Profissional excluído!')
            except RegraNegocioException as e:
                self.__profissional_view.mostra_mensagem(str(e))

    def cadastrar_profissional(self, nome, telefone, cpf, especialidade, registro):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        if self._buscar_profissional_por_cpf(cpf):
            raise RegraNegocioException("CPF já cadastrado.")
        p = ProfissionalSaude(nome, telefone, cpf, especialidade, registro)
        self.__context.profissionais.append(p)
        return p

    def alterar_profissional(self, profissional, nome, telefone, cpf, especialidade, registro):
        validar_obrigatorios({"Nome": nome, "CPF": cpf})
        profissional.nome = nome
        profissional.telefone = telefone
        profissional.cpf = cpf
        profissional.especialidade = especialidade
        profissional.registro = registro

    def excluir_profissional(self, profissional):
        if any(at.profissional.cpf == profissional.cpf for at in self.__context.atendimentos):
            raise RegraNegocioException("Profissional possui atendimentos agendados.")
        if profissional in self.__context.profissionais: self.__context.profissionais.remove(profissional)
