from pydantic import BaseModel
from typing import Optional

class C_RequerimentoConsumivel(BaseModel):
    consumivel_id: Optional[int] 
    quantidade: Optional[int]
