from controllers import PessoaController
from controllers.Context import RegraNegocioException
from models import Especialidade

class ProfissionalView:
    def __init__(self, controller: PessoaController):
        self.controller = controller

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("        GERENCIAMENTO DE PROFISSIONAIS  ")
            print("-"*40)
            print("1. Listar Profissionais")
            print("2. Cadastrar Profissional")
            print("3. Alterar Profissional")
            print("4. Excluir Profissional")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_profissionais()
            elif opcao == "2":
                self.cadastrar_profissional()
            elif opcao == "3":
                self.alterar_profissional()
            elif opcao == "4":
                self.excluir_profissional()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def listar_profissionais(self) -> bool:
        print("\n--- PROFISSIONAIS CADASTRADOS ---")
        if not self.controller.context.profissionais:
            print("Nenhum profissional cadastrado.")
            return False
        for idx, p in enumerate(self.controller.context.profissionais, 1):
            print(f"{idx}. {p.nome} (Registro: {p.registro}) - Esp: {p.especialidade.value} | Tel: {p.telefone}")
        return True

    def cadastrar_profissional(self):
        print("\n--- CADASTRAR PROFISSIONAL DE SAÚDE ---")
        try:
            nome = input("Nome do médico/profissional: ").strip()
            telefone = input("Telefone: ").strip()
            cpf = input("CPF: ").strip()
            
            print("\nEspecialidades disponíveis:")
            for indice, esp in enumerate(Especialidade, 1):
                print(f"{indice}. {esp.value}")

            esp_opcao = int(input("Selecione a especialidade (número): "))
            especialidade = list(Especialidade)[esp_opcao - 1]
            
            registro = int(input("Registro Profissional (CRM): "))
            
            profissional = self.controller.cadastrar_profissional(nome, telefone, cpf, especialidade, registro)
            print(f"\n[SUCESSO] Profissional '{profissional.nome}' ({profissional.especialidade.value}) cadastrado com sucesso!")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção de especialidade ou registro inválido.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_profissional(self):
        print("\n--- ALTERAR PROFISSIONAL ---")
        if not self.listar_profissionais():
            return
        try:
            idx = int(input("Selecione o número do profissional a alterar: "))
            profissional = self.controller.context.profissionais[idx - 1]
            
            nome = input(f"Novo nome [{profissional.nome}]: ").strip() or profissional.nome
            telefone = input(f"Novo telefone [{profissional.telefone}]: ").strip() or profissional.telefone
            cpf = input(f"Novo CPF [{profissional.cpf}]: ").strip() or profissional.cpf
            
            print(f"\nEspecialidade atual: {profissional.especialidade.value}")
            print("Deseja alterar a especialidade? (S/N): ")
            alterar_esp = input().strip().upper()
            
            especialidade = profissional.especialidade
            if alterar_esp == "S":
                print("\nEspecialidades disponíveis:")
                for index, esp in enumerate(Especialidade, 1):
                    print(f"{index}. {esp.value}")
                esp_opcao = int(input("Selecione a especialidade (número): "))
                especialidade = list(Especialidade)[esp_opcao - 1]
                
            reg_str = input(f"Novo Registro CRM [{profissional.registro}]: ").strip()
            registro = int(reg_str) if reg_str else profissional.registro
            
            self.controller.alterar_profissional(profissional, nome, telefone, cpf, especialidade, registro)
            print(f"\n[SUCESSO] Profissional '{profissional.nome}' alterado com sucesso!")
            
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção ou valores inválidos.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_profissional(self):
        print("\n--- EXCLUIR PROFISSIONAL ---")
        if not self.listar_profissionais():
            return
        try:
            idx = int(input("Selecione o número do profissional a excluir: "))
            profissional = self.controller.context.profissionais[idx - 1]
            
            self.controller.excluir_profissional(profissional)
            print(f"\n[SUCESSO] Profissional excluído com sucesso!")
    
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")