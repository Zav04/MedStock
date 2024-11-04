from pydantic import BaseModel
from typing import Optional

class C_Create_User_Email(BaseModel):
    email: Optional[str] = ''
    password: Optional[str] = ''