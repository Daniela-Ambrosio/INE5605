import FreeSimpleGUI as sg

class ProcedimentoView:
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
            [sg.Text("-------- PROCEDIMENTOS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Cadastrar Procedimento", "RD1", key="1")],
            [sg.Radio("Alterar Procedimento", "RD1", key="2")],
            [sg.Radio("Listar Procedimentos", "RD1", key="3")],
            [sg.Radio("Excluir Procedimento", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_procedimento(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS PROCEDIMENTO ----------", font=("Helvetica", 25))],
            [sg.Text("Descrição:", size=(20, 1)), sg.InputText("", key="descricao")],
            [sg.Text("Nome do Profissional:", size=(20, 1)), sg.InputText("", key="profissional")],
            [sg.Text("Custo:", size=(20, 1)), sg.InputText("", key="custo")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Cadastrar Procedimento").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "descricao": values["descricao"],
                "profissional": values["profissional"],
                "custo": values["custo"]
            }
        self.close()
        return dados

    def mostra_procedimento(self, dados_procedimentos):
        string_todos = ""
        for dado in dados_procedimentos:
            string_todos += "DESCRIÇÃO: " + dado["descricao"] + "\n"
            string_todos += "PROFISSIONAL: " + dado["profissional"] + "\n"
            string_todos += "CUSTO: R$ " + dado["custo"] + "\n\n"
        
        if not string_todos:
            string_todos = "Nenhum procedimento cadastrado."
        sg.Popup("-------- LISTA DE PROCEDIMENTOS ----------", string_todos)

    def seleciona_procedimento(self, descricoes):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- SELECIONAR PROCEDIMENTO ----------", font=("Helvetica", 25))],
            [sg.Text("Selecione a descrição do procedimento:", font=("Helvetica", 15))],
            [sg.Text("Descrição:", size=(15, 1)), sg.Combo(descricoes, readonly=True, key="descricao")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Procedimento").Layout(layout)
        button, values = self.open()
        
        descricao = None
        if button == "Confirmar":
            descricao = values["descricao"]
        self.close()
        return descricao

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
