import FreeSimpleGUI as sg
from views.view_base import ViewBase

class MenuView(ViewBase):
    def __init__(self):
        self.__window = None
        self.init_components()

    def init_components(self):
        if self.__window is not None:
            self.__window.close()
            
        layout = [
            [sg.Text('SISTEMA CLÍNICO', font=('Helvetica', 18, 'bold'), justification='center')],
            [sg.Text('─' * 45)],
            [sg.Button('Clínicas', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Pacientes', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Profissionais', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Atendimentos', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Procedimentos', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Pagamentos', size=(25, 2), font=('Helvetica', 12))],
            [sg.Button('Relatórios', size=(25, 2), font=('Helvetica', 12))],
            [sg.Text('─' * 45)],
            [sg.Button('Sair', size=(15, 1), button_color=('white', 'red'))]
        ]
        
        self.__window = sg.Window('Menu Principal', layout, element_justification='center', size=(400, 600))

    def open(self):
        self.init_components()
        botao, valores = self.__window.read()
        self.__window.close()
        return botao, valores
