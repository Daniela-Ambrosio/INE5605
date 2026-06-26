import FreeSimpleGUI as sg

class ViewBase:
    def mostra_lista_selecao(self, titulo, lista):
        if not lista:
            self.mostra_mensagem('Aviso', 'Nenhum item disponível.')
            return None
        layout = [
            [sg.Text(titulo, font=('Helvetica', 14))],
            [sg.Listbox(lista, size=(50, min(len(lista), 10)),
                        key='lista',
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        window = sg.Window(titulo, layout)
        botao, valores = window.read()
        window.close()
        if botao == 'Confirmar' and valores['lista']:
            return lista.index(valores['lista'][0])
        return None

    def mostra_mensagem(self, titulo, mensagem):
        sg.popup(mensagem, title=titulo)
