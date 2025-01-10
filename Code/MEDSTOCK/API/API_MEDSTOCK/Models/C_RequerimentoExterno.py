from pydantic import BaseModel
from typing import Optional
from Models.C_RequerimentoConsumivel import C_RequerimentoConsumivel

class C_RequerimentoExterno(BaseModel):
    requerimento_id: int
    setor_id: Optional[int]
    user_id: int
    items_list: Optional[list[C_RequerimentoConsumivel]] 