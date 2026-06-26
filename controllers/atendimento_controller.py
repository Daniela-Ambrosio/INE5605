from datetime import date, time, datetime
from models import Clinica, Paciente, ProfissionalSaude, Atendimento, TipoAtendimento, Procedimento
from .validacoes import validar_tipo, RegraNegocioException
from .context import Context
from views.atendimento_view import AtendimentoView
from views.procedimento_view import ProcedimentoView

class AtendimentoController:
    def __init__(self, context):
        self.context = context
        self.atendimento_view = AtendimentoView()
        self.procedimento_view = ProcedimentoView()

    # ================================================================
    #  ATENDIMENTOS - UI
    # ================================================================
    def abrir_tela_atendimento(self):
        while True:
            botao, valores = self.atendimento_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_atendimentos()
            elif botao == 'Cadastrar':
                self._cadastrar_atendimento()
            elif botao == 'Alterar':
                self._alterar_atendimento()
            elif botao == 'Excluir':
                self._excluir_atendimento()

    def _obter_descricoes_atendimentos(self, lista=None):
        if lista is None:
            lista = self.context.atendimentos
        descricoes = []
        for at in lista:
            pago = 'Pago' if at.pagamento else 'Pendente'
            descricoes.append(
                f"{at.paciente.nome} | {at.data.strftime('%d/%m/%Y')} | "
                f"{at.clinica.nome} | R$ {at.custo:.2f} ({pago})"
            )
        return descricoes

    def _listar_atendimentos(self):
        atendimentos = self.context.atendimentos
        if not atendimentos:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Nenhum atendimento agendado.')
            return
        dados = []
        for at in atendimentos:
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
        self.atendimento_view.tela_listagem(dados)

    def _cadastrar_atendimento(self):
        clinicas = self.context.clinicas
        pacientes = self.context.pacientes
        profissionais = self.context.profissionais

        if not clinicas:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Cadastre pelo menos uma clínica antes.')
            return
        if not pacientes:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Cadastre pelo menos um paciente antes.')
            return
        if not profissionais:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Cadastre pelo menos um profissional antes.')
            return

        nomes_clinicas = [f"{c.nome} ({c.cidade})" for c in clinicas]
        nomes_pacientes = [f"{p.nome} (CPF: {p.cpf})" for p in pacientes]
        nomes_profissionais = [f"{p.nome} ({p.especialidade.value})" for p in profissionais]
        lista_tipos = [t.value for t in TipoAtendimento]

        botao, vals = self.atendimento_view.tela_formulario(
            nomes_clinicas, nomes_pacientes,
            nomes_profissionais, lista_tipos
        )
        if botao == 'Confirmar':
            try:
                idx_c = nomes_clinicas.index(vals['clinica'])
                clinica = clinicas[idx_c]

                idx_p = nomes_pacientes.index(vals['paciente'])
                paciente = pacientes[idx_p]

                idx_pr = nomes_profissionais.index(vals['profissional'])
                profissional = profissionais[idx_pr]

                data = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                hi = datetime.strptime(vals['hora_inicio'], '%H:%M').time()
                hf = datetime.strptime(vals['hora_fim'], '%H:%M').time()

                tipo = None
                for t in TipoAtendimento:
                    if t.value == vals['tipo']:
                        tipo = t
                        break

                custo = float(vals['custo'])

                self.agendar_atendimento(
                    clinica, paciente, profissional,
                    data, hi, hf, tipo, custo
                )
                self.atendimento_view.mostra_mensagem(
                    'Sucesso', 'Atendimento agendado com sucesso!')
            except (ValueError, IndexError):
                self.atendimento_view.mostra_mensagem(
                    'Erro',
                    'Dados inválidos. Verifique os campos preenchidos.')
            except RegraNegocioException as e:
                self.atendimento_view.mostra_mensagem('Erro', str(e))

    def _alterar_atendimento(self):
        atendimentos = self.context.atendimentos
        if not atendimentos:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Nenhum atendimento agendado.')
            return
        descricoes = self._obter_descricoes_atendimentos(atendimentos)
        idx = self.atendimento_view.mostra_lista_selecao(
            'Selecionar Atendimento para Alterar', descricoes)
        if idx is None:
            return
        at = atendimentos[idx]

        clinicas = self.context.clinicas
        pacientes = self.context.pacientes
        profissionais = self.context.profissionais

        nomes_clinicas = [f"{c.nome} ({c.cidade})" for c in clinicas]
        nomes_pacientes = [f"{p.nome} (CPF: {p.cpf})" for p in pacientes]
        nomes_profissionais = [f"{p.nome} ({p.especialidade.value})" for p in profissionais]
        lista_tipos = [t.value for t in TipoAtendimento]

        dados = {
            'clinica': f"{at.clinica.nome} ({at.clinica.cidade})",
            'paciente': f"{at.paciente.nome} (CPF: {at.paciente.cpf})",
            'profissional': f"{at.profissional.nome} ({at.profissional.especialidade.value})",
            'data': at.data.strftime('%d/%m/%Y'),
            'inicio': at.inicio.strftime('%H:%M'),
            'fim': at.fim.strftime('%H:%M'),
            'tipo': at.tipo.value,
            'custo': f"{at.custo:.2f}"
        }
        botao, vals = self.atendimento_view.tela_formulario(
            nomes_clinicas, nomes_pacientes,
            nomes_profissionais, lista_tipos, dados
        )
        if botao == 'Confirmar':
            try:
                idx_c = nomes_clinicas.index(vals['clinica'])
                clinica = clinicas[idx_c]

                idx_p = nomes_pacientes.index(vals['paciente'])
                paciente = pacientes[idx_p]

                idx_pr = nomes_profissionais.index(vals['profissional'])
                profissional = profissionais[idx_pr]

                data = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                hi = datetime.strptime(vals['hora_inicio'], '%H:%M').time()
                hf = datetime.strptime(vals['hora_fim'], '%H:%M').time()

                tipo = None
                for t in TipoAtendimento:
                    if t.value == vals['tipo']:
                        tipo = t
                        break

                custo = float(vals['custo'])

                self.alterar_atendimento(
                    at, clinica, paciente, profissional,
                    data, hi, hf, tipo, custo
                )
                self.atendimento_view.mostra_mensagem(
                    'Sucesso', 'Atendimento alterado com sucesso!')
            except (ValueError, IndexError):
                self.atendimento_view.mostra_mensagem(
                    'Erro',
                    'Dados inválidos. Verifique os campos preenchidos.')
            except RegraNegocioException as e:
                self.atendimento_view.mostra_mensagem('Erro', str(e))

    def _excluir_atendimento(self):
        atendimentos = self.context.atendimentos
        if not atendimentos:
            self.atendimento_view.mostra_mensagem(
                'Aviso', 'Nenhum atendimento agendado.')
            return
        descricoes = self._obter_descricoes_atendimentos(atendimentos)
        idx = self.atendimento_view.mostra_lista_selecao(
            'Selecionar Atendimento para Excluir', descricoes)
        if idx is None:
            return
        atendimento = atendimentos[idx]
        try:
            self.excluir_atendimento(atendimento)
            self.atendimento_view.mostra_mensagem(
                'Sucesso', 'Atendimento excluído com sucesso!')
        except RegraNegocioException as e:
            self.atendimento_view.mostra_mensagem('Erro', str(e))

    # ================================================================
    #  PROCEDIMENTOS - UI
    # ================================================================
    def abrir_tela_procedimento(self):
        while True:
            botao, valores = self.procedimento_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_procedimentos()
            elif botao == 'Cadastrar':
                self._cadastrar_procedimento()
            elif botao == 'Alterar':
                self._alterar_procedimento()
            elif botao == 'Excluir':
                self._excluir_procedimento()

    def _selecionar_atendimento_para_procedimento(self):
        atendimentos = self.context.atendimentos
        if not atendimentos:
            self.procedimento_view.mostra_mensagem(
                'Aviso', 'Nenhum atendimento cadastrado.')
            return None
        descricoes = self._obter_descricoes_atendimentos(atendimentos)
        idx = self.procedimento_view.tela_selecionar_atendimento(descricoes)
        if idx is None:
            return None
        return atendimentos[idx]

    def _listar_procedimentos(self):
        atendimento = self._selecionar_atendimento_para_procedimento()
        if atendimento is None:
            return
        if not atendimento.procedimentos:
            self.procedimento_view.mostra_mensagem(
                'Aviso',
                'Nenhum procedimento neste atendimento.')
            return
        dados = []
        for proc in atendimento.procedimentos:
            dados.append({
                'descricao': proc.descricao,
                'custo': f"{proc.custo:.2f}",
                'profissional': proc.profissional.nome
            })
        self.procedimento_view.tela_listagem(dados)

    def _cadastrar_procedimento(self):
        atendimento = self._selecionar_atendimento_para_procedimento()
        if atendimento is None:
            return
        if atendimento.pagamento:
            self.procedimento_view.mostra_mensagem(
                'Aviso',
                'Atendimento já possui pagamento. Não é possível '
                'adicionar procedimentos.')
            return
        profissionais = self.context.profissionais
        if not profissionais:
            self.procedimento_view.mostra_mensagem(
                'Aviso', 'Cadastre pelo menos um profissional antes.')
            return

        nomes_prof = [f"{p.nome} ({p.especialidade.value})" for p in profissionais]
        botao, vals = self.procedimento_view.tela_formulario(nomes_prof)
        if botao == 'Confirmar':
            try:
                idx_pr = nomes_prof.index(vals['profissional'])
                responsavel = profissionais[idx_pr]
                custo = float(vals['custo'])
                self.adicionar_procedimento_a_atendimento(
                    atendimento, vals['descricao'], custo, responsavel
                )
                self.procedimento_view.mostra_mensagem(
                    'Sucesso',
                    f"Procedimento adicionado! "
                    f"Custo total: R$ {atendimento.custo:.2f}")
            except (ValueError, IndexError):
                self.procedimento_view.mostra_mensagem(
                    'Erro', 'Dados inválidos.')
            except RegraNegocioException as e:
                self.procedimento_view.mostra_mensagem('Erro', str(e))

    def _alterar_procedimento(self):
        atendimento = self._selecionar_atendimento_para_procedimento()
        if atendimento is None:
            return
        if atendimento.pagamento:
            self.procedimento_view.mostra_mensagem(
                'Aviso',
                'Atendimento já possui pagamento. Não é possível '
                'alterar procedimentos.')
            return
        if not atendimento.procedimentos:
            self.procedimento_view.mostra_mensagem(
                'Aviso', 'Nenhum procedimento neste atendimento.')
            return
        desc_procs = [
            f"{p.descricao} | R$ {p.custo:.2f} | {p.profissional.nome}"
            for p in atendimento.procedimentos
        ]
        idx = self.procedimento_view.mostra_lista_selecao(
            'Selecionar Procedimento para Alterar', desc_procs)
        if idx is None:
            return
        procedimento = atendimento.procedimentos[idx]
        profissionais = self.context.profissionais
        nomes_prof = [f"{p.nome} ({p.especialidade.value})" for p in profissionais]
        dados = {
            'descricao': procedimento.descricao,
            'custo': f"{procedimento.custo:.2f}",
            'profissional': f"{procedimento.profissional.nome} "
                            f"({procedimento.profissional.especialidade.value})"
        }
        botao, vals = self.procedimento_view.tela_formulario(nomes_prof, dados)
        if botao == 'Confirmar':
            try:
                idx_pr = nomes_prof.index(vals['profissional'])
                responsavel = profissionais[idx_pr]
                custo = float(vals['custo'])
                self.alterar_procedimento(
                    atendimento, procedimento,
                    vals['descricao'], custo, responsavel
                )
                self.procedimento_view.mostra_mensagem(
                    'Sucesso',
                    f"Procedimento alterado! "
                    f"Custo total: R$ {atendimento.custo:.2f}")
            except (ValueError, IndexError):
                self.procedimento_view.mostra_mensagem(
                    'Erro', 'Dados inválidos.')
            except RegraNegocioException as e:
                self.procedimento_view.mostra_mensagem('Erro', str(e))

    def _excluir_procedimento(self):
        atendimento = self._selecionar_atendimento_para_procedimento()
        if atendimento is None:
            return
        if atendimento.pagamento:
            self.procedimento_view.mostra_mensagem(
                'Aviso',
                'Atendimento já possui pagamento. Não é possível '
                'excluir procedimentos.')
            return
        if not atendimento.procedimentos:
            self.procedimento_view.mostra_mensagem(
                'Aviso', 'Nenhum procedimento neste atendimento.')
            return
        desc_procs = [
            f"{p.descricao} | R$ {p.custo:.2f} | {p.profissional.nome}"
            for p in atendimento.procedimentos
        ]
        idx = self.procedimento_view.mostra_lista_selecao(
            'Selecionar Procedimento para Excluir', desc_procs)
        if idx is None:
            return
        procedimento = atendimento.procedimentos[idx]
        try:
            self.excluir_procedimento(atendimento, procedimento)
            self.procedimento_view.mostra_mensagem(
                'Sucesso',
                f"Procedimento removido! "
                f"Custo total: R$ {atendimento.custo:.2f}")
        except RegraNegocioException as e:
            self.procedimento_view.mostra_mensagem('Erro', str(e))


    # ================================================================
    #  REGRAS DE NEGÓCIO
    # ================================================================
    def agendar_atendimento(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, 
                            data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float = 0.0) -> Atendimento:
        validar_tipo(clinica, Clinica)
        validar_tipo(paciente, Paciente)
        validar_tipo(profissional, ProfissionalSaude)
        validar_tipo(tipo, TipoAtendimento)

        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18:
            raise RegraNegocioException("Somente pacientes com mais de 18 anos podem realizar atendimentos de forma independente.")

        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("O horário do atendimento está fora do horário de funcionamento da clínica")

        for at in self.context.atendimentos:
            if at.profissional.cpf == profissional.cpf and at.data == data:
                if not (hora_fim <= at.fim or hora_inicio >= at.inicio):
                    raise RegraNegocioException(
                        f"O profissional {profissional.nome} já possui um atendimento agendado "
                        f"das {at.inicio.strftime('%H:%M')} às {at.fim.strftime('%H:%M')} neste dia."
                    )
                    
        atendimento = Atendimento(clinica, paciente, profissional, data, hora_inicio, hora_fim, tipo, custo)
        if self.atendimento_dao.get(atendimento.inicio.isoformat()) is not None:
            raise RegraNegocioException(f"Já existe um atendimento registrado com esse horário de início ({hora_inicio.strftime('%H:%M')}).")

        if atendimento not in self.context.atendimentos: self.context.atendimentos.append(atendimento)
        return atendimento

    def alterar_atendimento(self, atendimento: Atendimento, clinica: Clinica, paciente: Paciente, 
                            profissional: ProfissionalSaude, data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float):
        validar_tipo(clinica, Clinica)
        validar_tipo(paciente, Paciente)
        validar_tipo(profissional, ProfissionalSaude)
        validar_tipo(tipo, TipoAtendimento)

        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18:
            raise RegraNegocioException("Somente pacientes com mais de 18 anos podem realizar atendimentos de forma independente.")

        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("O horário del atendimento está fora do horário de funcionamento da clínica")

        if atendimento.inicio != hora_inicio:
            novo_id = hora_inicio.isoformat()
            if self.atendimento_dao.get(novo_id) is not None:
                raise RegraNegocioException(f"Já existe um atendimento registrado com esse novo horário de início ({hora_inicio.strftime('%H:%M')}).")
            if atendimento in self.context.atendimentos: self.context.atendimentos.remove(atendimento)

        atendimento.clinica = clinica
        atendimento.paciente = paciente
        atendimento.profissional = profissional
        atendimento.data = data
        atendimento.inicio = hora_inicio
        atendimento.fim = hora_fim
        atendimento.tipo = tipo
        atendimento.custo = custo

        if atendimento not in self.context.atendimentos: self.context.atendimentos.append(atendimento)

    def excluir_atendimento(self, atendimento: Atendimento):
        if atendimento in self.context.atendimentos: self.context.atendimentos.remove(atendimento)

    def adicionar_procedimento_a_atendimento(self, atendimento: Atendimento, descricao: str, custo: float, profissional: ProfissionalSaude) -> Procedimento:
        validar_tipo(atendimento, Atendimento)
        validar_tipo(profissional, ProfissionalSaude)
        
        procedimento = Procedimento(descricao, custo, profissional)
        atendimento.adicionar_procedimento(procedimento)
        
        return procedimento

    def alterar_procedimento(self, atendimento: Atendimento, procedimento: Procedimento, descricao: str, custo: float, profissional: ProfissionalSaude):
        validar_tipo(atendimento, Atendimento)
        validar_tipo(profissional, ProfissionalSaude)

        atendimento.custo -= procedimento.custo
        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.profissional = profissional
        atendimento.custo += custo
        
        

    def excluir_procedimento(self, atendimento: Atendimento, procedimento: Procedimento):
        validar_tipo(atendimento, Atendimento)
        if procedimento in atendimento.procedimentos:
            atendimento.custo -= procedimento.custo
            atendimento.procedimentos.remove(procedimento)
            