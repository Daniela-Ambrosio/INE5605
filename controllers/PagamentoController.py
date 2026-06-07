from models import Atendimento, Cartao, PIX, Dinheiro, Pagamento
from datetime import date, time
from .Context import Context, RegraNegocioException
from .validacoes import validar_tipo

class PagamentoController:
    def __init__(self, context: Context):
        self.context = context

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