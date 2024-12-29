from pydantic import BaseModel
from typing import Optional

class C_Update_Requerimento(BaseModel):
    requerimento_id: int
    user_id: Optional[int] = None
