import FreeSimpleGUI as sg

class PagamentoView:
    def __init__(self):
        self.__window = None

    def tela_opcoes(self):
        self.init_opcoes()
        button, values = self.open()
        opcao = 0
        if values:
            if values.get("1"): opcao = 1
            if values.get("2"): opcao = 2
            if values.get("3"): opcao = 3
            if values.get("4"): opcao = 4
            if values.get("0") or button in (None, "Cancelar"): opcao = 0
        self.close()
        return opcao

    def init_opcoes(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- PAGAMENTOS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Realizar Pagamento de Atendimento", "RD1", key="1")],
            [sg.Radio("Pagar Parcela Pendente", "RD1", key="2")],
            [sg.Radio("Listar Extrato do Atendimento", "RD1", key="3")],
            [sg.Radio("Estornar Pagamento (Excluir)", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_pagamento(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS PAGAMENTO ----------", font=("Helvetica", 25))],
            [sg.Text("Tipo (Dinheiro/PIX/Cartao):", size=(20, 1)), sg.InputText("", key="tipo")],
            [sg.Text("É parcelado? (S/N):", size=(20, 1)), sg.InputText("", key="parcelado")],
            [sg.Text("--- Só PIX ---", font=("Helvetica", 12))],
            [sg.Text("CPF do pagador:", size=(20, 1)), sg.InputText("", key="cpf")],
            [sg.Text("--- Só Cartão ---", font=("Helvetica", 12))],
            [sg.Text("Número do cartão:", size=(20, 1)), sg.InputText("", key="numero")],
            [sg.Text("Bandeira:", size=(20, 1)), sg.InputText("", key="bandeira")],
            [sg.Text("Quantidade Parcelas:", size=(20, 1)), sg.InputText("", key="qtd_parcelas")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Realizar Pagamento").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "tipo": values["tipo"],
                "parcelado": values["parcelado"],
                "cpf": values["cpf"],
                "numero": values["numero"],
                "bandeira": values["bandeira"],
                "qtd_parcelas": values["qtd_parcelas"]
            }
        self.close()
        return dados

    def mostra_pagamento(self, string_extrato):
        sg.Popup("-------- EXTRATO DO ATENDIMENTO ----------", string_extrato)

    def seleciona_parcela(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- PAGAR PARCELA ----------", font=("Helvetica", 25))],
            [sg.Text("Digite o número da parcela que deseja pagar:", font=("Helvetica", 15))],
            [sg.Text("Número:", size=(15, 1)), sg.InputText("", key="numero")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Parcela").Layout(layout)
        button, values = self.open()
        
        numero = None
        if button == "Confirmar":
            numero = values["numero"]
        self.close()
        return numero

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
