from views.relatorio_view import RelatorioView

class RelatoriosController:
    def __init__(self, context):
        self.__context = context
        self.__relatorio_view = RelatorioView()

    def abrir_tela(self):
        while True:
            opcao = self.__relatorio_view.tela_opcoes()
            if opcao == 0: break
            else: self.__relatorio_view.mostra_mensagem("Em desenvolvimento...")
