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
                 itens_pedidos: List['ItemPedido'],
                 nome_utilizador_confirmacao: Optional[str] = None,
                 nome_utilizador_envio: Optional[str] = None,
                 nome_utilizador_preparacao: Optional[str] = None,
                 data_confirmacao: Optional[datetime] = None, 
                 data_envio: Optional[datetime] = None,
                 data_preparacao: Optional[datetime] = None):
        
        self.requerimento_id = requerimento_id
        self.setor_nome_localizacao = setor_nome_localizacao
        self.nome_utilizador_pedido = nome_utilizador_pedido
        self.status = status
        self.urgente = urgente
        self.data_pedido = data_pedido
        self.itens_pedidos = itens_pedidos
        self.nome_utilizador_confirmacao = nome_utilizador_confirmacao
        self.nome_utilizador_envio = nome_utilizador_envio
        self.nome_utilizador_preparacao = nome_utilizador_preparacao
        self.data_confirmacao = data_confirmacao
        self.data_envio = data_envio
        self.data_preparacao = data_preparacao

    def __eq__(self, other):
        if not isinstance(other, Requerimento):
            return False
        return (
            self.requerimento_id == other.requerimento_id and
            self.setor_nome_localizacao == other.setor_nome_localizacao and
            self.nome_utilizador_pedido == other.nome_utilizador_pedido and
            self.status == other.status and
            self.urgente == other.urgente and
            self.data_pedido == other.data_pedido and
            self.itens_pedidos == other.itens_pedidos and
            self.nome_utilizador_confirmacao == other.nome_utilizador_confirmacao and
            self.nome_utilizador_envio == other.nome_utilizador_envio and
            self.nome_utilizador_preparacao == other.nome_utilizador_preparacao and
            self.data_confirmacao == other.data_confirmacao and
            self.data_envio == other.data_envio and
            self.data_preparacao == other.data_preparacao
        )
