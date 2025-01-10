class SetorHospital:
    def __init__(self, setor_id: int, nome_setor: str, localizacao: str):
        self.setor_id = setor_id
        self.nome_setor = nome_setor
        self.localizacao = localizacao

    def __eq__(self, other):
        if isinstance(other, SetorHospital):
            return (
                self.setor_id == other.setor_id and
                self.nome_setor == other.nome_setor and
                self.localizacao == other.localizacao
            )
        return False

    def __hash__(self):
        return hash((self.setor_id, self.nome_setor, self.localizacao))
