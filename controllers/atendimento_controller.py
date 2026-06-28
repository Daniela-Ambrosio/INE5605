from datetime import date, time, datetime
from models import Clinica, Paciente, ProfissionalSaude, Atendimento, TipoAtendimento, Procedimento
from .validacoes import RegraNegocioException
from .context import Context
from views.atendimento_view import AtendimentoView
from views.procedimento_view import ProcedimentoView

class AtendimentoController:
    def __init__(self, context):
        self.__context = context
        self.__atendimento_view = AtendimentoView()
        self.__procedimento_view = ProcedimentoView()

    # ==================== ATENDIMENTOS ====================
    def abrir_tela_atendimento(self):
        while True:
            opcao = self.__atendimento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_atendimento()
            elif opcao == 2: self._alterar_atendimento()
            elif opcao == 3: self._listar_atendimentos()
            elif opcao == 4: self._excluir_atendimento()

    def _listar_atendimentos(self):
        dados = []
        for at in self.context.atendimentos:
            pago = 'Pago' if at.pagamento else 'Pendente'
            dados.append({
                'data': at.data.strftime('%d/%m/%Y'),
                'inicio': at.inicio.strftime('%H:%M'),
                'fim': at.fim.strftime('%H:%M'),
                'clinica': at.clinica.nome,
                'paciente': at.paciente.nome,
                'profissional': at.profissional.nome,
                'tipo': at.tipo.value,
                'custo': f"{at.custo:.2f}",
                'status': pago
            })
        self.__atendimento_view.mostra_atendimento(dados)

    def _buscar_atendimento(self, dt, ini):
        for at in self.context.atendimentos:
            if at.data.strftime('%d/%m/%Y') == dt and at.inicio.strftime('%H:%M') == ini:
                return at
        return None

    def _buscar_clinica(self, nome):
        for c in self.context.clinicas:
            if c.nome == nome: return c
        return None

    def _buscar_paciente(self, cpf):
        for p in self.context.pacientes:
            if p.cpf == cpf: return p
        return None

    def _buscar_profissional(self, nome):
        for p in self.context.profissionais:
            if p.nome == nome: return p
        return None

    def _cadastrar_atendimento(self):
        vals = self.__atendimento_view.pega_dados_atendimento()
        if vals:
            try:
                c = self._buscar_clinica(vals['clinica'])
                pa = self._buscar_paciente(vals['paciente'])
                pr = self._buscar_profissional(vals['profissional'])
                if not c: raise ValueError("Clínica não encontrada.")
                if not pa: raise ValueError("Paciente não encontrado.")
                if not pr: raise ValueError("Profissional não encontrado.")
                
                dt = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                hi = datetime.strptime(vals['inicio'], '%H:%M').time()
                hf = datetime.strptime(vals['fim'], '%H:%M').time()
                
                tipo = None
                for t in TipoAtendimento:
                    if t.value == vals['tipo']: tipo = t
                if not tipo: raise ValueError("Tipo inválido.")
                
                custo = float(vals['custo'])
                self.agendar_atendimento(c, pa, pr, dt, hi, hf, tipo, custo)
                self.__atendimento_view.mostra_mensagem('Atendimento cadastrado!')
            except ValueError as e:
                self.__atendimento_view.mostra_mensagem(f'Erro: {e}')
            except RegraNegocioException as e:
                self.__atendimento_view.mostra_mensagem(str(e))

    def _alterar_atendimento(self):
        self._listar_atendimentos()
        dt, ini = self.__atendimento_view.seleciona_atendimento()
        if dt and ini:
            at = self._buscar_atendimento(dt, ini)
            if not at:
                self.__atendimento_view.mostra_mensagem('Atendimento não encontrado.')
                return
            vals = self.__atendimento_view.pega_dados_atendimento()
            if vals:
                try:
                    c = self._buscar_clinica(vals['clinica'])
                    pa = self._buscar_paciente(vals['paciente'])
                    pr = self._buscar_profissional(vals['profissional'])
                    if not c: raise ValueError("Clínica não encontrada.")
                    if not pa: raise ValueError("Paciente não encontrado.")
                    if not pr: raise ValueError("Profissional não encontrado.")
                    
                    ndt = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                    nhi = datetime.strptime(vals['inicio'], '%H:%M').time()
                    nhf = datetime.strptime(vals['fim'], '%H:%M').time()
                    tipo = None
                    for t in TipoAtendimento:
                        if t.value == vals['tipo']: tipo = t
                    if not tipo: raise ValueError("Tipo inválido.")
                    custo = float(vals['custo'])

                    self.alterar_atendimento(at, c, pa, pr, ndt, nhi, nhf, tipo, custo)
                    self.__atendimento_view.mostra_mensagem('Atendimento alterado!')
                except Exception as e:
                    self.__atendimento_view.mostra_mensagem(f'Erro: {e}')

    def _excluir_atendimento(self):
        self._listar_atendimentos()
        dt, ini = self.__atendimento_view.seleciona_atendimento()
        if dt and ini:
            at = self._buscar_atendimento(dt, ini)
            if at:
                self.excluir_atendimento(at)
                self.__atendimento_view.mostra_mensagem('Excluído com sucesso!')
            else:
                self.__atendimento_view.mostra_mensagem('Não encontrado.')

    # ==================== PROCEDIMENTOS ====================
    def abrir_tela_procedimento(self):
        while True:
            opcao = self.__procedimento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_procedimento()
            elif opcao == 2: self._alterar_procedimento()
            elif opcao == 3: self._listar_procedimentos()
            elif opcao == 4: self._excluir_procedimento()

    def _selecionar_atendimento_para_procedimento(self):
        self._listar_atendimentos()
        dt, ini = self.__atendimento_view.seleciona_atendimento()
        if dt and ini: 
            at = self._buscar_atendimento(dt, ini)
            if at:
                return at
            else:
                self.__procedimento_view.mostra_mensagem("Atendimento não encontrado.")
                return None
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
        vals = self.__procedimento_view.pega_dados_procedimento()
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
        self._listar_procedimentos()
        descricoes = [p.descricao for p in at.procedimentos]
        desc = self.__procedimento_view.seleciona_procedimento(descricoes)
        proc_target = None
        for p in at.procedimentos:
            if p.descricao == desc: proc_target = p
        if not proc_target:
            self.__procedimento_view.mostra_mensagem("Não encontrado.")
            return

        vals = self.__procedimento_view.pega_dados_procedimento()
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
        desc = self.__procedimento_view.seleciona_procedimento(descricoes)
        proc_target = None
        for p in at.procedimentos:
            if p.descricao == desc: proc_target = p
        if proc_target:
            self.excluir_procedimento(at, proc_target)
            self.__procedimento_view.mostra_mensagem("Excluído.")

    # ==================== REGRAS DE NEGOCIO ====================
    def agendar_atendimento(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, 
                            data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float = 0.0) -> Atendimento:
        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18: raise RegraNegocioException("Maioridade necessária.")
        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("Fora do horário da clínica.")
        for at in self.context.atendimentos:
            if at.data == data and at.inicio == hora_inicio:
                raise RegraNegocioException("Horário já preenchido.")
        at = Atendimento(clinica, paciente, profissional, data, hora_inicio, hora_fim, tipo, custo)
        self.context.atendimentos.append(at)
        return at

    def alterar_atendimento(self, atendimento: Atendimento, clinica: Clinica, paciente: Paciente, 
                            profissional: ProfissionalSaude, data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float):
        atendimento.clinica = clinica
        atendimento.paciente = paciente
        atendimento.profissional = profissional
        atendimento.data = data
        atendimento.inicio = hora_inicio
        atendimento.fim = hora_fim
        atendimento.tipo = tipo
        atendimento.custo = custo

    def excluir_atendimento(self, atendimento: Atendimento):
        if atendimento in self.context.atendimentos: self.context.atendimentos.remove(atendimento)

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

    def excluir_procedimento(self, atendimento: Atendimento, procedimento: Procedimento):
        if procedimento in atendimento.procedimentos:
            atendimento.custo -= procedimento.custo
            atendimento.procedimentos.remove(procedimento)
