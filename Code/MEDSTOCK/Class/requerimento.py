from datetime import datetime
from typing import Optional


class Requerimento:
    def __init__(self, requerimento_id: int, setor_id: int, utilizador_id_pedido: int, status: int,
                 data_pedido: datetime, utilizador_id_confirmacao: Optional[int] = None, 
                 utilizador_id_envio: Optional[int] = None, data_confirmacao: Optional[datetime] = None, 
                 data_envio: Optional[datetime] = None):
        self.requerimento_id = requerimento_id
        self.setor_id = setor_id
        self.utilizador_id_pedido = utilizador_id_pedido
        self.utilizador_id_confirmacao = utilizador_id_confirmacao
        self.utilizador_id_envio = utilizador_id_envio
        self.data_pedido = data_pedido
        self.data_confirmacao = data_confirmacao
        self.data_envio = data_envio
        self.status = status