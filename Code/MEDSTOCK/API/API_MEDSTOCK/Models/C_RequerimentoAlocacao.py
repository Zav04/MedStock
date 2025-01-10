from pydantic import BaseModel
from typing import Optional
from Models.C_ConsumivelAlocado import C_ConsumivelAlocado
from pydantic import BaseModel

class C_RequerimentoAtualizacao(BaseModel):
    requerimento_id: int
    consumiveis: Optional[list[C_ConsumivelAlocado]]