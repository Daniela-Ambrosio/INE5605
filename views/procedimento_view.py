import FreeSimpleGUI as sg
from views.view_base import ViewBase

class ProcedimentoView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE PROCEDIMENTOS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Cadastrar', size=(25, 1))],
            [sg.Button('Alterar', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Procedimentos', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_formulario(self, profissionais, dados=None):
        if dados is None:
            dados = {'descricao': '', 'custo': '', 'profissional': profissionais[0] if profissionais else ''}
            titulo = 'CADASTRAR PROCEDIMENTO'
        else:
            titulo = 'ALTERAR PROCEDIMENTO'

        layout = [
            [sg.Text(titulo, font=('Helvetica', 14, 'bold'))],
            [sg.Text('Descrição', size=(20, 1)), sg.Input(default_text=dados['descricao'], key='descricao', size=(30, 1))],
            [sg.Text('Custo Adicional (R$)', size=(20, 1)), sg.Input(default_text=dados['custo'], key='custo', size=(15, 1))],
            [sg.Text('Profissional Responsável', size=(20, 1)), sg.Combo(profissionais, default_value=dados['profissional'], key='profissional', size=(28, 1), readonly=True)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_listagem(self, dados):
        if not dados:
            self.mostra_mensagem('Aviso', 'Nenhum procedimento cadastrado.')
            return
        colunas = ['Descrição', 'Custo (R$)', 'Profissional']
        tabela = [
            [d['descricao'], d['custo'], d['profissional']]
            for d in dados
        ]
        layout = [
            [sg.Text('PROCEDIMENTOS DO ATENDIMENTO', font=('Helvetica', 14, 'bold'))],
            [sg.Table(values=tabela, headings=colunas, auto_size_columns=True, justification='left', key='tabela')],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Procedimentos', layout)
        window.read()
        window.close()

    def tela_selecionar_atendimento(self, lista):
        return self.mostra_lista_selecao('Selecione o Atendimento', lista)