from typing import Optional
from pydantic import BaseModel

class C_SetorCreateRequest(BaseModel):
    nome_setor: str 
    localizacao: str
