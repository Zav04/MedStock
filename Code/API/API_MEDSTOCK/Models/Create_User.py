from pydantic import BaseModel
from typing import Optional

class C_Create_User(BaseModel):
    nome: Optional[str] = ''
    email: Optional[str] = ''
    password: Optional[str] = ''
    sexo: Optional[str] = ''
    data_nascimento: Optional[str] = ''
    role: Optional[int] = ''