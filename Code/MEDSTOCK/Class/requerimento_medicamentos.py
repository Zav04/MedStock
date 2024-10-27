
class RequerimentoMedicamentos:
    def __init__(self, requerimento_id: int, medicamento_id: int, quantidade: int):
        self.requerimento_id = requerimento_id
        self.medicamento_id = medicamento_id
        self.quantidade = quantidade
