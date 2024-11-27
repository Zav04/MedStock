from pydantic import BaseModel

class C_UpdateRequerimentoPreparacao(BaseModel):
    user_id: int
    requerimento_id: int