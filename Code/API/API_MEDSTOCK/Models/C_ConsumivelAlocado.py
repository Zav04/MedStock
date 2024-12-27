from pydantic import BaseModel

class C_ConsumivelAlocado(BaseModel):
    consumivel_id: int
    quantidade_alocada: int