from pydantic import BaseModel
from typing import Optional

class C_RequerimentoItem(BaseModel):
    item_id: Optional[int] 
    quantidade: Optional[int]
