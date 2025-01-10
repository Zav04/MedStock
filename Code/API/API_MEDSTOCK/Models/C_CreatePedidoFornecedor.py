from pydantic import BaseModel
from typing import List
from Models.C_ConsumivelExterno import C_ConsumivelExterno

class C_CreatePedidoFornecedor(BaseModel):
    pedido_id: int
    fornecedor_nome: str
    consumiveis: List[C_ConsumivelExterno]