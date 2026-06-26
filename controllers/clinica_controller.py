from datetime import time, datetime
from models import Clinica
from .validacoes import validar_obrigatorios, RegraNegocioException
from .context import Context
from views.clinica_view import ClinicaView

class ClinicaController:
    def __init__(self, context):
        self.context = context
        self.clinica_view = ClinicaView()

    def abrir_tela(self):
        while True:
            botao, valores = self.clinica_view.open()
            if botao in (None, 'Voltar'):
                break
            elif botao == 'Listar':
                self._listar_clinicas()
            elif botao == 'Cadastrar':
                self._cadastrar_clinica()
            elif botao == 'Alterar':
                self._alterar_clinica()
            elif botao == 'Excluir':
                self._excluir_clinica()

    def _listar_clinicas(self):
        clinicas = self.context.clinicas
        if not clinicas:
            self.clinica_view.mostra_mensagem(
                'Aviso', 'Nenhuma clínica cadastrada.')
            return
        dados = []
        for c in clinicas:
            dados.append({
                'nome': c.nome,
                'cidade': c.cidade,
                'descricao': c.descricao,
                'hora_abertura': c.hora_abertura.strftime('%H:%M'),
                'hora_fechamento': c.hora_fechamento.strftime('%H:%M')
            })
        self.clinica_view.tela_listagem(dados)

    def _cadastrar_clinica(self):
        botao, vals = self.clinica_view.tela_formulario()
        if botao == 'Confirmar':
            try:
                ha = datetime.strptime(vals['hora_abertura'], '%H:%M').time()
                hf = datetime.strptime(vals['hora_fechamento'], '%H:%M').time()
                self.cadastrar_clinica(
                    vals['nome'], vals['cidade'], vals['descricao'], ha, hf
                )
                self.clinica_view.mostra_mensagem(
                    'Sucesso', 'Clínica cadastrada com sucesso!')
            except ValueError:
                self.clinica_view.mostra_mensagem(
                    'Erro', 'Formato de hora inválido! Use HH:MM.')
            except RegraNegocioException as e:
                self.clinica_view.mostra_mensagem('Erro', str(e))

    def _alterar_clinica(self):
        clinicas = self.context.clinicas
        if not clinicas:
            self.clinica_view.mostra_mensagem(
                'Aviso', 'Nenhuma clínica cadastrada.')
            return
        nomes = [f"{c.nome} ({c.cidade})" for c in clinicas]
        idx = self.clinica_view.mostra_lista_selecao(
            'Selecionar Clínica para Alterar', nomes)
        if idx is None:
            return
        clinica = clinicas[idx]
        dados = {
            'nome': clinica.nome,
            'cidade': clinica.cidade,
            'descricao': clinica.descricao,
            'hora_abertura': clinica.hora_abertura.strftime('%H:%M'),
            'hora_fechamento': clinica.hora_fechamento.strftime('%H:%M')
        }
        botao, vals = self.clinica_view.tela_formulario(dados)
        if botao == 'Confirmar':
            try:
                ha = datetime.strptime(vals['hora_abertura'], '%H:%M').time()
                hf = datetime.strptime(vals['hora_fechamento'], '%H:%M').time()
                self.alterar_clinica(
                    clinica, vals['nome'], vals['cidade'],
                    vals['descricao'], ha, hf
                )
                self.clinica_view.mostra_mensagem(
                    'Sucesso', 'Clínica alterada com sucesso!')
            except ValueError:
                self.clinica_view.mostra_mensagem(
                    'Erro', 'Formato de hora inválido! Use HH:MM.')
            except RegraNegocioException as e:
                self.clinica_view.mostra_mensagem('Erro', str(e))

    def _excluir_clinica(self):
        clinicas = self.context.clinicas
        if not clinicas:
            self.clinica_view.mostra_mensagem(
                'Aviso', 'Nenhuma clínica cadastrada.')
            return
        nomes = [f"{c.nome} ({c.cidade})" for c in clinicas]
        idx = self.clinica_view.mostra_lista_selecao(
            'Selecionar Clínica para Excluir', nomes)
        if idx is None:
            return
        clinica = clinicas[idx]
        try:
            self.excluir_clinica(clinica)
            self.clinica_view.mostra_mensagem(
                'Sucesso', 'Clínica excluída com sucesso!')
        except RegraNegocioException as e:
            self.clinica_view.mostra_mensagem('Erro', str(e))

    # Métodos de negócio (mantidos e integrados com DAO)
    def cadastrar_clinica(self, nome: str, cidade: str, descricao: str, 
                          hora_abertura: time, hora_fechamento: time) -> Clinica:
        validar_obrigatorios({"Nome": nome, "Cidade": cidade})
        clinica = Clinica(nome, cidade, descricao, hora_abertura, hora_fechamento)
        if clinica not in self.context.clinicas: self.context.clinicas.append(clinica)
        return clinica

    def alterar_clinica(self, clinica: Clinica, nome: str, cidade: str, descricao: str, 
                        hora_abertura: time, hora_fechamento: time):
        validar_obrigatorios({"Nome": nome, "Cidade": cidade})
        if clinica.nome != nome:
            if clinica in self.context.clinicas: self.context.clinicas.remove(clinica)
        clinica.nome = nome
        clinica.cidade = cidade
        clinica.descricao = descricao
        clinica.hora_abertura = hora_abertura
        clinica.hora_fechamento = hora_fechamento
        if clinica not in self.context.clinicas: self.context.clinicas.append(clinica)

    def excluir_clinica(self, clinica: Clinica):
        if any(at.clinica.nome == clinica.nome for at in self.context.atendimentos):
            raise RegraNegocioException("Não é possível excluir esta clínica pois ela possui atendimentos agendados.")
        if clinica in self.context.clinicas: self.context.clinicas.remove(clinica)