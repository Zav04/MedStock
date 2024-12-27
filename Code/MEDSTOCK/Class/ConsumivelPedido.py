class ConsumivelPedido:
    def __init__(self, consumivel_id: int, nome_item: str, quantidade: int,quantidade_alocada: int, tipo_item: str):
        self.consumivel_id = consumivel_id
        self.nome_item = nome_item
        self.quantidade = quantidade
        self.quantidade_alocada = quantidade_alocada
        self.tipo_item = tipo_item

    def __eq__(self, other):
        if not isinstance(other, ConsumivelPedido):
            return False
        return (
            self.consumivel_id == other.consumivel_id and
            self.nome_item == other.nome_item and
            self.quantidade == other.quantidade and
            self.quantidade_alocada == other.quantidade_alocada and
            self.tipo_item == other.tipo_item
        )