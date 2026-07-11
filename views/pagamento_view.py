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
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_pagamento(self, valor_total):
        sg.ChangeLookAndFeel("DarkTeal4")
        
        layout_inicial = [
            [sg.Text("-------- REALIZAR PAGAMENTO ----------", font=("Helvetica", 22))],
            [sg.Text(f"Valor do Atendimento: R$ {valor_total:.2f}", font=("Helvetica", 14), text_color="lightgreen")],
            [sg.Text("É parcelado?:", size=(15, 1)), 
             sg.Combo(['Não', 'Sim'], default_value='Não', readonly=True, key="parcelado", enable_events=True)],
            [sg.Text("Tipo:", size=(15, 1)), 
             sg.Combo(['Dinheiro', 'PIX', 'Cartão'], readonly=True, key="tipo")],
            [sg.Button("Avançar", key="Confirmar"), sg.Cancel("Cancelar")]
        ]
        
        self.__window = sg.Window("Realizar Pagamento - Configurações").Layout(layout_inicial)
        
        tipo_escolhido = None
        parcelado_escolhido = None
        
        while True:
            button, values = self.open()
            if button in (None, "Cancelar"):
                self.close()
                return None
                
            if button == "parcelado":
                is_parcelado = values["parcelado"]
                if is_parcelado == 'Sim':
                    self.__window['tipo'].Update(values=['Cartão'], value='Cartão')
                else:
                    self.__window['tipo'].Update(values=['Dinheiro', 'PIX', 'Cartão'], value='')
                    
            if button == "Confirmar":
                if not values["tipo"]:
                    sg.popup("Erro", "Por favor, selecione o tipo de pagamento.")
                    continue
                tipo_escolhido = values["tipo"]
                parcelado_escolhido = values["parcelado"]
                self.close()
                break
                
        dados = {
            "tipo": tipo_escolhido,
            "parcelado": parcelado_escolhido,
            "cpf": "",
            "numero": "",
            "bandeira": "",
            "qtd_parcelas": "1"
        }
        
        if tipo_escolhido == "PIX":
            layout_pix = [
                [sg.Text("-------- PAGAMENTO VIA PIX ----------", font=("Helvetica", 22))],
                [sg.Text(f"Valor a pagar: R$ {valor_total:.2f}", font=("Helvetica", 14))],
                [sg.Text("CPF do pagador:", size=(18, 1)), sg.InputText("", key="cpf")],
                [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
            ]
            self.__window = sg.Window("Dados do PIX").Layout(layout_pix)
            button, values = self.open()
            if button == "Confirmar":
                dados["cpf"] = values["cpf"]
            else:
                self.close()
                return None
            self.close()
            
        elif tipo_escolhido == "Cartão":
            layout_cartao = [
                [sg.Text("-------- PAGAMENTO VIA CARTÃO ----------", font=("Helvetica", 22))],
                [sg.Text(f"Valor total: R$ {valor_total:.2f}", font=("Helvetica", 14))]
            ]
            layout_cartao.append([sg.Text("Número do cartão:", size=(18, 1)), sg.InputText("", key="numero")])
            layout_cartao.append([sg.Text("Bandeira:", size=(18, 1)), sg.InputText("", key="bandeira")])
            
            if parcelado_escolhido == "Sim":
                layout_cartao.append([sg.Text("Quantidade Parcelas:", size=(18, 1)), sg.InputText("", key="qtd_parcelas")])
                
            layout_cartao.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])
            
            self.__window = sg.Window("Dados do Cartão").Layout(layout_cartao)
            button, values = self.open()
            if button == "Confirmar":
                dados["numero"] = values["numero"]
                dados["bandeira"] = values["bandeira"]
                if parcelado_escolhido == "Sim":
                    dados["qtd_parcelas"] = values["qtd_parcelas"]
            else:
                self.close()
                return None
            self.close()
            
        elif tipo_escolhido == "Dinheiro":
            layout_dinheiro = [
                [sg.Text("-------- PAGAMENTO EM DINHEIRO ----------", font=("Helvetica", 22))],
                [sg.Text(f"Confirmar recebimento de R$ {valor_total:.2f} em espécie?", font=("Helvetica", 14))],
                [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
            ]
            self.__window = sg.Window("Confirmar Dinheiro").Layout(layout_dinheiro)
            button, values = self.open()
            self.close()
            if button != "Confirmar":
                return None
                
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
