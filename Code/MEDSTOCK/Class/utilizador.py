from datetime import date


class Utilizador:
    def __init__(self, utilizador_id: int, nome: str, email: str, sexo: str, data_nascimento: date, role_id: int):
        self.utilizador_id = utilizador_id
        self.nome = nome
        self.email = email
        self.sexo = sexo
        self.data_nascimento = data_nascimento
        self.role_id = role_id