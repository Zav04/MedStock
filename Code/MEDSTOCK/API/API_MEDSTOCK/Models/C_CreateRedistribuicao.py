from pydantic import BaseModel

class C_CreateRedistribuicao(BaseModel):
    consumivel_id: int
    requerimento_origem: int
    requerimento_destino: int
    quantidade: int