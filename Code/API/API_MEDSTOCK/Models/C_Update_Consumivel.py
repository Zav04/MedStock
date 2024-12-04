from pydantic import BaseModel
from typing import Optional

class C_Update_Consumivel(BaseModel):
    consumivel_id: int 
    quantidade_minima: int 
    quantidade_pedido: int
