from controllers import AtendimentoController 
from controllers.Context import RegraNegocioException, Context

class ProcedimentoView:
    def __init__(self, controller: AtendimentoController, context: Context):
        self.controller = controller
        self.context = context

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("        GERENCIAMENTO DE PROCEDIMENTOS  ")
            print("-"*40)
            print("1. Listar Procedimentos de um Atendimento")
            print("2. Registrar Procedimento em Atendimento")
            print("3. Alterar Procedimento")
            print("4. Excluir Procedimento")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_procedimentos()
            elif opcao == "2":
                self.registrar_procedimento()
            elif opcao == "3":
                self.alterar_procedimento()
            elif opcao == "4":
                self.excluir_procedimento()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def selecionar_atendimento(self) -> str:
        if not self.context.atendimentos:
            print("\n[AVISO] Não há atendimentos agendados cadastrados.")
            return None
        
        print("\nSelecione o Atendimento:")
        for idx, at in enumerate(self.context.atendimentos, 1):
            pago_str = "Pago" if at.pagamento else "Pendente"
            print(f"{idx}. Paciente: {at.paciente.nome} | Data: {at.data.strftime('%d/%m/%Y')} | Custo: R$ {at.custo:.2f} ({pago_str})")
        
        try:
            at_opcao = int(input("Selecione o atendimento (número): "))
            return self.context.atendimentos[at_opcao - 1]
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
            return None

    def listar_procedimentos(self) -> bool:
        atendimento = self.selecionar_atendimento()
        if not atendimento:
            return False
        
        print(f"\n--- PROCEDIMENTOS DO ATENDIMENTO ({atendimento.paciente.nome} - {atendimento.data.strftime('%d/%m/%Y')}) ---")
        if not atendimento.procedimentos:
            print("Nenhum procedimento registrado neste atendimento.")
            return False
        
        for idx, proc in enumerate(atendimento.procedimentos, 1):
            print(f"{idx}. {proc.descricao} | Custo: R$ {proc.custo:.2f} | Responsável: {proc.profissional.nome}")
        return True

    def registrar_procedimento(self):
        print("\n--- REGISTRAR PROCEDIMENTO EM ATENDIMENTO ---")
        atendimento = self.selecionar_atendimento()
        if not atendimento:
            return

        if atendimento.pagamento:
            print("\n[AVISO] Este atendimento já possui um pagamento registrado. Não é possível adicionar novos procedimentos.")
            return

        try:
            descricao = input("Descrição do procedimento: ").strip()
            custo = float(input("Custo do procedimento (R$): "))

            # profissional responsável pelo procedimento
            print("\nSelecione o Profissional Responsável:")
            for idx, prof in enumerate(self.context.profissionais, 1):
                print(f"{idx}. {prof.nome} ({prof.especialidade.value})")

            prof_opcao = int(input("Selecione o profissional (número): "))
            responsavel = self.context.profissionais[prof_opcao - 1]

            self.controller.adicionar_procedimento_a_atendimento(atendimento, descricao, custo, responsavel)
            print(f"\n[SUCESSO] Procedimento '{descricao}' (R$ {custo:.2f}) adicionado ao atendimento. Novo custo total: R$ {atendimento.custo:.2f}")
        except (ValueError, IndexError):
            print("\n[ERRO] Entrada inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_procedimento(self):
        print("\n--- ALTERAR PROCEDIMENTO ---")
        atendimento = self.selecionar_atendimento()
        if not atendimento:
            return

        if atendimento.pagamento:
            print("\n[AVISO] Este atendimento já possui um pagamento registrado. Não é possível alterar seus procedimentos.")
            return

        if not atendimento.procedimentos:
            print("Nenhum procedimento cadastrado neste atendimento para alterar.")
            return

        for idx, proc in enumerate(atendimento.procedimentos, 1):
            print(f"{idx}. {proc.descricao} | Custo: R$ {proc.custo:.2f}")

        try:
            proc_idx = int(input("Selecione o número do procedimento a alterar: "))
            procedimento = atendimento.procedimentos[proc_idx - 1]

            descricao = input(f"Nova descrição [{procedimento.descricao}]: ").strip() or procedimento.descricao
            custo_str = input(f"Novo custo (R$) [{procedimento.custo:.2f}]: ").strip()
            custo = float(custo_str) if custo_str else procedimento.custo

            print(f"\nProfissional atual: {procedimento.profissional.nome}")
            print("Deseja alterar o profissional responsável? (S/N): ")
            alterar_prof = input().strip().upper()
            responsavel = procedimento.profissional
            if alterar_prof == "S":
                for i, prof in enumerate(self.context.profissionais, 1):
                    print(f"{i}. {prof.nome} ({prof.especialidade.value})")
                responsavel = self.context.profissionais[int(input("Selecione o profissional (número): ")) - 1]

            self.controller.alterar_procedimento(atendimento, procedimento, descricao, custo, responsavel)
            print(f"\n[SUCESSO] Procedimento alterado com sucesso! Novo custo total do atendimento: R$ {atendimento.custo:.2f}")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção ou valor inválido.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_procedimento(self):
        print("\n--- EXCLUIR PROCEDIMENTO ---")
        atendimento = self.selecionar_atendimento()
        if not atendimento:
            return

        if atendimento.pagamento:
            print("\n[AVISO] Este atendimento já possui um pagamento registrado. Não é possível excluir procedimentos.")
            return

        if not atendimento.procedimentos:
            print("Nenhum procedimento cadastrado neste atendimento para excluir.")
            return

        for idx, proc in enumerate(atendimento.procedimentos, 1):
            print(f"{idx}. {proc.descricao} | Custo: R$ {proc.custo:.2f}")

        try:
            proc_idx = int(input("Selecione o número do procedimento a excluir: "))
            procedimento = atendimento.procedimentos[proc_idx - 1]

            confirmar = input(f"Deseja excluir o procedimento '{procedimento.descricao}'? (S/N): ").strip().upper()
            if confirmar == "S":
                self.controller.excluir_procedimento(atendimento, procedimento)
                print(f"\n[SUCESSO] Procedimento removido com sucesso! Novo custo total do atendimento: R$ {atendimento.custo:.2f}")
            else:
                print("\nOperação cancelada.")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")