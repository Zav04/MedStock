from pydantic import BaseModel
from typing import Optional

class C_Items(BaseModel):
    nome_item: Optional[str] = ''
    tipo_id: Optional[int] = ''
    codigo: Optional[str] = ''
    quantidade_disponivel: Optional[int] = ''