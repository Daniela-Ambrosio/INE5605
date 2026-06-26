import FreeSimpleGUI as sg
from controllers.controlador_sistema import ControladorSistema

if __name__ == "__main__":
    sg.theme('DarkAmber')
    controlador = ControladorSistema()
    controlador.iniciar()
