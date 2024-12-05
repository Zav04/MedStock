class RequerimentoHistorico:
    def __init__(self, requerimento_status: int, descricao: str, data: str, user_responsavel: str):
        self.requerimento_status = requerimento_status
        self.descricao = descricao
        self.data = data
        self.user_responsavel = user_responsavel

    def __eq__(self, other):
        if not isinstance(other, RequerimentoHistorico):
            return False
        return (
            self.requerimento_status == other.requerimento_status and
            self.descricao == other.descricao and
            self.data == other.data and
            self.user_responsavel == other.user_responsavel
        )
