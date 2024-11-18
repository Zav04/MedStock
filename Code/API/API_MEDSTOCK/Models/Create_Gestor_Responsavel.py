from pydantic import BaseModel
from typing import Optional

class C_Create_Gestor_Responsavel(BaseModel):
    nome: Optional[str] = ''
    email: Optional[str] = ''
    password: Optional[str] = ''
    sexo: Optional[str] = ''
    data_nascimento: Optional[str] = ''
    role: Optional[int] = ''
    setor: Optional[int] = ''