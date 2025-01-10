from datetime import date

class Utilizador:
    def __init__(self, utilizador_id: int, nome: str, email: str, sexo: str, data_nascimento: date, role_id: int, role_nome: str):
        self.utilizador_id = utilizador_id
        self.nome = nome
        self.email = email
        self.sexo = sexo
        self.data_nascimento = data_nascimento
        self.role_id = role_id
        self.role_nome = role_nome

    def __eq__(self, other):
        if not isinstance(other, Utilizador):
            return False
        return (
            self.utilizador_id == other.utilizador_id and
            self.nome == other.nome and
            self.email == other.email and
            self.sexo == other.sexo and
            self.data_nascimento == other.data_nascimento and
            self.role_id == other.role_id and
            self.role_nome == other.role_nome
        )

    def __hash__(self):
        return hash((self.utilizador_id, self.nome, self.email, self.sexo, self.data_nascimento, self.role_id, self.role_nome))
