from pydantic import BaseModel

class C_ConsumivelExterno(BaseModel):
    nome_consumivel: str
    quantidade: int