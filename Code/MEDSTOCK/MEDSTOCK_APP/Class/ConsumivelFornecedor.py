class Consumivel_Fornecedor:
    def __init__(
        self,
        fornecedor_id: int,
        fornecedor_nome: str,
        consumivel_id : int,
        nome_consumivel: str,
        nome_tipo: str, 
        tempoentrega: int,
        quantidade: int, 
    ):
        self.fornecedor_id = fornecedor_id
        self.fornecedor_nome = fornecedor_nome
        self.consumivel_id = consumivel_id
        self.nome_consumivel = nome_consumivel
        self.nome_tipo = nome_tipo
        self.tempoentrega = tempoentrega
        self.quantidade = quantidade
        
    def __eq__(self, other):
        if not isinstance(other, Consumivel_Fornecedor):
            return False
        return (
            self.fornecedor_id == other.fornecedor_id and
            self.fornecedor_nome == other.fornecedor_nome and
            self.consumivel_id == other.consumivel_id and
            self.nome_consumivel == other.nome_consumivel and
            self.nome_tipo == other.nome_tipo and
            self.tempoentrega == other.tempoentrega and
            self.quantidade == other.quantidade
        )
