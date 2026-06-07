from controllers import RelatoriosController

class RelatorioView:
    def __init__(self, controller: RelatoriosController):
        self.controller = controller

    def relatorio_clinicas_atendimentos(self):
        print("\n" + "-"*50)
        print("   RELATÓRIO: CLÍNICAS COM MAIOR NÚMERO DE ATENDIMENTOS")
        print("-"*50)

        resultados = self.controller.obter_clinicas_mais_atendimentos()
        if not resultados:
            print("Nenhum atendimento registrado no sistema.")
            return None

        print(f"{'Posição':<8} | {'Clínica':<25} | {'Cidade':<15} | {'Qtd. Atendimentos'}")
        print("-"*65)

        for indice, (clinica, qtd) in enumerate(resultados, 0):
            print(f"{indice:<8} | {clinica.nome:<25} | {clinica.cidade:<15} | {qtd}")


    def relatorio_atendimentos_precos(self):
        print("\n" + "-"*65)
        print("   RELATÓRIO: ATENDIMENTOS MAIS CAROS E MAIS BARATOS")
        print("-"*65)
        caros, baratos = self.controller.obter_atendimentos_mais_caros_e_baratos()

        if not caros and not baratos:
            print("Nenhum atendimento registrado no sistema.")
            return None

        print(">>> ATENDIMENTO(S) MAIS CARO(S):")
        for at in caros:
            print(f" - Paciente: {at.paciente.nome} | Médico: {at.profissional.nome} | Clínica: {at.clinica.nome}")
            print(f"   Data: {at.data.strftime('%d/%m/%Y')} | Tipo: {at.tipo.value} | CUSTO TOTAL: R$ {at.custo:.2f}")
            if at.procedimentos:
                procs = ", ".join(p.descricao for p in at.procedimentos)
                print(f"   Procedimentos: {procs}")
            print()

        print(">>> ATENDIMENTO(S) MAIS BARATO(S):")
        for at in baratos:
            print(f" - Paciente: {at.paciente.nome} | Médico: {at.profissional.nome} | Clínica: {at.clinica.nome}")
            print(f"   Data: {at.data.strftime('%d/%m/%Y')} | Tipo: {at.tipo.value} | CUSTO TOTAL: R$ {at.custo:.2f}")
            if at.procedimentos:
                procs = ", ".join(p.descricao for p in at.procedimentos)
                print(f"   Procedimentos: {procs}")

            print()


    def relatorio_procedimentos_populares(self):
        print("\n" + "-"*50)
        print("   RELATÓRIO: PROCEDIMENTOS MAIS POPULARES / REALIZADOS")
        print("-"*50)
        resultados = self.controller.obter_procedimentos_mais_realizados()

        if not resultados:
            print("Nenhum procedimento foi realizado no sistema até o momento.")
            return None

        print(f"{'Posição':<8} | {'Procedimento':<30} | {'Vezes Realizado'}")
        print("-"*55)

        for indice, (desc, qtd) in enumerate(resultados, 0):
            print(f"{indice:<8} | {desc:<30} | {qtd}")


    def relatorio_procedimentos_precos(self):
        print("\n" + "-"*65)
        print("   RELATÓRIO: PROCEDIMENTOS MAIS CAROS E MAIS BARATOS")
        print("-"*65)
        caros, baratos = self.controller.obter_procedimentos_mais_caros_e_baratos()

        if not caros and not baratos:
            print("Nenhum procedimento registrado no sistema.")
            return None

        print(">>> PROCEDIMENTO(S) MAIS CARO(S):")
        for p in caros:
            print(f" - {p.descricao:<25} | Custo: R$ {p.custo:<10.2f} | Responsável: {p.profissional.nome}")
            
        print("\n>>> PROCEDIMENTO(S) MAIS BARATO(S):")
        for p in baratos:
            print(f" - {p.descricao:<25} | Custo: R$ {p.custo:<10.2f} | Responsável: {p.profissional.nome}")
