class Roles:
    def __init__(self, role_id: int, nome_role: str):
        self.role_id = role_id
        self.nome_role = nome_role

    def __eq__(self, other):
        if isinstance(other, Roles):
            return self.role_id == other.role_id and self.nome_role == other.nome_role
        return False

    def __hash__(self):
        return hash((self.role_id, self.nome_role))
