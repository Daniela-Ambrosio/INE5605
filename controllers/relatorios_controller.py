from typing import List, Tuple, Dict
from models import Clinica, Atendimento, Procedimento
from .context import Context
from views.relatorio_view import RelatorioView

class RelatoriosController:
    def __init__(self, context):
        self.context = context
        self.relatorio_view = RelatorioView()

    # ================================================================
    #  RELATÓRIOS - UI
    # ================================================================
    def abrir_tela(self):
        while True:
            botao, valores = self.relatorio_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Relatório 1':
                self._gerar_relatorio_clinicas()
            elif botao == 'Relatório 2':
                self._gerar_relatorio_procedimentos_qtd()
            elif botao == 'Relatório 3':
                self._gerar_relatorio_atendimentos_caros_baratos()
            elif botao == 'Relatório 4':
                self._gerar_relatorio_procedimentos_caros_baratos()

    def _gerar_relatorio_clinicas(self):
        lista = self.obter_clinicas_mais_atendimentos()
        if not lista:
            self.relatorio_view.mostra_relatorio("Nenhum dado encontrado.")
            return
        linhas = ["=== CLÍNICAS COM MAIS ATENDIMENTOS ===", ""]
        for clinica, qtd in lista:
            linhas.append(f"{clinica.nome} ({clinica.cidade}) - {qtd} atendimento(s)")
        self.relatorio_view.mostra_relatorio("\n".join(linhas))

    def _gerar_relatorio_procedimentos_qtd(self):
        lista = self.obter_procedimentos_mais_realizados()
        if not lista:
            self.relatorio_view.mostra_relatorio("Nenhum dado encontrado.")
            return
        linhas = ["=== PROCEDIMENTOS MAIS REALIZADOS ===", ""]
        for desc, qtd in lista:
            linhas.append(f"{desc} - {qtd} vez(es)")
        self.relatorio_view.mostra_relatorio("\n".join(linhas))

    def _gerar_relatorio_atendimentos_caros_baratos(self):
        caros, baratos = self.obter_atendimentos_mais_caros_e_baratos()
        if not caros and not baratos:
            self.relatorio_view.mostra_relatorio("Nenhum dado encontrado.")
            return
        linhas = ["=== ATENDIMENTOS MAIS CAROS ==="]
        for at in caros:
            linhas.append(
                f"Data: {at.data.strftime('%d/%m/%Y')} | Paciente: {at.paciente.nome} | "
                f"Profissional: {at.profissional.nome} | Custo: R$ {at.custo:.2f}"
            )
        linhas.extend(["", "=== ATENDIMENTOS MAIS BARATOS ==="])
        for at in baratos:
            linhas.append(
                f"Data: {at.data.strftime('%d/%m/%Y')} | Paciente: {at.paciente.nome} | "
                f"Profissional: {at.profissional.nome} | Custo: R$ {at.custo:.2f}"
            )
        self.relatorio_view.mostra_relatorio("\n".join(linhas))

    def _gerar_relatorio_procedimentos_caros_baratos(self):
        caros, baratos = self.obter_procedimentos_mais_caros_e_baratos()
        if not caros and not baratos:
            self.relatorio_view.mostra_relatorio("Nenhum dado encontrado.")
            return
        linhas = ["=== PROCEDIMENTOS MAIS CAROS ==="]
        for p in caros:
            linhas.append(
                f"{p.descricao} | Profissional: {p.profissional.nome} | "
                f"Custo: R$ {p.custo:.2f}"
            )
        linhas.extend(["", "=== PROCEDIMENTOS MAIS BARATOS ==="])
        for p in baratos:
            linhas.append(
                f"{p.descricao} | Profissional: {p.profissional.nome} | "
                f"Custo: R$ {p.custo:.2f}"
            )
        self.relatorio_view.mostra_relatorio("\n".join(linhas))

    # ================================================================
    #  REGRAS DE NEGÓCIO
    # ================================================================
    def obter_clinicas_mais_atendimentos(self) -> List[Tuple[Clinica, int]]:
        contagem: Dict[str, int] = {c.nome: 0 for c in self.context.clinicas}
        clinicas_dict = {c.nome: c for c in self.context.clinicas}
        
        for at in self.context.atendimentos:
            if at.clinica.nome in contagem:
                contagem[at.clinica.nome] += 1
        
        resultado = [(clinicas_dict[nome], qtd) for nome, qtd in contagem.items()]
        return sorted(resultado, key=lambda item: item[1], reverse=True)
    
    def obter_atendimentos_mais_caros_e_baratos(self) -> Tuple[List[Atendimento], List[Atendimento]]:
        atendimentos = self.context.atendimentos
        if not atendimentos:
            return [], []
        
        custo_max = max(at.custo for at in atendimentos)
        custo_min = min(at.custo for at in atendimentos)

        mais_caros = [at for at in atendimentos if at.custo == custo_max]
        mais_baratos = [at for at in atendimentos if at.custo == custo_min]

        return mais_caros, mais_baratos

    def obter_procedimentos_mais_realizados(self) -> List[Tuple[str, int]]:
        contagem: Dict[str, int] = {}
        for at in self.context.atendimentos:
            for proc in at.procedimentos:
                desc = proc.descricao.strip().capitalize()
                contagem[desc] = contagem.get(desc, 0) + 1
        
        lista_maior_para_menor = sorted(contagem.items(), key=lambda item: item[1], reverse=True)
        return lista_maior_para_menor
    
    def obter_procedimentos_mais_caros_e_baratos(self) -> Tuple[List[Procedimento], List[Procedimento]]:
        todos_procedimentos: List[Procedimento] = []

        for at in self.context.atendimentos:
            todos_procedimentos.extend(at.procedimentos)
        
        if not todos_procedimentos:
            return [], []

        custo_max = max(p.custo for p in todos_procedimentos)
        custo_min = min(p.custo for p in todos_procedimentos)

        mais_caros: List[Procedimento] = []
        mais_baratos: List[Procedimento] = []
        
        descs_caras = set()
        descs_baratas = set()

        for p in todos_procedimentos:
            if p.custo == custo_max and p.descricao not in descs_caras:
                mais_caros.append(p)
                descs_caras.add(p.descricao)
            if p.custo == custo_min and p.descricao not in descs_baratas:
                mais_baratos.append(p)
                descs_baratas.add(p.descricao)

        return mais_caros, mais_baratos
