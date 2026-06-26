import FreeSimpleGUI as sg
from views.view_base import ViewBase

class PagamentoView(ViewBase):
    def open(self):
        layout = [
            [sg.Text('GERENCIAMENTO DE PAGAMENTOS', font=('Helvetica', 16, 'bold'))],
            [sg.Text('─' * 40)],
            [sg.Button('Listar', size=(25, 1))],
            [sg.Button('Registrar', size=(25, 1))],
            [sg.Button('Quitar Parcela', size=(25, 1))],
            [sg.Button('Excluir', size=(25, 1))],
            [sg.Text('─' * 40)],
            [sg.Button('Voltar', size=(25, 1))]
        ]
        window = sg.Window('Pagamentos', layout, element_justification='center')
        botao, valores = window.read()
        window.close()
        return botao, valores

    def tela_selecionar_atendimento(self, descricoes):
        return self.mostra_lista_selecao('Selecionar Atendimento', descricoes)

    def tela_registrar(self, custo_total):
        layout = [
            [sg.Text('REGISTRAR PAGAMENTO', font=('Helvetica', 14, 'bold'))],
            [sg.Text(f'Custo Total do Atendimento: R$ {custo_total:.2f}', font=('Helvetica', 11))],
            [sg.Text('─' * 45)],
            [sg.Text('Data (DD/MM/AAAA)', size=(22, 1)), sg.Input(key='data', size=(15, 1))],
            [sg.Text('Modalidade', size=(22, 1)), sg.Combo(['Dinheiro', 'PIX', 'Cartão de Crédito'], key='modalidade', readonly=True, size=(20, 1), enable_events=True)],
            [sg.pin(sg.Column([[sg.Text('─' * 45)], [sg.Text('Valor (R$)', size=(22, 1)), sg.Input(key='valor', size=(15, 1))]], key='-COL_DINHEIRO-', visible=False, pad=(0, 0)))],
            [sg.pin(sg.Column([[sg.Text('─' * 45)], [sg.Text('Valor (R$)', size=(22, 1)), sg.Input(key='valor_pix', size=(15, 1))], [sg.Text('CPF Pagador', size=(22, 1)), sg.Input(key='cpf_pagador', size=(15, 1))]], key='-COL_PIX-', visible=False, pad=(0, 0)))],
            [sg.pin(sg.Column([[sg.Text('─' * 45)], [sg.Text('Nº Cartão', size=(22, 1)), sg.Input(key='num_cartao', size=(20, 1))], [sg.Text('Bandeira', size=(22, 1)), sg.Input(key='bandeira', size=(15, 1))], [sg.Text('Qtd. Parcelas', size=(22, 1)), sg.Input(key='qtd_parcelas', size=(5, 1))]], key='-COL_CARTAO-', visible=False, pad=(0, 0)))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window('Registrar Pagamento', layout)
        botao, valores = None, None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                botao = 'Cancelar'
                valores = values
                break
            if event == 'Confirmar':
                botao = 'Confirmar'
                if values and values.get('modalidade') == 'PIX':
                    values['valor'] = values.get('valor_pix')
                    values['cpf'] = values.get('cpf_pagador')
                elif values and values.get('modalidade') == 'Cartão de Crédito':
                    values['numero_cartao'] = values.get('num_cartao')
                valores = values
                break
            if event == 'modalidade':
                mod = values['modalidade']
                window['-COL_DINHEIRO-'].update(visible=(mod == 'Dinheiro'))
                window['-COL_PIX-'].update(visible=(mod == 'PIX'))
                window['-COL_CARTAO-'].update(visible=(mod == 'Cartão de Crédito'))
        window.close()
        return botao, valores

    def tela_listagem(self, tipo, parcelas_dados):
        layout = [
            [sg.Text(f'PAGAMENTO - {tipo.upper()}', font=('Helvetica', 14, 'bold'))],
            [sg.Listbox(parcelas_dados, size=(60, min(len(parcelas_dados), 10)), key='lista', disabled=True)],
            [sg.Button('Voltar')]
        ]
        window = sg.Window('Listagem de Pagamento', layout)
        window.read()
        window.close()

    def tela_quitar_parcela(self, parcelas_texto):
        return self.mostra_lista_selecao('Quitar Parcela', parcelas_texto)