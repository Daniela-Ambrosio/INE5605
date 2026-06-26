import FreeSimpleGUI as sg
from views.view_base import ViewBase

class ClinicaView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE CLÍNICAS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Cadastrar', size=(25, 1))],
            [sg.Button('Alterar', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Clínicas', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_formulario(self, dados=None):
        if dados is None:
            dados = {'nome': '', 'cidade': '', 'descricao': '', 'hora_abertura': '', 'hora_fechamento': ''}
            titulo = 'CADASTRAR CLÍNICA'
        else:
            titulo = 'ALTERAR CLÍNICA'

        layout = [
            [sg.Text(titulo, font=('Helvetica', 14, 'bold'))],
            [sg.Text('Nome', size=(20, 1)), sg.Input(default_text=dados['nome'], key='nome', size=(30, 1))],
            [sg.Text('Cidade', size=(20, 1)), sg.Input(default_text=dados['cidade'], key='cidade', size=(30, 1))],
            [sg.Text('Descrição', size=(20, 1)), sg.Input(default_text=dados['descricao'], key='descricao', size=(30, 1))],
            [sg.Text('Hora Abertura (HH:MM)', size=(20, 1)), sg.Input(default_text=dados['hora_abertura'], key='hora_abertura', size=(10, 1))],
            [sg.Text('Hora Fechamento (HH:MM)', size=(20, 1)), sg.Input(default_text=dados['hora_fechamento'], key='hora_fechamento', size=(10, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_listagem(self, dados):
        if not dados:
            self.mostra_mensagem('Aviso', 'Nenhuma clínica cadastrada.')
            return
        colunas = ['Nome', 'Cidade', 'Descrição', 'Abertura', 'Fechamento']
        tabela = [
            [d['nome'], d['cidade'], d['descricao'], d['hora_abertura'], d['hora_fechamento']]
            for d in dados
        ]
        layout = [
            [sg.Text('CLÍNICAS CADASTRADAS', font=('Helvetica', 14, 'bold'))],
            [sg.Table(values=tabela, headings=colunas, auto_size_columns=True, justification='left', key='tabela')],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Clínicas', layout)
        window.read()
        window.close()