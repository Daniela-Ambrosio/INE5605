import FreeSimpleGUI as sg

class ProfissionalView:
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
            [sg.Text("-------- PROFISSIONAIS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Cadastrar Profissional", "RD1", key="1")],
            [sg.Radio("Alterar Profissional", "RD1", key="2")],
            [sg.Radio("Listar Profissionais", "RD1", key="3")],
            [sg.Radio("Excluir Profissional", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_profissional(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS PROFISSIONAL ----------", font=("Helvetica", 25))],
            [sg.Text("Nome:", size=(15, 1)), sg.InputText("", key="nome")],
            [sg.Text("Telefone:", size=(15, 1)), sg.InputText("", key="telefone")],
            [sg.Text("CPF:", size=(15, 1)), sg.InputText("", key="cpf")],
            [sg.Text("Registro:", size=(15, 1)), sg.InputText("", key="registro")],
            [sg.Text("Especialidade:", size=(15, 1)), sg.Combo(['Clínico Geral', 'Pediatria', 'Cardiologia', 'Dermatologia', 'Ortopedia', 'Ginecologia'], readonly=True, key="especialidade")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Cadastrar Profissional").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "nome": values["nome"],
                "telefone": values["telefone"],
                "cpf": values["cpf"],
                "registro": values["registro"],
                "especialidade": values["especialidade"]
            }
        self.close()
        return dados

    def mostra_profissional(self, dados_profissional):
        string_todos = ""
        for dado in dados_profissional:
            string_todos += "NOME: " + dado["nome"] + "\n"
            string_todos += "FONE: " + dado["telefone"] + "\n"
            string_todos += "CPF: " + dado["cpf"] + "\n"
            string_todos += "REGISTRO: " + dado["registro"] + "\n"
            string_todos += "ESPECIALIDADE: " + dado["especialidade"] + "\n\n"
        
        if not string_todos:
            string_todos = "Nenhum profissional cadastrado."
        sg.Popup("-------- LISTA DE PROFISSIONAIS ----------", string_todos)

    def seleciona_profissional(self, profissionais):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- SELECIONAR PROFISSIONAL ----------", font=("Helvetica", 25))],
            [sg.Text("Selecione o CPF do profissional:", font=("Helvetica", 15))],
            [sg.Text("CPF:", size=(15, 1)), sg.Combo(profissionais, readonly=True, key="cpf")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Profissional").Layout(layout)
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
