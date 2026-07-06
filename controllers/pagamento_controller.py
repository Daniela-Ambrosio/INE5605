from datetime import datetime, timedelta, date
from models import PIX, Cartao, Dinheiro
from .validacoes import RegraNegocioException
from views import PagamentoView, AtendimentoView
from DAOs import PagamentoDAO

class PagamentoController:
    def __init__(self):
        self.__pagamento_DAO = PagamentoDAO()
        self.pagamento_view = PagamentoView()
        self.atendimento_view = AtendimentoView()

    def abrir_tela(self):
        while True:
            opcao = self.pagamento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self.tela_realizar_pagamento()
            elif opcao == 2: self.tela_pagar_parcela()
            elif opcao == 3: self.listar_extrato()
            
    def selecionar_atendimento(self):
        lista_atendimentos = [f"{at.data.strftime('%d/%m/%Y')} às {at.inicio.strftime('%H:%M')} - Paciente: {at.paciente.nome}" for at in self.__pagamento_DAO.get_all()]
        if not lista_atendimentos:
            self.pagamento_view.mostra_mensagem("Nenhum atendimento cadastrado.")
            return None
            
        escolha = self.atendimento_view.seleciona_atendimento(lista_atendimentos)
        if escolha:
            for at in self.__pagamento_DAO.get_all():
                string_formatada = f"{at.data.strftime('%d/%m/%Y')} às {at.inicio.strftime('%H:%M')} - Paciente: {at.paciente.nome}"
                if string_formatada == escolha:
                    return at
        return None

    def tela_realizar_pagamento(self):
        at = self.selecionar_atendimento()
        if not at: return
        if at.pagamento:
            self.pagamento_view.mostra_mensagem("Este atendimento já possui pagamento registrado.")
            return

        vals = self.pagamento_view.pega_dados_pagamento()
        if vals:
            try:
                tipo = vals['tipo']
                parcelado = True if vals['parcelado'] == 'Sim' else False
                custo_total = at.custo

                hoje = date.today()

                if tipo == 'Dinheiro':
                    pag = Dinheiro(hoje, custo_total, parcelado)
                elif tipo == 'PIX':
                    if not vals['cpf']: raise ValueError("CPF é obrigatório para PIX.")
                    pag = PIX(hoje, custo_total, parcelado, vals['cpf'])
                elif tipo == 'Cartão':
                    if not vals['numero'] or not vals['bandeira']:
                        raise ValueError("Número e Bandeira são obrigatórios para Cartão.")
                    pag = Cartao(hoje, custo_total, parcelado, int(vals['numero']), vals['bandeira'])
                else:
                    raise ValueError("Tipo de pagamento inválido.")

                if parcelado:
                    if not vals['qtd_parcelas'] or int(vals['qtd_parcelas']) <= 0:
                        raise ValueError("Quantidade de parcelas inválida.")
                    qtd = int(vals['qtd_parcelas'])
                    valor_parcela = custo_total / qtd
                    for i in range(qtd):
                        vencimento = hoje + timedelta(days=30*(i+1))
                        pag.adicionar_parcela(i+1, valor_parcela, vencimento)

                at.pagamento = pag
                self.pagamento_view.mostra_mensagem("Pagamento realizado com sucesso!")
            except Exception as e:
                self.pagamento_view.mostra_mensagem(f"Erro: {e}")

    def tela_pagar_parcela(self):
        at = self.selecionar_atendimento()
        if not at: return
        if not at.pagamento or not at.pagamento.parcelado:
            self.pagamento_view.mostra_mensagem("Atendimento não possui parcelas pendentes.")
            return

        num = self.pagamento_view.seleciona_parcela()
        if num:
            try:
                num = int(num)
                for p in at.pagamento.parcelas:
                    if p.numero == num:
                        if p.paga:
                            self.pagamento_view.mostra_mensagem("Esta parcela já está paga.")
                            return
                        p.paga = True
                        self.pagamento_view.mostra_mensagem(f"Parcela {num} paga com sucesso!")
                        return
                self.pagamento_view.mostra_mensagem("Parcela não encontrada.")
            except ValueError:
                self.pagamento_view.mostra_mensagem("Número inválido.")

    def listar_extrato(self):
        at = self.selecionar_atendimento()
        if not at: return
        
        extrato = f"Atendimento: {at.data.strftime('%d/%m/%Y')} às {at.inicio.strftime('%H:%M')}\n"
        extrato += f"Paciente: {at.paciente.nome}\n"
        extrato += f"Custo Total: R$ {at.custo:.2f}\n\n"
        
        if at.procedimentos:
            extrato += "Procedimentos Realizados:\n"
            for p in at.procedimentos:
                extrato += f"- {p.descricao} (R$ {p.custo:.2f})\n"
            extrato += "\n"

        if at.pagamento:
            extrato += f"Status: PAGO ({at.pagamento.__class__.__name__})\n"
            if at.pagamento.parcelado:
                extrato += "Parcelas:\n"
                for p in at.pagamento.parcelas:
                    status = "Paga" if p.paga else "Pendente"
                    extrato += f"  {p.numero} - R$ {p.custo:.2f} ({status}) venc. {p.vencimento.strftime('%d/%m/%Y')}\n"
                extrato += f"\nTotal Pago: R$ {at.pagamento.obter_valor_pago():.2f}\n"
                extrato += f"Restante: R$ {at.pagamento.obter_valor_restante():.2f}\n"
        else:
            extrato += "Status: PENDENTE\n"

        self.pagamento_view.mostra_pagamento(extrato)

