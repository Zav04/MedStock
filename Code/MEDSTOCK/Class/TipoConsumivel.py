class Tipo_Consumivel:
    def __init__(
        self, 
        tipo_consumivel_id: int,
        nome_tipo: str
    ):
        self.tipo_consumivel_id = tipo_consumivel_id
        self.nome_tipo = nome_tipo

    def __eq__(self, other):
        if isinstance(other, Tipo_Consumivel):
            return (
                self.tipo_consumivel_id == other.tipo_consumivel_id and 
                self.nome_tipo == other.nome_tipo
            )
        return False

    def __hash__(self):
        return hash((self.tipo_consumivel_id, self.nome_tipo))
