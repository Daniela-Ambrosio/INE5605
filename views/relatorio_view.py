import FreeSimpleGUI as sg

class RelatorioView:
    def __init__(self):
        self.__window = None

    def tela_opcoes(self):
        self.init_opcoes()
        button, values = self.open()
        opcao = 0
        if values and button == "Confirmar":
            escolha = values.get("opcao")
            if escolha == "Listar Atendimentos da Clínica":
                opcao = 1
            elif escolha == "Listar Atendimentos do Paciente":
                opcao = 2
            elif escolha == "Listar Atendimentos do Profissional":
                opcao = 3
            elif escolha == "Retornar":
                opcao = 0
        elif button in (None, "Cancelar"):
            opcao = 0
        self.close()
        return opcao

    def init_opcoes(self):
        sg.ChangeLookAndFeel("DarkTeal4")
        opcoes = [
            "Listar Atendimentos da Clínica",
            "Listar Atendimentos do Paciente",
            "Listar Atendimentos do Profissional",
            "Retornar"
        ]
        layout = [
            [sg.Text("-------- RELATÓRIOS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Combo(opcoes, default_value="Listar Atendimentos da Clínica", readonly=True, key="opcao", size=(35, 1))],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")]
        ]
        self.__window = sg.Window("Sistema de Clínica Médica").Layout(layout)

    def mostra_mensagem(self, msg):
        sg.popup("", msg)

    def close(self):
        if self.__window: self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
