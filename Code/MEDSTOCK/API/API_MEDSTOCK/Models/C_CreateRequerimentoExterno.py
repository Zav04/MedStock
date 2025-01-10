from pydantic import BaseModel

class C_CreateRequerimentoExterno(BaseModel):
    user_id_pedido: int
    paciente_nome: str
    paciente_estado: str