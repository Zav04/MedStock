from pydantic import BaseModel
from typing import Optional
from Models.C_RequerimentoItem import C_RequerimentoItem

class C_CreateRequerimento(BaseModel):
    user_id_pedido: int
    setor_id: Optional[int]
    urgente: bool
    requerimento_items: Optional[list[C_RequerimentoItem]] 