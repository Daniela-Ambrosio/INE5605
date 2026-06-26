import FreeSimpleGUI as sg
from views.view_base import ViewBase

class AtendimentoView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE ATENDIMENTOS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Cadastrar', size=(25, 1))],
            [sg.Button('Alterar', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Atendimentos', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_formulario(self, clinicas, pacientes, profissionais, tipos, dados=None):
        if dados is None:
            dados = {'clinica': clinicas[0] if clinicas else '',
                     'paciente': pacientes[0] if pacientes else '',
                     'profissional': profissionais[0] if profissionais else '',
                     'data': '', 'inicio': '', 'fim': '',
                     'tipo': tipos[0] if tipos else '', 'custo': ''}
            titulo = 'CADASTRAR ATENDIMENTO'
        else:
            titulo = 'ALTERAR ATENDIMENTO'

        layout = [
            [sg.Text(titulo, font=('Helvetica', 14, 'bold'))],
            [sg.Text('Clínica', size=(20, 1)), sg.Combo(clinicas, default_value=dados['clinica'], key='clinica', size=(28, 1), readonly=True)],
            [sg.Text('Paciente', size=(20, 1)), sg.Combo(pacientes, default_value=dados['paciente'], key='paciente', size=(28, 1), readonly=True)],
            [sg.Text('Profissional', size=(20, 1)), sg.Combo(profissionais, default_value=dados['profissional'], key='profissional', size=(28, 1), readonly=True)],
            [sg.Text('Data (DD/MM/AAAA)', size=(20, 1)), sg.Input(default_text=dados['data'], key='data', size=(15, 1))],
            [sg.Text('Hora Início (HH:MM)', size=(20, 1)), sg.Input(default_text=dados['inicio'], key='hora_inicio', size=(10, 1))],
            [sg.Text('Hora Fim (HH:MM)', size=(20, 1)), sg.Input(default_text=dados['fim'], key='hora_fim', size=(10, 1))],
            [sg.Text('Tipo', size=(20, 1)), sg.Combo(tipos, default_value=dados['tipo'], key='tipo', size=(15, 1), readonly=True)],
            [sg.Text('Custo (R$)', size=(20, 1)), sg.Input(default_text=dados['custo'], key='custo', size=(15, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_listagem(self, dados):
        if not dados:
            self.mostra_mensagem('Aviso', 'Nenhum atendimento agendado.')
            return
        colunas = ['Data', 'Início', 'Fim', 'Clínica', 'Paciente', 'Profissional', 'Tipo', 'Custo', 'Status']
        tabela = [
            [d['data'], d['inicio'], d['fim'], d['clinica'], d['paciente'],
             d['profissional'], d['tipo'], d['custo'], d['status']]
            for d in dados
        ]
        layout = [
            [sg.Text('ATENDIMENTOS CADASTRADOS', font=('Helvetica', 14, 'bold'))],
            [sg.Table(values=tabela, headings=colunas, auto_size_columns=True, justification='left', key='tabela')],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Atendimentos', layout)
        window.read()
        window.close()