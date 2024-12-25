from datetime import datetime
from typing import Optional, List
from Class.ItemPedido import ItemPedido
from Class.RequerimentoHistorico import RequerimentoHistorico

class Requerimento:
    def __init__(self, 
                 requerimento_id: int, 
                 setor_nome_localizacao: str,
                 nome_utilizador_pedido: str,
                 email_utilizador_pedido: str,
                 status_atual: int,
                 status_anterior: Optional[int],
                 urgente: bool,
                 tipo_requerimento: str,
                 paciente_nome: Optional[str],
                 paciente_estado: Optional[str],
                 itens_pedidos: List[ItemPedido],
                 data_pedido: datetime,
                 historico: List[RequerimentoHistorico]):
        
        self.requerimento_id = requerimento_id
        self.setor_nome_localizacao = setor_nome_localizacao
        self.nome_utilizador_pedido = nome_utilizador_pedido
        self.email_utilizador_pedido = email_utilizador_pedido
        self.status_atual = status_atual
        self.status_anterior = status_anterior
        self.urgente = urgente
        self.tipo_requerimento = tipo_requerimento
        self.paciente_nome = paciente_nome
        self.paciente_estado = paciente_estado
        self.itens_pedidos = itens_pedidos
        self.data_pedido = data_pedido
        self.historico = historico

    def __eq__(self, other):
        if not isinstance(other, Requerimento):
            return False
        return (
            self.requerimento_id == other.requerimento_id and
            self.setor_nome_localizacao == other.setor_nome_localizacao and
            self.nome_utilizador_pedido == other.nome_utilizador_pedido and
            self.email_utilizador_pedido == other.email_utilizador_pedido and
            self.status_atual == other.status_atual and
            self.status_anterior == other.status_anterior and
            self.urgente == other.urgente and
            self.tipo_requerimento == other.tipo_requerimento and
            self.paciente_nome == other.paciente_nome and
            self.paciente_estado == other.paciente_estado and
            self.itens_pedidos == other.itens_pedidos and
            self.data_pedido == other.data_pedido and
            self.historico == other.historico
        )
