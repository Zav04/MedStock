class Itens:
    def __init__(
        self, 
        consumivel_id : int,
        nome_consumivel: str, 
        nome_tipo: str, 
        codigo: str, 
        quantidade_total: int, 
        quantidade_alocada: int, 
        quantidade_minima: int, 
        quantidade_pedido: int
    ):
        self.consumivel_id = consumivel_id
        self.nome_consumivel = nome_consumivel
        self.nome_tipo = nome_tipo
        self.codigo = codigo
        self.quantidade_total = quantidade_total
        self.quantidade_alocada = quantidade_alocada
        self.quantidade_minima = quantidade_minima
        self.quantidade_pedido = quantidade_pedido