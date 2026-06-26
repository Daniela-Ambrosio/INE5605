from models import Atendimento, Cartao, PIX, Dinheiro, Pagamento
from datetime import date, time, datetime
from .validacoes import validar_tipo, RegraNegocioException
from .context import Context
from views.pagamento_view import PagamentoView

class PagamentoController:
    def __init__(self, context):
        self.context = context
        self.pagamento_view = PagamentoView()

    # ================================================================
    #  PAGAMENTOS - UI
    # ================================================================
    def abrir_tela(self):
        while True:
            botao, valores = self.pagamento_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_pagamento()
            elif botao == 'Registrar':
                self._registrar_pagamento()
            elif botao == 'Quitar Parcela':
                self._quitar_parcela()
            elif botao == 'Excluir':
                self._excluir_pagamento()

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

    def _selecionar_atendimento_para_pagamento(self):
        atendimentos = self.context.atendimentos
        if not atendimentos:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Nenhum atendimento cadastrado.')
            return None
        descricoes = self._obter_descricoes_atendimentos(atendimentos)
        idx = self.pagamento_view.tela_selecionar_atendimento(descricoes)
        if idx is None:
            return None
        return atendimentos[idx]

    def _listar_pagamento(self):
        atendimento = self._selecionar_atendimento_para_pagamento()
        if atendimento is None:
            return
        if not atendimento.pagamento:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Nenhum pagamento registrado para este atendimento.')
            return
        pag = atendimento.pagamento
        tipo = pag.__class__.__name__
        parcelas_dados = []
        for p in pag.parcelas:
            status = 'Paga' if p.paga else 'Pendente'
            parcelas_dados.append(
                f"Parcela {p.numero} - R$ {p.custo:.2f} - "
                f"Venc: {p.vencimento.strftime('%d/%m/%Y')} - Status: {status}"
            )
        self.pagamento_view.tela_listagem(tipo, parcelas_dados)

    def _registrar_pagamento(self):
        atendimento = self._selecionar_atendimento_para_pagamento()
        if atendimento is None:
            return
        if atendimento.pagamento:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Este atendimento já possui pagamento registrado.')
            return

        botao, vals = self.pagamento_view.tela_registrar(atendimento.custo)
        if botao == 'Confirmar':
            try:
                mod = vals['modalidade']
                dt = datetime.strptime(
                    vals['data_pagamento'], '%d/%m/%Y').date()

                if mod == 'Dinheiro':
                    valor = float(vals.get('valor', 0))
                    self.registrar_pagamento_dinheiro(atendimento, dt, valor)

                elif mod == 'PIX':
                    valor = float(vals.get('valor', 0))
                    cpf = vals.get('cpf', '')
                    if not cpf:
                        raise RegraNegocioException("CPF é obrigatório para PIX.")
                    self.registrar_pagamento_pix(atendimento, dt, valor, cpf)

                elif mod == 'Cartão de Crédito':
                    num = int(vals.get('numero_cartao', 0))
                    bandeira = vals.get('bandeira', '')
                    qtd = int(vals.get('qtd_parcelas', 1))
                    if not bandeira:
                        raise RegraNegocioException(
                            "Bandeira é obrigatória para Cartão.")
                    self.registrar_pagamento_cartao_parcelado(
                        atendimento, dt, num, bandeira, qtd
                    )

                self.pagamento_view.mostra_mensagem(
                    'Sucesso', 'Pagamento registrado com sucesso!')
            except ValueError:
                self.pagamento_view.mostra_mensagem(
                    'Erro', 'Dados numéricos ou de data inválidos.')
            except RegraNegocioException as e:
                self.pagamento_view.mostra_mensagem('Erro', str(e))

    def _quitar_parcela(self):
        atendimento = self._selecionar_atendimento_para_pagamento()
        if atendimento is None:
            return
        if not atendimento.pagamento:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Nenhum pagamento registrado para este atendimento.')
            return
        pag = atendimento.pagamento
        parcelas_desc = []
        for p in pag.parcelas:
            status = 'Paga' if p.paga else 'Pendente'
            parcelas_desc.append(
                f"Parcela {p.numero} - R$ {p.custo:.2f} ({status})"
            )
        idx = self.pagamento_view.mostra_lista_selecao(
            'Selecione a Parcela para Quitar', parcelas_desc)
        if idx is None:
            return
        parcela = pag.parcelas[idx]
        if parcela.paga:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Esta parcela já está paga.')
            return
        try:
            self.quitar_parcela(atendimento, parcela.numero)
            self.pagamento_view.mostra_mensagem(
                'Sucesso', 'Parcela quitada com sucesso!')
        except RegraNegocioException as e:
            self.pagamento_view.mostra_mensagem('Erro', str(e))

    def _excluir_pagamento(self):
        atendimento = self._selecionar_atendimento_para_pagamento()
        if atendimento is None:
            return
        if not atendimento.pagamento:
            self.pagamento_view.mostra_mensagem(
                'Aviso', 'Nenhum pagamento registrado para este atendimento.')
            return
        try:
            self.excluir_pagamento(atendimento)
            self.pagamento_view.mostra_mensagem(
                'Sucesso', 'Pagamento excluído com sucesso!')
        except RegraNegocioException as e:
            self.pagamento_view.mostra_mensagem('Erro', str(e))


    # ================================================================
    #  REGRAS DE NEGÓCIO
    # ================================================================
    def registrar_pagamento_pix(self, atendimento: Atendimento, data_pagamento: date, valor: float, cpf_pagador: str) -> PIX:
        validar_tipo(atendimento, Atendimento)
        
        if data_pagamento > atendimento.data:
            raise RegraNegocioException("Data do pagamento não pode ser posterior à data do atendimento")

        pagamento = PIX(data_pagamento, atendimento.custo, parcelado=False, cpf=cpf_pagador)
        pagamento.adicionar_parcela(numero=1, custo=valor, vencimento=data_pagamento, paga=True)
        atendimento.registrar_pagamento(pagamento)
        
        
        return pagamento

    def registrar_pagamento_dinheiro(self, atendimento: Atendimento, data_pagamento: date, valor: float) -> Dinheiro:
        validar_tipo(atendimento, Atendimento)
        
        if data_pagamento > atendimento.data:
            raise RegraNegocioException("Data do pagamento não pode ser posterior à data do atendimento")

        pagamento = Dinheiro(data_pagamento, atendimento.custo, parcelado=False)
        pagamento.adicionar_parcela(numero=1, custo=valor, vencimento=data_pagamento, paga=True)
        atendimento.registrar_pagamento(pagamento)
        
        
        return pagamento

    def registrar_pagamento_cartao_parcelado(self, atendimento: Atendimento, data_pagamento: date, 
                                             numero_cartao: int, bandeira: str, qtd_parcelas: int) -> Cartao:
        validar_tipo(atendimento, Atendimento)
        
        if data_pagamento > atendimento.data:
            raise RegraNegocioException("Data do pagamento não pode ser posterior à data do atendimento")
        
        if qtd_parcelas <= 0:
            raise RegraNegocioException("A quantidade de parcelas deve ser pelo menos 1.")

        custo_parcela = round(atendimento.custo / qtd_parcelas, 2)
        pagamento = Cartao(data_pagamento, atendimento.custo, parcelado=(qtd_parcelas > 1), numero=numero_cartao, bandeira=bandeira)

        for i in range(1, qtd_parcelas + 1):
            if data_pagamento > atendimento.data:
                raise RegraNegocioException("Os pagamentos devem ser realizados até a data do atendimento.")
            
            pagamento.adicionar_parcela(numero=i, custo=custo_parcela, vencimento=data_pagamento, paga=False)

        atendimento.registrar_pagamento(pagamento)
        
        
        return pagamento

    def excluir_pagamento(self, atendimento: Atendimento):
        validar_tipo(atendimento, Atendimento)
        if atendimento.pagamento is None:
            raise RegraNegocioException("Este atendimento não possui pagamentos registrados.")
        
        atendimento.pagamento = None
        atendimento.parcelado = False
        
        

    def quitar_parcela(self, atendimento: Atendimento, numero_parcela: int):
        validar_tipo(atendimento, Atendimento)
        
        if atendimento.pagamento is None:
            raise RegraNegocioException("Este atendimento não possui pagamentos registrados.")
        
        pagamento = atendimento.pagamento
        
        if not pagamento.parcelado:
            for parc in pagamento.parcelas:
                if parc.numero == 1:
                    parc.paga = True
                    
                    return
        
        for parc in pagamento.parcelas:
            if parc.numero == numero_parcela:
                if parc.paga:
                    raise RegraNegocioException(f"A parcela {numero_parcela} já está paga.")
                parc.paga = True
                
                return

        raise RegraNegocioException(f"Parcela número {numero_parcela} não encontrada.")