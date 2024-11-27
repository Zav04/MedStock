from pydantic import BaseModel
from typing import Optional

class C_ResetPassword(BaseModel):
    email: Optional[str] = ''