from datetime import time, datetime
from models import Clinica
from .validacoes import RegraNegocioException
from views.clinica_view import ClinicaView
from DAOs import ClinicaDAO, AtendimentoDAO

class ClinicaController:
    def __init__(self, context):
        self.__clinica_DAO = ClinicaDAO()
        self.__atendimento_DAO = AtendimentoDAO()
        self.__clinica_view = ClinicaView()

    def abrir_tela(self):
        while True:
            opcao = self.__clinica_view.tela_opcoes()
            if opcao == 0:
                break
            elif opcao == 1:
                self._cadastrar_clinica()
            elif opcao == 2:
                self._alterar_clinica()
            elif opcao == 3:
                self._listar_clinicas()
            elif opcao == 4:
                self._excluir_clinica()

    def _listar_clinicas(self):
        dados = []
        for c in self.__clinica_DAO.get_all():
            dados.append({
                'nome': c.nome,
                'cidade': c.cidade,
                'descricao': c.descricao,
                'hora_abertura': c.hora_abertura.strftime('%H:%M'),
                'hora_fechamento': c.hora_fechamento.strftime('%H:%M')
            })
        self.__clinica_view.mostra_clinica(dados)

    def _cadastrar_clinica(self):
        vals = self.__clinica_view.pega_dados_clinica()
        if vals:
            try:
                ha = datetime.strptime(vals['hora_abertura'], '%H:%M').time()
                hf = datetime.strptime(vals['hora_fechamento'], '%H:%M').time()
                self.cadastrar_clinica(
                    vals['nome'], vals['cidade'], vals['descricao'], ha, hf
                )
                self.__clinica_view.mostra_mensagem('Clínica cadastrada com sucesso!')

            except ValueError:
                self.__clinica_view.mostra_mensagem('Erro: Formato de hora inválido! Use HH:MM.')
            except RegraNegocioException as e:
                self.__clinica_view.mostra_mensagem(f'Erro: {str(e)}')

    def _buscar_clinica_por_nome(self, nome):
        for c in self.__clinica_DAO.get_all():
            if c.nome == nome:
                return c
        return None

    def _alterar_clinica(self):
        self._listar_clinicas()
        nome = self.__clinica_view.seleciona_clinica()
        if nome:
            clinica = self._buscar_clinica_por_nome(nome)
            if not clinica:
                self.__clinica_view.mostra_mensagem('Clínica não encontrada.')
                return
            
            vals = self.__clinica_view.pega_dados_clinica()
            if vals:
                try:
                    ha = datetime.strptime(vals['hora_abertura'], '%H:%M').time()
                    hf = datetime.strptime(vals['hora_fechamento'], '%H:%M').time()
                    self.alterar_clinica(
                        clinica, vals['nome'], vals['cidade'],
                        vals['descricao'], ha, hf
                    )
                    self.__clinica_view.mostra_mensagem('Clínica alterada com sucesso!')

                except ValueError:
                    self.__clinica_view.mostra_mensagem('Erro: Formato de hora inválido! Use HH:MM.')
                except RegraNegocioException as e:
                    self.__clinica_view.mostra_mensagem(f'Erro: {str(e)}')

    def _excluir_clinica(self):
        self._listar_clinicas()
        nome = self.__clinica_view.seleciona_clinica()
        if nome:
            clinica = self._buscar_clinica_por_nome(nome)
            if not clinica:
                self.__clinica_view.mostra_mensagem('Clínica não encontrada.')
                return
            try:
                self.excluir_clinica(clinica)
                self.__clinica_view.mostra_mensagem('Clínica excluída com sucesso!')

            except RegraNegocioException as e:
                self.__clinica_view.mostra_mensagem(f'Erro: {str(e)}')

    def cadastrar_clinica(self, nome: str, cidade: str, descricao: str, 
                          hora_abertura: time, hora_fechamento: time) -> Clinica:
        clinica = Clinica(nome, cidade, descricao, hora_abertura, hora_fechamento)
        if clinica not in self.__clinica_DAO.get_all(): self.__clinica_DAO.add(clinica)
        return clinica

    def alterar_clinica(self, clinica: Clinica, nome: str, cidade: str, descricao: str, 
                        hora_abertura: time, hora_fechamento: time):
        clinica.nome = nome
        clinica.cidade = cidade
        clinica.descricao = descricao
        clinica.hora_abertura = hora_abertura
        clinica.hora_fechamento = hora_fechamento

        self.__clinica_DAO.update(clinica)

    def excluir_clinica(self, clinica: Clinica):
        if any(at.clinica.nome == clinica.nome for at in self.__atendimento_DAO.get_all()):
            raise RegraNegocioException("Não é possível excluir esta clínica pois ela possui atendimentos agendados.")
            
        if clinica in self.__clinica_DAO.get_all(): self.__clinica_DAO.remove(clinica.nome)
