from pydantic import BaseModel

class C_Update_Requerimento(BaseModel):
    requerimento_id: int
    user_id: int
