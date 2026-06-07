from typing import List, Tuple, Dict
from models import Clinica, Atendimento, Procedimento
from .Context import Context

class RelatoriosController:
    def __init__(self, context: Context):
        self.context = context

    def obter_clinicas_mais_atendimentos(self) -> List[Tuple[Clinica, int]]:
        contagem: Dict[Clinica, int] = {c: 0 for c in self.context.clinicas}
        for at in self.context.atendimentos:
            if at.clinica in contagem:
                contagem[at.clinica] += 1
        
        # Retorna lista ordenada de tuplas (Clinica, quantidade)
        return sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    
    def obter_atendimentos_mais_caros_e_baratos(self) -> Tuple[List[Atendimento], List[Atendimento]]:
        if not self.context.atendimentos:
            return [], []
        
        custo_max = max(at.custo for at in self.context.atendimentos)
        custo_min = min(at.custo for at in self.context.atendimentos)

        mais_caros = [at for at in self.context.atendimentos if at.custo == custo_max]
        mais_baratos = [at for at in self.context.atendimentos if at.custo == custo_min]

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
            todos_procedimentos.extend(at.procedimentos) #adiciona cada procedimento individualmente na lista
        
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
