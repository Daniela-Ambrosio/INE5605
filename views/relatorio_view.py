import FreeSimpleGUI as sg
from views.view_base import ViewBase

class RelatorioView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE RELATÓRIOS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 45)],
            [sg.Button('Relatório 1', size=(25, 1)), sg.Text('Clínicas com mais atendimentos')],
            [sg.Button('Relatório 2', size=(25, 1)), sg.Text('Procedimentos mais realizados')],
            [sg.Button('Relatório 3', size=(25, 1)), sg.Text('Atendimentos mais caros e baratos')],
            [sg.Button('Relatório 4', size=(25, 1)), sg.Text('Procedimentos mais caros e baratos')],
            [sg.Text('─' * 45)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Relatórios', layout, element_justification='left')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def mostra_relatorio(self, texto):
        layout = [
            [sg.Text('RESULTADO DO RELATÓRIO', font=('Helvetica', 14, 'bold'))],
            [sg.Multiline(texto, size=(60, 20), disabled=True, font=('Courier', 10))],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Relatório', layout)
        window.read()
        window.close()
