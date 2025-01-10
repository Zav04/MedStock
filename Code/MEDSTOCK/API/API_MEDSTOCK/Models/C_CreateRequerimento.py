from pydantic import BaseModel
from typing import Optional
from Models.C_RequerimentoConsumivel import C_RequerimentoConsumivel

class C_CreateRequerimento(BaseModel):
    user_id_pedido: int
    setor_id: Optional[int]
    urgente: bool
    requerimento_consumiveis: Optional[list[C_RequerimentoConsumivel]] 