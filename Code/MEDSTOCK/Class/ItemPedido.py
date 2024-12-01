class ItemPedido:
    def __init__(self, nome_item: str, quantidade: int, tipo_item: str):
        self.nome_item = nome_item
        self.quantidade = quantidade
        self.tipo_item = tipo_item

    def __eq__(self, other):
        if not isinstance(other, ItemPedido):
            return False
        return (
            self.nome_item == other.nome_item and
            self.quantidade == other.quantidade and
            self.tipo_item == other.tipo_item
        )
