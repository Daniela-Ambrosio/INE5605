from datetime import date, time, datetime
from models import Clinica, Paciente, ProfissionalSaude, Atendimento, TipoAtendimento, Procedimento
from .validacoes import RegraNegocioException
from views.atendimento_view import AtendimentoView
from DAOs.atendimento_dao import AtendimentoDAO
from DAOs.clinica_dao import ClinicaDAO
from DAOs.paciente_dao import PacienteDAO
from DAOs.profissional_dao import ProfissionalDAO

class AtendimentoController:
    def __init__(self, context):
        self.__atendimento_DAO = AtendimentoDAO()
        self.__clinica_DAO = ClinicaDAO()
        self.__paciente_DAO = PacienteDAO()
        self.__profissional_DAO = ProfissionalDAO()
        self.__atendimento_view = AtendimentoView()

    def abrir_tela_atendimento(self):
        while True:
            opcao = self.__atendimento_view.tela_opcoes()
            if opcao == 0: break
            elif opcao == 1: self._cadastrar_atendimento()
            elif opcao == 2: self._alterar_atendimento()
            elif opcao == 3: self._listar_atendimentos()
            elif opcao == 4: self._excluir_atendimento()

    def _listar_atendimentos(self):
        dados = []
        for at in self.__atendimento_DAO.get_all():
            pago = 'Pago' if at.pagamento else 'Pendente'
            dados.append({
                'data': at.data.strftime('%d/%m/%Y'),
                'inicio': at.inicio.strftime('%H:%M'),
                'fim': at.fim.strftime('%H:%M'),
                'clinica': at.clinica.nome,
                'paciente': at.paciente.nome,
                'profissional': at.profissional.nome,
                'tipo': at.tipo.value,
                'custo': f"{at.custo:.2f}",
                'status': pago,
                'codigo': at.codigo
            })
        self.__atendimento_view.mostra_atendimento(dados)

    def _buscar_atendimento(self, dt, ini):
        for at in self.__atendimento_DAO.get_all():
            if at.data.strftime('%d/%m/%Y') == dt and at.inicio.strftime('%H:%M') == ini:
                return at
        return None

    def _buscar_clinica(self, nome):
        for c in self.__clinica_DAO:
            if c.nome == nome: return c
        return None

    def _buscar_paciente(self, cpf):
        for p in self.__paciente_DAO:
            if p.cpf == cpf: return p
        return None

    def _buscar_profissional(self, nome):
        for p in self.__profissional_DAO:
            if p.nome == nome: return p
        return None

    def _cadastrar_atendimento(self):
        nomes_clinicas = [c.nome for c in self.__clinica_DAO]
        cpfs_pacientes = [p.cpf for p in self.__paciente_DAO]
        nomes_profissionais = [p.nome for p in self.__profissional_DAO]
        
        vals = self.__atendimento_view.pega_dados_atendimento(nomes_clinicas, cpfs_pacientes, nomes_profissionais)
        if vals:
            try:
                clinica = None
                for c in self.__clinica_DAO:
                    if c.nome == vals['clinica']: clinica = c
                if not clinica: raise ValueError("Opção de clínica inválida.")

                pa = self._buscar_paciente(vals['paciente'])
                pr = self._buscar_profissional(vals['profissional'])
                if not clinica: raise ValueError("Clínica não encontrada.")
                if not pa: raise ValueError("Paciente não encontrado.")
                if not pr: raise ValueError("Profissional não encontrado.")
                
                dt = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                hi = datetime.strptime(vals['inicio'], '%H:%M').time()
                hf = datetime.strptime(vals['fim'], '%H:%M').time()
                
                tipo = None
                for t in TipoAtendimento:
                    if t.value == vals['tipo']: tipo = t
                if not tipo: raise ValueError("Tipo inválido.")
                
                custo = float(vals['custo'])
                self.agendar_atendimento(clinica, pa, pr, dt, hi, hf, tipo, custo)
                self.__atendimento_view.mostra_mensagem('Atendimento cadastrado!')
            except ValueError as e:
                self.__atendimento_view.mostra_mensagem(f'Erro: {e}')
            except RegraNegocioException as e:
                self.__atendimento_view.mostra_mensagem(str(e))

    def _alterar_atendimento(self):
        self._listar_atendimentos()
        lista = [f"{a.data.strftime('%d/%m/%Y')} às {a.inicio.strftime('%H:%M')} - Paciente: {a.paciente.nome}" for a in self.__atendimento_DAO.get_all()]
        escolha = self.__atendimento_view.seleciona_atendimento(lista)
        if escolha:
            at = None
            for a in self.__atendimento_DAO.get_all():
                if f"{a.data.strftime('%d/%m/%Y')} às {a.inicio.strftime('%H:%M')} - Paciente: {a.paciente.nome}" == escolha:
                    at = a
                    break
                
            nomes_clinicas = [c.nome for c in self.__clinica_DAO]
            cpfs_pacientes = [p.cpf for p in self.__paciente_DAO]
            nomes_profissionais = [p.nome for p in self.__profissional_DAO]
            
            vals = self.__atendimento_view.pega_dados_atendimento(nomes_clinicas, cpfs_pacientes, nomes_profissionais)
            if vals:
                try:
                    clinica = None
                    for c in self.__clinica_DAO:
                        if c.nome == vals['clinica']: clinica = c
                    if not clinica: raise ValueError("Opção de clínica inválida.")
                    
                    pa = self._buscar_paciente(vals['paciente'])
                    pr = self._buscar_profissional(vals['profissional'])
                    if not clinica: raise ValueError("Clínica não encontrada.")
                    if not pa: raise ValueError("Paciente não encontrado.")
                    if not pr: raise ValueError("Profissional não encontrado.")
                    
                    ndt = datetime.strptime(vals['data'], '%d/%m/%Y').date()
                    nhi = datetime.strptime(vals['inicio'], '%H:%M').time()
                    nhf = datetime.strptime(vals['fim'], '%H:%M').time()

                    tipo = None
                    for t in TipoAtendimento:
                        if t.value == vals['tipo']: tipo = t
                    if not tipo: raise ValueError("Tipo inválido.")

                    custo = float(vals['custo'])

                    self.alterar_atendimento(at, clinica, pa, pr, ndt, nhi, nhf, tipo, custo)
                    self.__atendimento_view.mostra_mensagem('Atendimento alterado!')
                except Exception as e:
                    self.__atendimento_view.mostra_mensagem(f'Erro: {e}')
            

    def _excluir_atendimento(self):
        self._listar_atendimentos()
        lista = [f"{a.data.strftime('%d/%m/%Y')} às {a.inicio.strftime('%H:%M')} - Paciente: {a.paciente.nome}" for a in self.__atendimento_DAO.get_all()]
        escolha = self.__atendimento_view.seleciona_atendimento(lista)
        if escolha:
            at = None
            for a in self.__atendimento_DAO.get_all():
                if f"{a.data.strftime('%d/%m/%Y')} às {a.inicio.strftime('%H:%M')} - Paciente: {a.paciente.nome}" == escolha:
                    at = a
                    break
            if at:
                self.excluir_atendimento(at)
                self.__atendimento_view.mostra_mensagem('Excluído com sucesso!')
            else:
                self.__atendimento_view.mostra_mensagem('Não encontrado.')

    def agendar_atendimento(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, 
                            data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float = 0.0) -> Atendimento:
        idade = 2026 - paciente.data_nascimento.year 
        if idade < 18: raise RegraNegocioException("Maioridade necessária.")

        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise RegraNegocioException("Fora do horário da clínica.")

        for at in self.__atendimento_DAO.get_all():
            if at.data == data and at.inicio == hora_inicio:
                raise RegraNegocioException("Horário já preenchido.")

        at = Atendimento(clinica, paciente, profissional, data, hora_inicio, hora_fim, tipo, custo)
        self.__atendimento_DAO.add(at)
        return at

    def alterar_atendimento(self, atendimento: Atendimento, clinica: Clinica, paciente: Paciente, 
                            profissional: ProfissionalSaude, data: date, hora_inicio: time, hora_fim: time, 
                            tipo: TipoAtendimento, custo: float):
        atendimento.clinica = clinica
        atendimento.paciente = paciente
        atendimento.profissional = profissional
        atendimento.data = data
        atendimento.inicio = hora_inicio
        atendimento.fim = hora_fim
        atendimento.tipo = tipo
        atendimento.custo = custo

        self.__atendimento_DAO.update(atendimento)

    def excluir_atendimento(self, atendimento: Atendimento):
        if atendimento in self.__atendimento_DAO.get_all(): self.__atendimento_DAO.remove(atendimento.codigo)
