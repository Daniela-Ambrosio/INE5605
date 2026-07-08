import FreeSimpleGUI as sg

class PacienteView:
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
            [sg.Text("-------- PACIENTES ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Cadastrar Paciente", "RD1", key="1")],
            [sg.Radio("Alterar Paciente", "RD1", key="2")],
            [sg.Radio("Listar Pacientes", "RD1", key="3")],
            [sg.Radio("Excluir Paciente", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_paciente(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS PACIENTE ----------", font=("Helvetica", 25))],
            [sg.Text("Nome:", size=(15, 1)), sg.InputText("", key="nome")],
            [sg.Text("Telefone:", size=(15, 1)), sg.InputText("", key="telefone")],
            [sg.Text("CPF:", size=(15, 1)), sg.InputText("", key="cpf")],
            [sg.Text("Nascimento (DD/MM/AAAA):", size=(25, 1)), sg.InputText("", key="nascimento")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Cadastrar Paciente").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "nome": values["nome"],
                "telefone": values["telefone"],
                "cpf": values["cpf"],
                "data_nascimento": values["nascimento"]
            }
        self.close()
        return dados

    def mostra_paciente(self, dados_paciente):
        string_todos = ""
        for dado in dados_paciente:
            string_todos += "NOME: " + dado["nome"] + "\n"
            string_todos += "FONE: " + dado["telefone"] + "\n"
            string_todos += "CPF: " + dado["cpf"] + "\n\n"
        
        if not string_todos:
            string_todos = "Nenhum paciente cadastrado."
        sg.Popup("-------- LISTA DE PACIENTES ----------", string_todos)

    def seleciona_paciente(self, pacientes):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- SELECIONAR PACIENTE ----------", font=("Helvetica", 25))],
            [sg.Text("Selecione o CPF do paciente:", font=("Helvetica", 15))],
            [sg.Text("CPF:", size=(15, 1)), sg.Combo(pacientes, readonly=True, key="cpf")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Paciente").Layout(layout)
        button, values = self.open()
        
        cpf = None
        if button == "Confirmar":
            cpf = values["cpf"]
        self.close()
        return cpf

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
