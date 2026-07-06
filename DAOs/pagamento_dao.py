from DAOs.dao import DAO
from models.pagamento import Pagamento

class PagamentoDAO(DAO):
    def __init__(self):
            super().__init__("pagamento.pkl")
    
    def add(self, pagamento: Pagamento):
        if (
            (pagamento is not None)
            and isinstance(pagamento, Pagamento)
            and isinstance(pagamento.codigo, int)
        ):
            super().add(pagamento.codigo, pagamento)

    def update(self, pagamento: Pagamento):
        if (
            (pagamento is not None)
            and isinstance(pagamento, Pagamento)
            and isinstance(pagamento.codigo, int)
        ):
            super().update(pagamento.codigo, pagamento)

    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo)

    def remove(self, codigo: int):
        if isinstance(codigo, int):
            return super().remove(codigo)