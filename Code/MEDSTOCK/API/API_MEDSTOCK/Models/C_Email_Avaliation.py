from pydantic import BaseModel


class C_Email_Avaliation(BaseModel):
    remetente_email: str
    nome_avaliador: str
    data_avaliacao: str
    requerimento_id: int
    itens: list