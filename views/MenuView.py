import sys
from controllers.Context import Context

class MenuView:
    def __init__(self, context, clinica_view, paciente_view, profissional_view, atendimento_view, procedimento_view, pagamento_view, relatorio_view):
        self.context = context
        self.clinica_view = clinica_view
        self.paciente_view = paciente_view
        self.profissional_view = profissional_view
        self.atendimento_view = atendimento_view
        self.procedimento_view = procedimento_view
        self.pagamento_view = pagamento_view
        self.relatorio_view = relatorio_view

    def exibir_menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("       SISTEMA DE GERENCIAMENTO DE CLÍNICAS      ")
            print("="*50)
            print("1. Gerenciar Clínicas")
            print("2. Gerenciar Pacientes")
            print("3. Gerenciar Profissionais de Saúde")
            print("4. Gerenciar Atendimentos (Agendamentos)")
            print("5. Gerenciar Procedimentos")
            print("6. Gerenciar Pagamentos")
            print("7. Relatórios e Estatísticas")
            print("0. Sair")
            print("="*50)
            
            opcao = input("Selecione uma opção: ").strip()
            
            if opcao == "1":
                self.clinica_view.exibir_menu()
            elif opcao == "2":
                self.paciente_view.exibir_menu()
            elif opcao == "3":
                self.profissional_view.exibir_menu()
            elif opcao == "4":
                self.atendimento_view.exibir_menu()
            elif opcao == "5":
                self.procedimento_view.exibir_menu()
            elif opcao == "6":
                self.pagamento_view.exibir_menu()
            elif opcao == "7":
                self.submenu_relatorios()
            elif opcao == "0":
                print("\nSaindo do sistema. Até logo!")
                sys.exit(0)
            else:
                print("\n[ERRO] Opção inválida! Tente novamente.")

    def submenu_relatorios(self):
        while True:
            print("\n" + "="*40)
            print("            MENU DE RELATÓRIOS          ")
            print("="*40)
            print("1. Clínicas com maior número de atendimentos")
            print("2. Atendimentos mais caros e mais baratos")
            print("3. Procedimentos mais realizados (populares)")
            print("4. Procedimentos mais caros e mais baratos")
            print("0. Voltar ao Menu Principal")
            print("="*40)
            
            opcao = input("Selecione uma opção: ").strip()
            
            if opcao == "1":
                self.relatorio_view.relatorio_clinicas_atendimentos()
            elif opcao == "2":
                self.relatorio_view.relatorio_atendimentos_precos()
            elif opcao == "3":
                self.relatorio_view.relatorio_procedimentos_populares()
            elif opcao == "4":
                self.relatorio_view.relatorio_procedimentos_precos()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")
