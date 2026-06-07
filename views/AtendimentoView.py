from datetime import datetime
from controllers import AtendimentoController
from controllers.Context import RegraNegocioException, Context
from models import TipoAtendimento

class AtendimentoView:
    def __init__(self, controller: AtendimentoController, context: Context):
        self.controller = controller
        self.context = context

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("        GERENCIAMENTO DE ATENDIMENTOS   ")
            print("-"*40)
            print("1. Listar Atendimentos")
            print("2. Agendar Atendimento")
            print("3. Alterar Atendimento")
            print("4. Excluir Atendimento")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_atendimentos()
            elif opcao == "2":
                self.registrar_atendimento()
            elif opcao == "3":
                self.alterar_atendimento()
            elif opcao == "4":
                self.excluir_atendimento()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def listar_atendimentos(self) -> bool:
        print("\n--- ATENDIMENTOS AGENDADOS ---")
        if not self.context.atendimentos:
            print("Nenhum atendimento agendado.")
            return False
        for idx, at in enumerate(self.context.atendimentos, 1):
            pago_str = "Pago" if at.pagamento else "Pendente"
            print(f"{idx}. Data: {at.data.strftime('%d/%m/%Y')} | {at.inicio.strftime('%H:%M')} - {at.fim.strftime('%H:%M')}")
            print(f"   Clínica: {at.clinica.nome} | Paciente: {at.paciente.nome} | Médico: {at.profissional.nome}")
            print(f"   Tipo: {at.tipo.value} | Custo: R$ {at.custo:.2f} | Status: {pago_str}")
        return True

    def registrar_atendimento(self):
        print("\n--- REGISTRAR / AGENDAR ATENDIMENTO ---")
        if not self.context.clinicas:
            print("\n[AVISO] Cadastre pelo menos uma clínica antes de agendar atendimentos.")
            return
        if not self.context.pacientes:
            print("\n[AVISO] Cadastre pelo menos um paciente antes de agendar atendimentos.")
            return
        if not self.context.profissionais:
            print("\n[AVISO] Cadastre pelo menos um profissional de saúde antes de agendar atendimentos.")
            return

        try:
            # Clínica
            print("\nClínicas Disponíveis:")
            for indice, clinica in enumerate(self.context.clinicas, 1):
                print(f"{indice}. {clinica.nome} ({clinica.cidade})")
            c_opcao = int(input("Selecione a clínica (número): "))
            clinica = self.context.clinicas[c_opcao - 1]

            # Paciente
            print("\nPacientes Disponíveis:")
            for indice, p in enumerate(self.context.pacientes, 1):
                print(f"{indice}. {p.nome} (CPF: {p.cpf})")
            p_opcao = int(input("Selecione o paciente (número): "))
            paciente = self.context.pacientes[p_opcao - 1]

            # Profissional
            print("\nProfissionais Disponíveis:")
            for indice, prof in enumerate(self.context.profissionais, 1):
                print(f"{indice}. {prof.nome} ({prof.especialidade.value})")
            prof_opcao = int(input("Selecione o profissional (número): "))
            profissional = self.context.profissionais[prof_opcao - 1]

            # Data e Horário
            data_str = input("Data do Atendimento (DD/MM/AAAA): ").strip()
            data_atendimento = datetime.strptime(data_str, "%d/%m/%Y").date()
            
            hi_str = input("Hora de Início (HH:MM): ").strip()
            hf_str = input("Hora de Fim (HH:MM): ").strip()
            hora_inicio = datetime.strptime(hi_str, "%H:%M").time()
            hora_fim = datetime.strptime(hf_str, "%H:%M").time()
            
            # Tipo de Atendimento
            print("\nTipos de Atendimento:")
            for indice, tipo in enumerate(TipoAtendimento, 1):
                print(f"{indice}. {tipo.value}")
            tipo_opcao = int(input("Selecione o tipo (número): "))
            tipo = list(TipoAtendimento)[tipo_opcao - 1]

            custo_base = float(input("Custo do Atendimento (R$): "))
            
            atendimento = self.controller.agendar_atendimento(
                clinica, paciente, profissional, data_atendimento, hora_inicio, hora_fim, tipo, custo_base
            )
            print(f"\n[SUCESSO] Atendimento de {paciente.nome} agendado com sucesso!")

        except (ValueError, IndexError):
            print("\n[ERRO] Entrada de dados inválida ou seleção incorreta.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_atendimento(self):
        print("\n--- ALTERAR ATENDIMENTO ---")
        if not self.listar_atendimentos():
            return
        try:
            idx = int(input("Selecione o número do atendimento a alterar: "))
            atendimento = self.context.atendimentos[idx - 1]

            # Clínica
            print(f"\nClínica Atual: {atendimento.clinica.nome}")
            print("Alterar Clínica? (S/N): ")
            alterar_c = input().strip().upper()
            clinica = atendimento.clinica
            if alterar_c == "S":
                for i, c in enumerate(self.context.clinicas, 1):
                    print(f"{i}. {c.nome}")
                clinica = self.context.clinicas[int(input("Selecione a clínica (número): ")) - 1]

            # Paciente
            print(f"\nPaciente Atual: {atendimento.paciente.nome}")
            print("Alterar Paciente? (S/N): ")
            alterar_p = input().strip().upper()
            paciente = atendimento.paciente
            if alterar_p == "S":
                for i, p in enumerate(self.context.pacientes, 1):
                    print(f"{i}. {p.nome}")
                paciente = self.context.pacientes[int(input("Selecione o paciente (número): ")) - 1]

            # Profissional
            print(f"\nProfissional Atual: {atendimento.profissional.nome}")
            print("Alterar Profissional? (S/N): ")
            alterar_prof = input().strip().upper()
            profissional = atendimento.profissional
            if alterar_prof == "S":
                for i, prof in enumerate(self.context.profissionais, 1):
                    print(f"{i}. {prof.nome} ({prof.especialidade.value})")
                profissional = self.context.profissionais[int(input("Selecione o profissional (número): ")) - 1]

            # Data e Horário
            data_str = input(f"Nova Data (DD/MM/AAAA) [{atendimento.data.strftime('%d/%m/%Y')}]: ").strip()
            data_atendimento = datetime.strptime(data_str, "%d/%m/%Y").date() if data_str else atendimento.data

            hi_str = input(f"Nova Hora de Início (HH:MM) [{atendimento.inicio.strftime('%H:%M')}]: ").strip()
            hora_inicio = datetime.strptime(hi_str, "%H:%M").time() if hi_str else atendimento.inicio

            hf_str = input(f"Nova Hora de Fim (HH:MM) [{atendimento.fim.strftime('%H:%M')}]: ").strip()
            hora_fim = datetime.strptime(hf_str, "%H:%M").time() if hf_str else atendimento.fim

            # Tipo de Atendimento
            print(f"\nTipo Atual: {atendimento.tipo.value}")
            print("Alterar Tipo? (S/N): ")
            alterar_t = input().strip().upper()
            tipo = atendimento.tipo
            if alterar_t == "S":
                for i, t in enumerate(TipoAtendimento, 1):
                    print(f"{i}. {t.value}")
                tipo = list(TipoAtendimento)[int(input("Selecione o tipo (número): ")) - 1]

            custo_str = input(f"Novo Custo (R$) [{atendimento.custo:.2f}]: ").strip()
            custo = float(custo_str) if custo_str else atendimento.custo

            self.controller.alterar_atendimento(
                atendimento, clinica, paciente, profissional, data_atendimento, hora_inicio, hora_fim, tipo, custo
            )
            print(f"\n[SUCESSO] Atendimento alterado com sucesso!")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção ou valor inválido.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_atendimento(self):
        print("\n--- EXCLUIR ATENDIMENTO ---")
        if not self.listar_atendimentos():
            return
        try:
            idx = int(input("Selecione o número do atendimento a excluir: "))
            atendimento = self.context.atendimentos[idx - 1]
            
            confirmar = input(f"Deseja excluir o atendimento do paciente '{atendimento.paciente.nome}'? (S/N): ").strip().upper()
            if confirmar == "S":
                self.controller.excluir_atendimento(atendimento)
                print(f"\n[SUCESSO] Atendimento excluído com sucesso!")
            else:
                print("\nOperação cancelada.")
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")