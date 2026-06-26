import FreeSimpleGUI as sg
from views.view_base import ViewBase

class PacienteView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE PACIENTES', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Cadastrar', size=(25, 1))],
            [sg.Button('Alterar', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Pacientes', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_formulario(self, dados=None):
        if dados is None:
            dados = {'nome': '', 'telefone': '', 'cpf': '', 'data_nascimento': ''}
            titulo = 'CADASTRAR PACIENTE'
        else:
            titulo = 'ALTERAR PACIENTE'

        layout = [
            [sg.Text(titulo, font=('Helvetica', 14, 'bold'))],
            [sg.Text('Nome', size=(20, 1)), sg.Input(default_text=dados['nome'], key='nome', size=(30, 1))],
            [sg.Text('Telefone', size=(20, 1)), sg.Input(default_text=dados['telefone'], key='telefone', size=(30, 1))],
            [sg.Text('CPF', size=(20, 1)), sg.Input(default_text=dados['cpf'], key='cpf', size=(30, 1))],
            [sg.Text('Nascimento (DD/MM/AAAA)', size=(20, 1)), sg.Input(default_text=dados['data_nascimento'], key='data_nascimento', size=(15, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_listagem(self, dados):
        if not dados:
            self.mostra_mensagem('Aviso', 'Nenhum paciente cadastrado.')
            return
        colunas = ['Nome', 'Telefone', 'CPF', 'Nascimento']
        tabela = [
            [d['nome'], d['telefone'], d['cpf'], d['data_nascimento']]
            for d in dados
        ]
        layout = [
            [sg.Text('PACIENTES CADASTRADOS', font=('Helvetica', 14, 'bold'))],
            [sg.Table(values=tabela, headings=colunas, auto_size_columns=True, justification='left', key='tabela')],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Pacientes', layout)
        window.read()
        window.close()
