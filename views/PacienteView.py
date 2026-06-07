from datetime import datetime
from controllers import PessoaController
from controllers.Context import RegraNegocioException

class PacienteView:
    def __init__(self, controller: PessoaController):
        self.controller = controller

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("         GERENCIAMENTO DE PACIENTES     ")
            print("-"*40)
            print("1. Listar Pacientes")
            print("2. Cadastrar Paciente")
            print("3. Alterar Paciente")
            print("4. Excluir Paciente")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_pacientes()
            elif opcao == "2":
                self.cadastrar_paciente()
            elif opcao == "3":
                self.alterar_paciente()
            elif opcao == "4":
                self.excluir_paciente()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def listar_pacientes(self) -> bool:
        print("\n--- PACIENTES CADASTRADOS ---")
        if not self.controller.context.pacientes:
            print("Nenhum paciente cadastrado.")
            return False
        for idx, p in enumerate(self.controller.context.pacientes, 1):
            print(f"{idx}. {p.nome} (CPF: {p.cpf}) - Tel: {p.telefone} | Nascimento: {p.data_nascimento.strftime('%d/%m/%Y')}")
        return True

    def cadastrar_paciente(self):
        print("\n--- CADASTRAR PACIENTE ---")
        try:
            nome = input("Nome do paciente: ").strip()
            telefone = input("Telefone/Celular: ").strip()
            cpf = input("CPF: ").strip()
            nasc_str = input("Data de Nascimento (DD/MM/AAAA): ").strip()
            data_nascimento = datetime.strptime(nasc_str, "%d/%m/%Y").date()
            
            paciente = self.controller.cadastrar_paciente(nome, telefone, cpf, data_nascimento)
            print(f"\n[SUCESSO] Paciente '{paciente.nome}' cadastrado com sucesso!")
        except ValueError:
            print("\n[ERRO] Formato de data inválido! Use o formato DD/MM/AAAA (ex: 25/12/1990).")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_paciente(self):
        print("\n--- ALTERAR PACIENTE ---")
        if not self.listar_pacientes():
            return
        try:
            idx = int(input("Selecione o número do paciente a alterar: "))
            paciente = self.controller.context.pacientes[idx - 1]
            
            nome = input(f"Novo nome [{paciente.nome}]: ").strip() or paciente.nome
            telefone = input(f"Novo telefone [{paciente.telefone}]: ").strip() or paciente.telefone
            cpf = input(f"Novo CPF [{paciente.cpf}]: ").strip() or paciente.cpf
            
            nasc_str = input(f"Nova data de nascimento (DD/MM/AAAA) [{paciente.data_nascimento.strftime('%d/%m/%Y')}]: ").strip()
            data_nascimento = datetime.strptime(nasc_str, "%d/%m/%Y").date() if nasc_str else paciente.data_nascimento
            
            self.controller.alterar_paciente(paciente, nome, telefone, cpf, data_nascimento)
            print(f"\n[SUCESSO] Paciente '{paciente.nome}' alterado com sucesso!")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção ou valor inválido.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_paciente(self):
        print("\n--- EXCLUIR PACIENTE ---")
        if not self.listar_pacientes():
            return
        try:
            idx = int(input("Selecione o número do paciente a excluir: "))
            paciente = self.controller.context.pacientes[idx - 1]
            
            self.controller.excluir_paciente(paciente)
            print(f"\n[SUCESSO] Paciente excluído com sucesso!")
        
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")
