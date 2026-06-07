from datetime import datetime
from controllers import ClinicaController
from controllers.Context import RegraNegocioException

class ClinicaView:
    def __init__(self, controller: ClinicaController):
        self.controller = controller

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("         GERENCIAMENTO DE CLÍNICAS      ")
            print("-"*40)
            print("1. Listar Clínicas")
            print("2. Cadastrar Clínica")
            print("3. Alterar Clínica")
            print("4. Excluir Clínica")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_clinicas()
            elif opcao == "2":
                self.cadastrar_clinica()
            elif opcao == "3":
                self.alterar_clinica()
            elif opcao == "4":
                self.excluir_clinica()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def listar_clinicas(self) -> bool:
        print("\n--- CLÍNICAS CADASTRADAS ---")
        if not self.controller.context.clinicas:
            print("Nenhuma clínica cadastrada.")
            return False
        for idx, c in enumerate(self.controller.context.clinicas, 1):
            print(f"{idx}. {c.nome} ({c.cidade}) - {c.descricao} | Funcionamento: {c.hora_abertura.strftime('%H:%M')} - {c.hora_fechamento.strftime('%H:%M')}")
        return True

    def cadastrar_clinica(self):
        print("\n--- CADASTRAR CLÍNICA ---")
        try:
            nome = input("Nome da clínica: ").strip()
            cidade = input("Cidade: ").strip()
            descricao = input("Descrição: ").strip()
            ha_str = input("Hora de Abertura (HH:MM): ").strip()
            hf_str = input("Hora de Fechamento (HH:MM): ").strip()
            
            hora_abertura = datetime.strptime(ha_str, "%H:%M").time()
            hora_fechamento = datetime.strptime(hf_str, "%H:%M").time()
            
            clinica = self.controller.cadastrar_clinica(nome, cidade, descricao, hora_abertura, hora_fechamento)
            print(f"\n[SUCESSO] Clínica '{clinica.nome}' cadastrada com sucesso!")
        except ValueError:
            print("\n[ERRO] Formato de hora inválido! Use o formato HH:MM (ex: 08:30).")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_clinica(self):
        print("\n--- ALTERAR CLÍNICA ---")
        if not self.listar_clinicas():
            return
        try:
            idx = int(input("Selecione o número da clínica a alterar: "))
            clinica = self.controller.context.clinicas[idx - 1]
            
            nome = input(f"Novo nome [{clinica.nome}]: ").strip() or clinica.nome
            cidade = input(f"Nova cidade [{clinica.cidade}]: ").strip() or clinica.cidade
            descricao = input(f"Nova descrição [{clinica.descricao}]: ").strip() or clinica.descricao
            
            ha_str = input(f"Nova Hora de Abertura (HH:MM) [{clinica.hora_abertura.strftime('%H:%M')}]: ").strip()
            hora_abertura = datetime.strptime(ha_str, "%H:%M").time() if ha_str else clinica.hora_abertura
            
            hf_str = input(f"Nova Hora de Fechamento (HH:MM) [{clinica.hora_fechamento.strftime('%H:%M')}]: ").strip()
            hora_fechamento = datetime.strptime(hf_str, "%H:%M").time() if hf_str else clinica.hora_fechamento
            
            self.controller.alterar_clinica(clinica, nome, cidade, descricao, hora_abertura, hora_fechamento)
            print(f"\n[SUCESSO] Clínica '{clinica.nome}' alterada com sucesso!")

        except (ValueError, IndexError):
            print("\n[ERRO] Seleção ou valor inválido.")

        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_clinica(self):
        print("\n--- EXCLUIR CLÍNICA ---")
        if not self.listar_clinicas():
            return
        try:
            idx = int(input("Selecione o número da clínica a excluir: "))
            clinica = self.controller.context.clinicas[idx - 1]
            
            self.controller.excluir_clinica(clinica)
            print ("[SUCESSO] Clínica excluída com sucesso!")
            
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")