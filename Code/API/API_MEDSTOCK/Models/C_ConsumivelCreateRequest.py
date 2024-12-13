from typing import Optional
from pydantic import BaseModel

class C_ConsumivelCreateRequest(BaseModel):
    nome_consumivel: str
    codigo: str
    tipo_id: Optional[int] = None
