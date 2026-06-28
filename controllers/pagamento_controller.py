from datetime import datetime
from models import PIX, Cartao, Dinheiro
from .validacoes import RegraNegocioException
from views.pagamento_view import PagamentoView

class PagamentoController:
    def __init__(self, context):
        self.__context = context
        self.__pagamento_view = PagamentoView()

    def abrir_tela(self):
        while True:
            opcao = self.__pagamento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._realizar_pagamento()
            elif opcao == 2: self._pagar_parcela()
            elif opcao == 3: self._listar_extrato()
            elif opcao == 4: self._estornar_pagamento()

    def _realizar_pagamento(self):
        # Simplificado para o padrao
        self.__pagamento_view.mostra_mensagem("Em desenvolvimento...")

    def _pagar_parcela(self):
        self.__pagamento_view.mostra_mensagem("Em desenvolvimento...")

    def _listar_extrato(self):
        self.__pagamento_view.mostra_mensagem("Em desenvolvimento...")

    def _estornar_pagamento(self):
        self.__pagamento_view.mostra_mensagem("Em desenvolvimento...")
