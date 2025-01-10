from pydantic import BaseModel
from typing import Optional

class C_ReavaliationRequerimento(BaseModel):
    requerimento_id: int
    user_id: int
    comentario: Optional[str] = None
    rejected_items: Optional[str] = None
