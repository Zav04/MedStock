from pydantic import BaseModel
from typing import Optional

class C_Requerimento(BaseModel):
    setor_id: Optional[int] = ''
    user_id_pedido: Optional[int] = ''
    user_id_confirmacao: Optional[int] = ''
    user_id_envio: Optional[int] = ''
    data_pedido: Optional[str] = ''
    data_confirmacao: Optional[str] = ''
    data_envio: Optional[str] = ''
    status: Optional[int] = ''
    urgent: Optional[int] = ''