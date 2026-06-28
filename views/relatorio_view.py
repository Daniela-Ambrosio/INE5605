import FreeSimpleGUI as sg

class RelatorioView:
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
            [sg.Text("-------- RELATÓRIOS ----------", font=("Helvetica", 25))],
            [sg.Text("Escolha sua opção", font=("Helvetica", 15))],
            [sg.Radio("Listar Atendimentos da Clínica", "RD1", key="1")],
            [sg.Radio("Listar Atendimentos do Paciente", "RD1", key="2")],
            [sg.Radio("Listar Atendimentos do Profissional", "RD1", key="3")],
            [sg.Radio("Retornar", "RD1", key="0")],
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
