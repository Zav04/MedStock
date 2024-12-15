
from pydantic import BaseModel


class C_Gestor_Sector(BaseModel):
    utilizador_id: int
    setor_id: int