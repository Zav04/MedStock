class Consumivel_Requerimento_Fornecedor:
    def __init__(self, categoria: str, nome: str, quantidade_pedida: int):
        self.categoria = categoria
        self.nome = nome
        self.quantidade_pedida = quantidade_pedida
        
    def __eq__(self, other):
        if not isinstance(other, Consumivel_Requerimento_Fornecedor):
            return False
        return (
            self.categoria == other.categoria and
            self.nome == other.nome and
            self.quantidade_pedida == other.quantidade_pedida
        )



class Requerimento_Fornecedor:
    def __init__(
        self,
        id_requerimento: int,
        fornecedor_nome: str,
        status: str,
        data_requerimento: str,
        consumiveis: list[Consumivel_Requerimento_Fornecedor],
        alocado: bool
    ):
        self.id_requerimento = id_requerimento
        self.fornecedor_nome = fornecedor_nome
        self.status = status
        self.data_requerimento = data_requerimento
        self.consumiveis = consumiveis
        self.alocado = alocado
        
    def __eq__(self, other):
        if not isinstance(other, Requerimento_Fornecedor):
            return False
        return (
            self.id_requerimento == other.id_requerimento and
            self.fornecedor_nome == other.fornecedor_nome and
            self.status == other.status and
            self.data_requerimento == other.data_requerimento and
            self.consumiveis == other.consumiveis and 
            self.alocado == other.alocado
        )


