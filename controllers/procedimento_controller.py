from models import Procedimento, Atendimento, ProfissionalSaude
from views import ProcedimentoView, AtendimentoView
from DAOs import ProcedimentoDAO, ProfissionalDAO

class ProcedimentoController:
    def __init__(self):
        self.__procedimento_DAO = ProcedimentoDAO()
        self.__profissional_DAO = ProfissionalDAO()
        self.__procedimento_view = ProcedimentoView()
        self.__atendimento_view = AtendimentoView()

    def abrir_tela_procedimento(self):
        while True:
            opcao = self.__procedimento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_procedimento()
            elif opcao == 2: self._alterar_procedimento()
            elif opcao == 3: self._listar_procedimentos()
            elif opcao == 4: self._excluir_procedimento()

    def _buscar_atendimento(self, dt, ini):
        for at in self.__procedimento_DAO.get_all():
            if at.data.strftime('%d/%m/%Y') == dt and at.inicio.strftime('%H:%M') == ini:
                return at
        return None

    def _buscar_profissional(self, nome):
        for p in self.__profissional_DAO.get_all():
            if p.nome == nome: return p
        return None

    def _selecionar_atendimento_para_procedimento(self):
        lista = [f"{a.data.strftime('%d/%m/%Y')} às {a.inicio.strftime('%H:%M')} - Paciente: {a.paciente.nome}" for a in self.__procedimento_DAO.get_all()]
        escolha = self.__atendimento_view.seleciona_atendimento(lista)
        if escolha: 
            for at in self.__procedimento_DAO.get_all():
                if f"{at.data.strftime('%d/%m/%Y')} às {at.inicio.strftime('%H:%M')} - Paciente: {at.paciente.nome}" == escolha:
                    return at
        return None

    def _listar_procedimentos(self):
        at = self._selecionar_atendimento_para_procedimento()
        if at:
            dados = []
            for proc in at.procedimentos:
                dados.append({
                    'descricao': proc.descricao,
                    'custo': f"{proc.custo:.2f}",
                    'profissional': proc.profissional.nome
                })
            self.__procedimento_view.mostra_procedimento(dados)

    def _cadastrar_procedimento(self):
        at = self._selecionar_atendimento_para_procedimento()
        if not at: return
        
        nomes_profissionais = [p.nome for p in self.__profissional_DAO.get_all()]
        vals = self.__procedimento_view.pega_dados_procedimento(nomes_profissionais)
        if vals:
            try:
                pr = self._buscar_profissional(vals['profissional'])
                if not pr: raise ValueError("Profissional não encontrado.")
                custo = float(vals['custo'])
                self.adicionar_procedimento_a_atendimento(at, vals['descricao'], custo, pr)
                self.__procedimento_view.mostra_mensagem('Procedimento adicionado!')
            except Exception as e:
                self.__procedimento_view.mostra_mensagem(f'Erro: {e}')

    def _alterar_procedimento(self):
        at = self._selecionar_atendimento_para_procedimento()
        if not at: return
        
        descricoes = [p.descricao for p in at.procedimentos]
        if not descricoes:
            self.__procedimento_view.mostra_mensagem("Não há procedimentos neste atendimento.")
            return
            
        desc = self.__procedimento_view.seleciona_procedimento(descricoes)
        proc_target = None
        for p in at.procedimentos:
            if p.descricao == desc: proc_target = p
        if not proc_target:
            self.__procedimento_view.mostra_mensagem("Não encontrado.")
            return

        nomes_profissionais = [p.nome for p in self.__profissional_DAO.get_all()]
        vals = self.__procedimento_view.pega_dados_procedimento(nomes_profissionais)
        if vals:
            try:
                pr = self._buscar_profissional(vals['profissional'])
                if not pr: raise ValueError("Profissional não encontrado.")
                custo = float(vals['custo'])
                self.alterar_procedimento(at, proc_target, vals['descricao'], custo, pr)
                self.__procedimento_view.mostra_mensagem('Alterado!')
            except Exception as e:
                self.__procedimento_view.mostra_mensagem(f'Erro: {e}')

    def _excluir_procedimento(self):
        at = self._selecionar_atendimento_para_procedimento()
        if not at: return
        descricoes = [p.descricao for p in at.procedimentos]
        if not descricoes:
            self.__procedimento_view.mostra_mensagem("Não há procedimentos neste atendimento.")
            return
            
        desc = self.__procedimento_view.seleciona_procedimento(descricoes)
        proc_target = None
        for p in at.procedimentos:
            if p.descricao == desc: proc_target = p
        if proc_target:
            self.excluir_procedimento(at, proc_target)
            self.__procedimento_view.mostra_mensagem("Excluído.")

    def adicionar_procedimento_a_atendimento(self, atendimento: Atendimento, descricao: str, custo: float, profissional: ProfissionalSaude) -> Procedimento:
        procedimento = Procedimento(descricao, custo, profissional)
        atendimento.adicionar_procedimento(procedimento)
        return procedimento

    def alterar_procedimento(self, atendimento: Atendimento, procedimento: Procedimento, descricao: str, custo: float, profissional: ProfissionalSaude):
        atendimento.custo -= procedimento.custo
        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.profissional = profissional
        atendimento.custo += custo

        self.__procedimento_DAO.update(procedimento)

    def excluir_procedimento(self, atendimento: Atendimento, procedimento: Procedimento):
        if procedimento in atendimento.procedimentos:
            atendimento.custo -= procedimento.custo
            atendimento.procedimentos.remove(procedimento)
