from pydantic import BaseModel
from typing import Optional

class C_ReavaliationRequerimento(BaseModel):
    requerimento_id: int
    user_id: int
    comentario: str
    rejected_items: Optional[str] = ''