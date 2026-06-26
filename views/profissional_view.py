import FreeSimpleGUI as sg
from views.view_base import ViewBase

class ProfissionalView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE PROFISSIONAIS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Cadastrar', size=(25, 1))],
            [sg.Button('Alterar', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Profissionais', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_formulario(self, lista_especialidades, dados=None):
        if dados is None:
            dados = {'nome': '', 'telefone': '', 'cpf': '', 'especialidade': lista_especialidades[0] if lista_especialidades else '', 'registro': ''}
            titulo = 'CADASTRAR PROFISSIONAL'
        else:
            titulo = 'ALTERAR PROFISSIONAL'

        layout = [
            [sg.Text(titulo, font=('Helvetica', 14, 'bold'))],
            [sg.Text('Nome', size=(20, 1)), sg.Input(default_text=dados['nome'], key='nome', size=(30, 1))],
            [sg.Text('Telefone', size=(20, 1)), sg.Input(default_text=dados['telefone'], key='telefone', size=(30, 1))],
            [sg.Text('CPF', size=(20, 1)), sg.Input(default_text=dados['cpf'], key='cpf', size=(30, 1))],
            [sg.Text('Especialidade', size=(20, 1)), sg.Combo(lista_especialidades, default_value=dados['especialidade'], key='especialidade', size=(28, 1), readonly=True)],
            [sg.Text('Registro CRM', size=(20, 1)), sg.Input(default_text=dados['registro'], key='registro', size=(15, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_listagem(self, dados):
        if not dados:
            self.mostra_mensagem('Aviso', 'Nenhum profissional cadastrado.')
            return
        colunas = ['Nome', 'Telefone', 'Especialidade', 'Registro']
        tabela = [
            [d['nome'], d['telefone'], d['especialidade'], d['registro']]
            for d in dados
        ]
        layout = [
            [sg.Text('PROFISSIONAIS CADASTRADOS', font=('Helvetica', 14, 'bold'))],
            [sg.Table(values=tabela, headings=colunas, auto_size_columns=True, justification='left', key='tabela')],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Profissionais', layout)
        window.read()
        window.close()