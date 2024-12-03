class Itens:
    def __init__(
        self, 
        item_id: int,
        nome_item: str, 
        nome_tipo: str, 
        codigo: str, 
        quantidade_disponivel: int, 
        quantidade_total: int, 
        quantidade_alocada: int, 
        quantidade_minima: int, 
        quantidade_pedido: int
    ):
        self.item_id = item_id
        self.nome_item = nome_item
        self.nome_tipo = nome_tipo
        self.codigo = codigo
        self.quantidade_disponivel = quantidade_disponivel
        self.quantidade_total = quantidade_total
        self.quantidade_alocada = quantidade_alocada
        self.quantidade_minima = quantidade_minima
        self.quantidade_pedido = quantidade_pedido