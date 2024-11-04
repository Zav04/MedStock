from pydantic import BaseModel
from typing import Optional

class C_RequerimentoMedicamentos(BaseModel):
    item_id: Optional[int] = ''
    requerimento_id: Optional[int] = ''
    quantidade: Optional[int] = ''