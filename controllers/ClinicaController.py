from datetime import time
from models import Clinica
from .Context import Context, RegraNegocioException
from .validacoes import validar_obrigatorios

class ClinicaController:
    def __init__(self, context: Context):
        self.context = context
    
    def cadastrar_clinica(self, nome: str, cidade: str, descricao: str, 
                          hora_abertura: time, hora_fechamento: time) -> Clinica:
        validar_obrigatorios({"Nome": nome, "Cidade": cidade})
        
        clinica = Clinica(nome, cidade, descricao, hora_abertura, hora_fechamento)
        self.context.clinicas.append(clinica)

        return clinica

    def alterar_clinica(self, clinica: Clinica, nome: str, cidade: str, descricao: str, 
                        hora_abertura: time, hora_fechamento: time):
        validar_obrigatorios({"Nome": nome, "Cidade": cidade})

        clinica.nome = nome
        clinica.cidade = cidade
        clinica.descricao = descricao
        clinica.hora_abertura = hora_abertura
        clinica.hora_fechamento = hora_fechamento

    def excluir_clinica(self, clinica: Clinica):
        if any(at.clinica == clinica for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir esta clínica pois ela possui atendimentos agendados.")
            
        if clinica in self.context.clinicas:
            self.context.clinicas.remove(clinica)