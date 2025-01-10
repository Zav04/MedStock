class Realocacao:
    def __init__(self,requerimento_origem: int, requerimento_destino: int, nome_consumivel: str, quantidade: int, data_redistribuicao: str):
        self.requerimento_origem = requerimento_origem
        self.requerimento_destino = requerimento_destino
        self.nome_consumivel = nome_consumivel
        self.quantidade = quantidade
        self.data_redistribuicao = data_redistribuicao


    def __eq__(self, other):
        if not isinstance(other, Realocacao):
            return False
        return (
            self.requerimento_origem == other.requerimento_origem and
            self.requerimento_destino == other.requerimento_destino and
            self.nome_consumivel == other.nome_consumivel and
            self.quantidade == other.quantidade and
            self.data_redistribuicao == other.data_redistribuicao
        )