from Class.Consumivel import Consumivel
from Class.Requerimento import Requerimento
from API.API_PUT_Request import API_UpdateConsumivelAlocado
from APP.Overlays.Overlay import Overlay
from PyQt5.QtCore import QObject, pyqtSignal
import asyncio

class ConsumivelManager(QObject):
    data_updated = pyqtSignal()
    def __init__(self):
        self.consumiveis = []
        self.requerimentos = []
        self.parent_window_window = None
        super().__init__()

    def add_consumivel(self, consumiveis: list[Consumivel]):
        for novo_consumivel in consumiveis:
            consumivel_existente = next(
                (c for c in self.consumiveis if c.consumivel_id == novo_consumivel.consumivel_id),
                None
            )

            if consumivel_existente:

                if novo_consumivel.quantidade_total != consumivel_existente.quantidade_total:
                    diferenca_total = novo_consumivel.quantidade_total - consumivel_existente.quantidade_total
                    consumivel_existente.quantidade_total += diferenca_total

                if novo_consumivel.quantidade_alocada != consumivel_existente.quantidade_alocada:
                    diferenca_alocada = novo_consumivel.quantidade_alocada - consumivel_existente.quantidade_alocada
                    consumivel_existente.quantidade_alocada += diferenca_alocada

                consumivel_existente.quantidade_alocada = min(
                    consumivel_existente.quantidade_alocada, consumivel_existente.quantidade_total
                )

                consumivel_existente.quantidade_minima = novo_consumivel.quantidade_minima
                consumivel_existente.quantidade_pedido = novo_consumivel.quantidade_pedido

            else:
                novo_consumivel.quantidade_alocada = min(
                    novo_consumivel.quantidade_alocada, novo_consumivel.quantidade_total
                )
                self.consumiveis.append(novo_consumivel)


    def add_requerimento(self, requerimento: Requerimento):
        for index, existing_requerimento in enumerate(self.requerimentos):
            if existing_requerimento.requerimento_id == requerimento.requerimento_id:
                self.requerimentos[index] = requerimento
                return

        if requerimento.status_atual < 1 or (requerimento.tipo_requerimento == "Externo" and requerimento.status_atual == 11):
            self.requerimentos.append(requerimento)


    def alocar_consumiveis(self, requerimento_id: int) -> int:
        """
        Returns:
        -2: Requerimento inválido, sem consumíveis, ou todos os consumíveis já alocados.
        -1: Não foi possível alocar nenhum consumível.
        0: Alguns consumíveis foram alocados, mas não todos.
        1: Todos os consumíveis foram alocados com sucesso.
        """
        requerimento = next((r for r in self.requerimentos if r.requerimento_id == requerimento_id), None)
        if not requerimento:
            return -2

        if not requerimento.itens_pedidos or len(requerimento.itens_pedidos) == 0:
            return -2

        if all(item.quantidade_alocada >= item.quantidade for item in requerimento.itens_pedidos):
            return -2

        all_allocated = True
        any_allocated = False

        for item_pedido in requerimento.itens_pedidos:
            if item_pedido.quantidade_alocada >= item_pedido.quantidade:
                continue

            consumivel = next((c for c in self.consumiveis if c.consumivel_id == item_pedido.consumivel_id), None)
            if consumivel is None:
                all_allocated = False
                continue

            stock_virtual = consumivel.quantidade_total - consumivel.quantidade_alocada
            quantidade_necessaria = item_pedido.quantidade - item_pedido.quantidade_alocada

            if stock_virtual >= quantidade_necessaria:
                item_pedido.quantidade_alocada += quantidade_necessaria
                consumivel.quantidade_alocada += quantidade_necessaria
                any_allocated = True
            elif stock_virtual > 0:
                item_pedido.quantidade_alocada += stock_virtual
                consumivel.quantidade_alocada += stock_virtual
                any_allocated = True
                all_allocated = False
            else:
                all_allocated = False

        if not any_allocated:
            return -1

        return 1 if all_allocated else 0


    def redistribuir_para_urgente(self, requerimento_id: int) -> int:
        """
        Returns:
        -2: Requerimento inválido, sem consumíveis, ou todos os consumíveis já alocados.
        -1: Não foi possível alocar nenhum consumível.
         0: Alguns consumíveis foram alocados, mas não todos.
         1: Todos os consumíveis foram alocados com sucesso.
        """
        requerimento_urgente = next((r for r in self.requerimentos if r.requerimento_id == requerimento_id), None)
        if not requerimento_urgente:
            return -2

        if not requerimento_urgente.itens_pedidos or len(requerimento_urgente.itens_pedidos) == 0:
            return -2

        all_urgent_allocated = True
        any_allocated = False

        for item_pedido in requerimento_urgente.itens_pedidos:
            if item_pedido.quantidade_alocada >= item_pedido.quantidade:
                continue

            consumivel = next((c for c in self.consumiveis if c.consumivel_id == item_pedido.consumivel_id), None)
            if consumivel is None:
                all_urgent_allocated = False
                continue

            quantidade_necessaria = item_pedido.quantidade - item_pedido.quantidade_alocada
            requerimentos_nao_urgentes = sorted(
                (r for r in self.requerimentos if not r.urgente and r.status_atual != 4),
                key=lambda r: r.data_pedido
            )

            for req in requerimentos_nao_urgentes:
                for item in req.itens_pedidos:
                    if item.consumivel_id == item_pedido.consumivel_id and item.quantidade_alocada > 0:
                        quantidade_para_realocar = min(item.quantidade_alocada, quantidade_necessaria)
                        item.quantidade_alocada -= quantidade_para_realocar
                        consumivel.quantidade_alocada -= quantidade_para_realocar
                        consumivel.quantidade_total += quantidade_para_realocar
                        quantidade_necessaria -= quantidade_para_realocar
                        item_pedido.quantidade_alocada += quantidade_para_realocar
                        any_allocated = True

                        if quantidade_necessaria <= 0:
                            break
                if quantidade_necessaria <= 0:
                    break

            if quantidade_necessaria > 0:
                print(f"Quantidade insuficiente para o consumível {item_pedido.consumivel_id}")
                all_urgent_allocated = False

        if not any_allocated:
            return -1

        return 1 if all_urgent_allocated else 0


    def processar_requerimento(self, requerimento: Requerimento):
        """
        Returns:
        -2: Requerimento inválido, sem consumíveis, ou todos os consumíveis já alocados.
        -1: Não foi possível alocar nenhum consumível.
         0: Alguns consumíveis foram alocados, mas não todos.
         1: Todos os consumíveis foram alocados com sucesso.
        """
        aloc = self.alocar_consumiveis(requerimento.requerimento_id)
        if aloc == -1 or aloc == 0:
            aloc_urgente = -99
            if requerimento.urgente:
                aloc_urgente = self.redistribuir_para_urgente(requerimento.requerimento_id)
                if aloc_urgente == -1:
                    Overlay.show_error(self.parent_window, f"REQ - {requerimento.requerimento_id} Não foi possível alocar os consumíveis para o requerimento urgente.")
                    requerimento.pendete_alocacao = True
                    return False
                elif aloc_urgente == 0:
                    Overlay.show_warning(self.parent_window, f"REQ - {requerimento.requerimento_id} Alguns consumíveis foram alocados, mas não todos.")
                    self.verificar_stock()
                    return True
                elif aloc_urgente == 1:
                    self.verificar_stock()
                    return True
            if aloc == 0 and aloc_urgente == -99:
                Overlay.show_warning(self.parent_window, f"REQ - {requerimento.requerimento_id} Alguns consumíveis foram alocados, mas não todos.")
                requerimento.pendete_alocacao = True
                self.verificar_stock()
                return True
            elif aloc == -1 and aloc_urgente == -99:
                Overlay.show_error(self.parent_window, f"REQ - {requerimento.requerimento_id} Não foi possível alocar nenhum consumível.")
                requerimento.pendete_alocacao = True
                return False
        elif aloc == 1:
            self.verificar_stock()
            return True
        else:
            return False

    def requerimentos_pendentes(self, requerimento_id: int):
        requerimento = next((r for r in self.requerimentos if r.requerimento_id == requerimento_id), None)
        
        if not requerimento:
            return
        
        requerimento.pendete_alocacao = False
        self.requerimento_manager(requerimento, self.parent_window)

    def verificar_stock(self):
        for consumivel in self.consumiveis:
            if consumivel.quantidade_total <= consumivel.quantidade_minima:
                quantidade_para_pedir = consumivel.quantidade_pedido
                #TODO FAZER ISTO DE PEDIDOS EXTERNOS
                #self.criar_pedido_externo(consumivel, quantidade_para_pedir)
                

    def verificar_alocacao(self, requerimento_id: int) -> tuple[bool, list[dict]]:
        requerimento = next((r for r in self.requerimentos if r.requerimento_id == requerimento_id), None)
        
        if requerimento is None:
            return False, []
        
        nao_alocados = []
        for item_pedido in requerimento.itens_pedidos:
            if item_pedido.quantidade != item_pedido.quantidade_alocada:
                consumivel = next((c for c in self.consumiveis if c.consumivel_id == item_pedido.consumivel_id), None)
                if consumivel:
                    nao_alocados.append({
                        "nome_consumivel": consumivel.nome_consumivel,
                        "quantidade_pedida": item_pedido.quantidade,
                        "quantidade_alocada": item_pedido.quantidade_alocada
                    })

        return len(nao_alocados) == 0, nao_alocados


    def criar_pedido_externo(self, consumivel: Consumivel, quantidade: int):
        #TODO FAZER ISTO DA MANEIRA JA IMPLEMENTADA
        #Falta fazer a implemntação da Função do Postgres, Da Route e Ligação com a API
        #VAI SER PRECISO CRIAR UMA TABLEA NO POSTGRES PARA GUARDAR OS PEDIDOS EXTERNOS
        payload = {
            "consumivel_id": consumivel.consumivel_id,
            "fornecedor_nome": "Fornecedor Padrão",
            "quantidade": quantidade
        }
        try:
            print(f"Registrando pedido externo: {payload}")
        except Exception as e:
            print(f"Erro ao registrar pedido externo para o consumível {consumivel.nome_consumivel}: {e}")

    def preparar_dados_alocacao(self, requerimento_id: int) -> dict:
        requerimento = next((r for r in self.requerimentos if r.requerimento_id == requerimento_id), None)
        
        if not requerimento or not requerimento.itens_pedidos:
            return {"requerimento_id": requerimento_id, "consumiveis": []}
        
        consumiveis_alocados = [
            {"consumivel_id": item_pedido.consumivel_id, "quantidade_alocada": item_pedido.quantidade_alocada}
            for item_pedido in requerimento.itens_pedidos
            if item_pedido.quantidade_alocada > 0
        ]
        
        return {
            "requerimento_id": requerimento.requerimento_id,
            "consumiveis": consumiveis_alocados or []
        }

    def requerimento_manager(self, requerimento: Requerimento, parent_page: object) -> list:
        self.parent_window = parent_page
        if requerimento.pendete_alocacao:
            return
        result = self.processar_requerimento(requerimento)
        if result:
            consumiveis_alocados = self.preparar_dados_alocacao(requerimento.requerimento_id)
            asyncio.ensure_future(self.update_consumiveis_alocados(consumiveis_alocados))
            self.data_updated.emit()

    
    async def update_consumiveis_alocados(self,consumiveis_alocados: list):
        requerimento_id=consumiveis_alocados["requerimento_id"]
        consumiveis_alocados=consumiveis_alocados["consumiveis"]
        
        response = await API_UpdateConsumivelAlocado(requerimento_id, consumiveis_alocados)
        if response.success:
            Overlay.show_success(self.parent_window, f"REQ - {requerimento_id} Consumíveis alocados e registados com sucesso.")
        else:
            Overlay.show_error(self.parent_window,  f"REQ - {requerimento_id} Erro ao registar os consumíveis alocados: {response.error_message}")