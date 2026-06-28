import FreeSimpleGUI as sg

class ClinicaView:
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
            [sg.Text("-------- CLÍNICAS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Cadastrar Clínica", "RD1", key="1")],
            [sg.Radio("Alterar Clínica", "RD1", key="2")],
            [sg.Radio("Listar Clínicas", "RD1", key="3")],
            [sg.Radio("Excluir Clínica", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_clinica(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS CLÍNICA ----------", font=("Helvetica", 25))],
            [sg.Text("Nome:", size=(15, 1)), sg.InputText("", key="nome")],
            [sg.Text("Cidade:", size=(15, 1)), sg.InputText("", key="cidade")],
            [sg.Text("Descrição:", size=(15, 1)), sg.InputText("", key="descricao")],
            [sg.Text("Abertura (HH:MM):", size=(15, 1)), sg.InputText("", key="hora_abertura")],
            [sg.Text("Fechamento (HH:MM):", size=(15, 1)), sg.InputText("", key="hora_fechamento")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Cadastrar Clínica").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "nome": values["nome"],
                "cidade": values["cidade"],
                "descricao": values["descricao"],
                "hora_abertura": values["hora_abertura"],
                "hora_fechamento": values["hora_fechamento"]
            }
        self.close()
        return dados

    def mostra_clinica(self, dados_clinica):
        string_todos = ""
        for dado in dados_clinica:
            string_todos += "NOME: " + dado["nome"] + "\n"
            string_todos += "CIDADE: " + dado["cidade"] + "\n"
            string_todos += "ABERTURA: " + dado["hora_abertura"] + "\n"
            string_todos += "FECHAMENTO: " + dado["hora_fechamento"] + "\n\n"
        
        if not string_todos:
            string_todos = "Nenhuma clínica cadastrada."
        sg.Popup("-------- LISTA DE CLÍNICAS ----------", string_todos)

    def seleciona_clinica(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- SELECIONAR CLÍNICA ----------", font=("Helvetica", 25))],
            [sg.Text("Digite o Nome da clínica que deseja selecionar:", font=("Helvetica", 15))],
            [sg.Text("Nome:", size=(15, 1)), sg.InputText("", key="nome")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Clínica").Layout(layout)
        button, values = self.open()
        
        nome = None
        if button == "Confirmar":
            nome = values["nome"]
        self.close()
        return nome

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
