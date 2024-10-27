from typing import Optional

class SetorHospital:
    def __init__(self, setor_id: int, nome_setor: str, localizacao: str, responsavel_id: Optional[int]):
        self.setor_id = setor_id
        self.nome_setor = nome_setor
        self.localizacao = localizacao
        self.responsavel_id = responsavel_id