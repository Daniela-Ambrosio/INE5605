import FreeSimpleGUI as sg

class AtendimentoView:
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
            [sg.Text("-------- ATENDIMENTOS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Cadastrar Atendimento", "RD1", key="1")],
            [sg.Radio("Alterar Atendimento", "RD1", key="2")],
            [sg.Radio("Listar Atendimentos", "RD1", key="3")],
            [sg.Radio("Excluir Atendimento", "RD1", key="4")],
            [sg.Radio("Retornar", "RD1", key="0")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def pega_dados_atendimento(self, clinicas, pacientes, profissionais):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- DADOS ATENDIMENTO ----------", font=("Helvetica", 25))],
            [sg.Text("Nome da Clínica:", size=(20, 1)), sg.Combo(clinicas, readonly=True, key="clinica")],
            [sg.Text("CPF Paciente:", size=(20, 1)), sg.Combo(pacientes, readonly=True, key="paciente")],
            [sg.Text("Nome do Profissional:", size=(20, 1)), sg.Combo(profissionais, readonly=True, key="profissional")],
            [sg.Text("Data (DD/MM/AAAA):", size=(20, 1)), sg.InputText("", key="data")],
            [sg.Text("Hora Início (HH:MM):", size=(20, 1)), sg.InputText("", key="inicio")],
            [sg.Text("Hora Fim (HH:MM):", size=(20, 1)), sg.InputText("", key="fim")],
            [sg.Text("Tipo:", size=(20, 1)), sg.Combo(['Consulta', 'Retorno', 'Exame', 'Procedimento'], readonly=True, key="tipo")],
            [sg.Text("Custo:", size=(20, 1)), sg.InputText("", key="custo")],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Cadastrar Atendimento").Layout(layout)
        button, values = self.open()
        
        dados = None
        if button == "Confirmar":
            dados = {
                "clinica": values["clinica"],
                "paciente": values["paciente"],
                "profissional": values["profissional"],
                "data": values["data"],
                "inicio": values["inicio"],
                "fim": values["fim"],
                "tipo": values["tipo"],
                "custo": values["custo"]
            }
        self.close()
        return dados

    def mostra_atendimento(self, dados_atendimento):
        string_todos = ""
        for dado in dados_atendimento:
            string_todos += "DATA: " + dado["data"] + "\n"
            string_todos += "HORA INÍCIO: " + dado["inicio"] + "\n"
            string_todos += "HORA FIM: " + dado["fim"] + "\n"
            string_todos += "CLÍNICA: " + dado["clinica"] + "\n"
            string_todos += "PACIENTE: " + dado["paciente"] + "\n"
            string_todos += "PROFISSIONAL: " + dado["profissional"] + "\n"
            string_todos += "TIPO: " + dado["tipo"] + "\n"
            string_todos += "CUSTO: R$ " + dado["custo"] + "\n"
            string_todos += "STATUS: " + dado["status"] + "\n\n"
        
        if not string_todos:
            string_todos = "Nenhum atendimento cadastrado."
        sg.Popup("-------- LISTA DE ATENDIMENTOS ----------", string_todos)

    def seleciona_atendimento(self, lista_atendimentos):
        sg.ChangeLookAndFeel("DarkTeal4")
        layout = [
            [sg.Text("-------- SELECIONAR ATENDIMENTO ----------", font=("Helvetica", 25))],
            [sg.Text("Selecione o atendimento:", font=("Helvetica", 15))],
            [sg.Text("Atendimento:", size=(15, 1)), sg.Combo(lista_atendimentos, readonly=True, key="atendimento", size=(40, 1))],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Selecionar Atendimento").Layout(layout)
        button, values = self.open()
        
        escolha = None
        if button == "Confirmar":
            escolha = values["atendimento"]
        self.close()
        return escolha

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
