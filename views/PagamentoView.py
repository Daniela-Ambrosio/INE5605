from datetime import datetime
from controllers import PagamentoController
from controllers.Context import RegraNegocioException, Context

class PagamentoView:
    def __init__(self, controller: PagamentoController, context: Context):
        self.controller = controller
        self.context = context

    def exibir_menu(self):
        while True:
            print("\n" + "-"*40)
            print("        GERENCIAMENTO DE PAGAMENTOS     ")
            print("-"*40)
            print("1. Listar Detalhes do Pagamento de um Atendimento")
            print("2. Registrar Pagamento")
            print("3. Quitar Parcela (Alterar Pagamento)")
            print("4. Excluir / Cancelar Pagamento")
            print("0. Voltar")
            print("-"*40)
            
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                self.listar_pagamentos()
            elif opcao == "2":
                self.registrar_pagamento()
            elif opcao == "3":
                self.alterar_pagamento()
            elif opcao == "4":
                self.excluir_pagamento()
            elif opcao == "0":
                break
            else:
                print("\n[ERRO] Opção inválida!")

    def selecionar_atendimento(self, apenas_pagos: bool = False) -> str:
        if not self.context.atendimentos:
            print("\n[AVISO] Não há atendimentos cadastrados.")
            return None
        
        print("\nSelecione o Atendimento:")
        lista = []
        for at in self.context.atendimentos:
            if apenas_pagos and at.pagamento is None:
                continue
            lista.append(at)
            
        if not lista:
            print("Nenhum atendimento corresponde aos critérios de seleção.")
            return None

        for idx, at in enumerate(lista, 1):
            status = "Com Pagamento" if at.pagamento else "Sem Pagamento"
            print(f"{idx}. Paciente: {at.paciente.nome} | Data: {at.data.strftime('%d/%m/%Y')} | Custo: R$ {at.custo:.2f} ({status})")
        
        try:
            at_opcao = int(input("Selecione o atendimento (número): "))
            return lista[at_opcao - 1]
        except (ValueError, IndexError):
            print("\n[ERRO] Seleção inválida.")
            return None

    def listar_pagamentos(self):
        print("\n--- DETALHES DE PAGAMENTO ---")
        atendimento = self.selecionar_atendimento()
        if not atendimento:
            return
        
        pagamento = atendimento.pagamento
        if pagamento is None:
            print("\nNenhum pagamento registrado para este atendimento.")
            print(f"Custo pendente de pagamento: R$ {atendimento.custo:.2f}")
            return
            
        print(f"\n--- Detalhes do Pagamento ---")
        print(f"Modalidade: {type(pagamento).__name__}")
        print(f"Data Contratação: {pagamento.data.strftime('%d/%m/%Y')}")
        print(f"Custo Total: R$ {pagamento.custo:.2f}")
        
        # Atributos específicos de cada forma de pagamento
        if hasattr(pagamento, "cpf"):
            print(f"CPF Pagador PIX: {pagamento.cpf}")
        elif hasattr(pagamento, "numero"):
            print(f"Cartão Nº: {pagamento.numero} | Bandeira: {pagamento.bandeira}")
            
        print(f"Valor Pago: R$ {pagamento.obter_valor_pago():.2f}")
        print(f"Valor Restante: R$ {pagamento.obter_valor_restante():.2f}")
        
        print("\n--- Situação das Parcelas ---")
        for parc in pagamento.parcelas:
            paga_str = "PAGA" if parc.paga else "PENDENTE"
            print(f" - Parcela {parc.numero}: R$ {parc.custo:.2f} | Vencimento: {parc.vencimento.strftime('%d/%m/%Y')} | Status: {paga_str}")

    def registrar_pagamento(self):
        print("\n--- REGISTRAR PAGAMENTO ---")
        if not self.context.atendimentos:
            print("\n[AVISO] Não há atendimentos registrados para efetuar pagamentos.")
            return

        print("\nSelecione o Atendimento para pagar:")
        atendimentos_pendentes = []
        for at in self.context.atendimentos:
            if at.pagamento is None:
                atendimentos_pendentes.append(at)
        
        if not atendimentos_pendentes:
            print("\nTodos os atendimentos já possuem pagamento registrado!")
            return

        for idx, at in enumerate(atendimentos_pendentes, 1):
            print(f"{idx}. {at.data.strftime('%d/%m/%Y')} | Paciente: {at.paciente.nome} | Custo Total: R$ {at.custo:.2f}")
        
        try:
            at_opcao = int(input("Selecione o atendimento (número): "))
            atendimento = atendimentos_pendentes[at_opcao - 1]

            data_str = input("Data do Pagamento (DD/MM/AAAA): ").strip()
            data_pagamento = datetime.strptime(data_str, "%d/%m/%Y").date()

            print("\nModalidades de Pagamento:")
            print("1. Dinheiro")
            print("2. PIX")
            print("3. Cartão de Crédito (Permite parcelamento)")
            modalidade = input("Selecione a modalidade: ").strip()

            if modalidade == "1":
                valor = float(input(f"Valor a ser pago em dinheiro (Total R$ {atendimento.custo:.2f}): "))
                self.controller.registrar_pagamento_dinheiro(atendimento, data_pagamento, valor)
                print(f"\n[SUCESSO] Pagamento em dinheiro registrado com sucesso!")
            
            elif modalidade == "2":
                cpf_pagador = input("CPF do Pagador PIX: ").strip()
                valor = float(input(f"Valor a ser pago no PIX (Total R$ {atendimento.custo:.2f}): "))
                self.controller.registrar_pagamento_pix(atendimento, data_pagamento, valor, cpf_pagador)
                print(f"\n[SUCESSO] Pagamento PIX registrado com sucesso!")

            elif modalidade == "3":
                num_cartao = int(input("Número do Cartão de Crédito: "))
                bandeira = input("Bandeira do Cartão (ex: Visa, Mastercard): ").strip()
                qtd_parcelas = int(input("Quantidade de Parcelas (Digite 1 para à vista): "))
                self.controller.registrar_pagamento_cartao_parcelado(atendimento, data_pagamento, num_cartao, bandeira, qtd_parcelas)
                
                custo_parcela = atendimento.custo / qtd_parcelas
                if qtd_parcelas > 1:
                    print(f"\n[SUCESSO] Pagamento Parcelado em {qtd_parcelas}x de R$ {custo_parcela:.2f} registrado com sucesso!")
                else:
                    print(f"\n[SUCESSO] Pagamento no Cartão à vista registrado com sucesso!")
            else:
                print("\n[ERRO] Modalidade inválida!")
        
        except (ValueError, IndexError):
            print("\n[ERRO] Entrada de dados inválida.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def alterar_pagamento(self):
        print("\n--- QUITAR PARCELA (ALTERAR PAGAMENTO) ---")
        atendimento = self.selecionar_atendimento(apenas_pagos=True)
        if not atendimento:
            return

        pagamento = atendimento.pagamento
        print("\nParcelas Pendentes:")
        pendentes = []
        for parc in pagamento.parcelas:
            if not parc.paga:
                pendentes.append(parc)
                print(f"Parcela {parc.numero}: Valor: R$ {parc.custo:.2f} | Vencimento: {parc.vencimento.strftime('%d/%m/%Y')}")

        if not pendentes:
            print("Todas as parcelas deste pagamento já estão quitadas!")
            return

        try:
            num_parcela = int(input("Selecione o número da parcela a quitar: "))
            self.controller.quitar_parcela(atendimento, num_parcela)
            print(f"\n[SUCESSO] Parcela {num_parcela} quitada com sucesso!")
        except ValueError:
            print("\n[ERRO] Valor inválido.")
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")

    def excluir_pagamento(self):
        print("\n--- EXCLUIR / CANCELAR PAGAMENTO ---")
        atendimento = self.selecionar_atendimento(apenas_pagos=True)
        if not atendimento:
            return
            
        try:
            self.controller.excluir_pagamento(atendimento)
            print(f"\n[SUCESSO] Pagamento cancelado/excluido com sucesso!")
            
        except RegraNegocioException as e:
            print(f"\n[AVISO] {e}")