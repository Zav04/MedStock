from datetime import datetime
from typing import Optional, List
from Class.ItemPedido import ItemPedido


class Requerimento:
    def __init__(self, 
                 requerimento_id: int, 
                 setor_nome_localizacao: str,
                 nome_utilizador_pedido: str,
                 status: int, 
                 urgente: bool,
                 data_pedido: datetime, 
                 itens_pedidos: List[ItemPedido],
                 nome_utilizador_confirmacao: Optional[str] = None,
                 nome_utilizador_envio: Optional[str] = None,
                 data_confirmacao: Optional[datetime] = None, 
                 data_envio: Optional[datetime] = None):
        
        self.requerimento_id = requerimento_id
        self.setor_nome_localizacao = setor_nome_localizacao
        self.nome_utilizador_pedido = nome_utilizador_pedido
        self.status = status
        self.urgente = urgente
        self.data_pedido = data_pedido
        self.itens_pedidos = itens_pedidos
        self.nome_utilizador_confirmacao = nome_utilizador_confirmacao
        self.nome_utilizador_envio = nome_utilizador_envio
        self.data_confirmacao = data_confirmacao
        self.data_envio = data_envio