from pydantic import BaseModel
from typing import Optional

class C_Login(BaseModel):
    email: Optional[str] = ''
    password: Optional[str] = ''