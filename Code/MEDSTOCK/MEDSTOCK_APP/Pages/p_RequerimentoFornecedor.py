from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QComboBox, QCheckBox,QSizePolicy,QLineEdit
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.Utilizador import Utilizador
from Class.Requerimento import Requerimento
from API.API_GET_Request import API_GetConsumiveisFornecedores,API_GetRequerimentosFornecedor,API_GetConsumiveis
from API.API_POST_Request import API_External_CreatePedidoFornecedor
from API.API_PUT_Request import API_UpdateStockConsumiveis,API_UpdateRequerimentoAlocado
from APP.Card.FornecedorCard import FornecedorCard
from Class.ConsumivelManager import ConsumivelManager
from Class.RequerimentoFornecedor import Requerimento_Fornecedor
from APP.UI.ui_functions import UIFunctions
from Pages.Requerimento.ui_DragAndDrop_Itens import DraggableLabel, DropZone, DropLabel
from Pages.p_Consumiveis import ConsumiveisTablePage
import asyncio
from collections import defaultdict


class RequerimentoFornecedor(QWidget):
    def __init__(self, consumivel_manager: ConsumivelManager , page_stock: ConsumiveisTablePage):
        super().__init__()
        self.page_stock = page_stock
        self.consumivel_manager = consumivel_manager
        self.all_external_consumivel = []
        self.current_requerimentos_externos = []
        self.main_layout = QVBoxLayout(self)
        asyncio.create_task(self.load_requerimentos_fornecedor())
        self.setup_RequerimentoPage()
        
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.load_requerimentos_fornecedor_wrapper)
        self.update_timer.start(60000)

    def setup_RequerimentoPage(self):
        self.setup_page=True
        title_layout = QHBoxLayout()
        self.title = QLabel("PEDIDO FORNECEDORES")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.create_button = QPushButton("NOVO PEDIDO FORNECEDOR")
        self.create_button.setFixedSize(400, 40)
        self.create_button.setStyleSheet(Style.style_bt_QPushButton)
        self.create_button.clicked.connect(self.show_create_fornecedor_page_wrapper)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(50)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        self.setLayout(self.main_layout)


    async def show_create_fornecedor_page(self):
        self.create_page_layout = QVBoxLayout()
        back_button = QPushButton()
        back_button.setFixedSize(100, 40)
        back_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/arrow_back.png", "#b5c6bf")))
        back_button.setStyleSheet(Style.style_bt_QPushButton)
        back_button.clicked.connect(self.reload_page_fornecedor)
        back_button.setText("Voltar")
        back_button.setIconSize(QSize(20, 20))
        self.create_page_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        self.content_layout = QVBoxLayout()
        
        self.create_page_layout.setSpacing(20)
        self.filter_line_edit = QLineEdit()
        self.filter_line_edit.setPlaceholderText("Digite para filtrar os itens...")
        self.filter_line_edit.setFixedHeight(30)
        self.filter_line_edit.setFixedWidth(650)
        self.filter_line_edit.setStyleSheet(Style.style_QlineEdit)
        self.filter_line_edit.textChanged.connect(self.apply_item_filter)
        self.filter_line_edit.setAlignment(Qt.AlignLeft)
        self.content_layout.addWidget(self.filter_line_edit)

        left_frame = QFrame()
        self.left_layout = QGridLayout()
        left_frame.setLayout(self.left_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(left_frame)
        
        asyncio.create_task(self.fetch_consumivel_external())

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        self.drop_zone = DropZone(self)
        shopping_cart_label = DropLabel(self.drop_zone)

        right_layout.addWidget(shopping_cart_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.drop_zone)
        right_layout.addWidget(self.drop_zone.delete_button, alignment=Qt.AlignCenter)

        horizontal_content_layout = QHBoxLayout()
        horizontal_content_layout.addWidget(left_scroll_area)
        horizontal_content_layout.addWidget(right_frame)

        self.content_layout.addLayout(horizontal_content_layout)

    async def requerimentoFornecedor_page(self):
        create_button = QPushButton("Criar Pedido")
        create_button.setFixedSize(500, 40)
        create_button.setStyleSheet(Style.style_bt_QPushButton)
        create_button.clicked.connect(lambda: self.create_pedido(drop_zone=self.drop_zone))
        self.content_layout.addWidget(create_button, alignment=Qt.AlignCenter)
        self.create_page_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.create_page_layout)
        

    async def fetch_consumivel_external(self):
        response = await API_GetConsumiveisFornecedores()
        if response.success:
            self.all_external_consumivel = response.data 
            self.update_item_display(self.all_external_consumivel)
        else:
            Overlay.show_error(self, response.error_message)

    def apply_item_filter(self):
        filter_text = self.filter_line_edit.text().lower()
        filtered_consumivel = [
            item for item in self.all_external_consumivel if filter_text in item.nome_consumivel.lower()
        ]
        self.update_item_display(filtered_consumivel)
        
    def update_item_display(self, consumivel):
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        row, col = 0, 0
        for item in consumivel:
            
            item_label = DraggableLabel(
                consumivel_id=item.consumivel_id,
                nome_consumivel=item.nome_consumivel,
                tipo_consumivel=item.nome_tipo,
                consumivel_quantidade=item.quantidade,
                fornecedor_id=item.fornecedor_id, 
                fornecedor_nome=item.fornecedor_nome
                
            )
            self.left_layout.addWidget(item_label, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1


    def create_pedido(self, drop_zone):
        fornecedores_pedidos = defaultdict(list)

        if drop_zone.rowCount() == 0:
            Overlay.show_error(self, "Adicione pelo menos um consumivel ao pedido!")
            return
        
        for row in range(drop_zone.rowCount()):
            item_widget = drop_zone.item(row, 0)
            consumivel_data = item_widget.data(Qt.UserRole)
            data_parts = consumivel_data.split("|")
            fornecedor_id, fornecedor_nome,consumivel_id, nome_consumivel, quantidade_disponivel = data_parts

            fornecedor_id = int(fornecedor_id) if fornecedor_id.isdigit() else None
            consumivel_id = int(consumivel_id)
            quantidade = drop_zone.cellWidget(row, 1).value()

            if fornecedor_id is not None:
                fornecedores_pedidos[fornecedor_id].append({
                    "fornecedor_nome": fornecedor_nome,
                    "produto_id": consumivel_id,
                    "quantidade": quantidade
                })


        for fornecedor_id, pedidos in fornecedores_pedidos.items():
            response = API_External_CreatePedidoFornecedor(fornecedor_id=fornecedor_id, pedidos=pedidos)
            if response.success:
                fornecedor_nome=pedidos[0]['fornecedor_nome']
                self.reload_page_fornecedor()
                Overlay.show_information(self, f"Pedido ao fornecedor {fornecedor_nome} criado com sucesso!")
            else:
                Overlay.show_error(self, f"Erro ao criar pedido para o fornecedor {fornecedor_nome}: {response.error_message}")


    async def load_requerimentos_fornecedor(self):
        response = await API_GetRequerimentosFornecedor()
        if not response.success:
            Overlay.show_error(self, response.error_message)
            return

        new_requerimentos = response.data

        for novo_requerimento in new_requerimentos:
            existing_requerimento = next(
                (req for req in self.current_requerimentos_externos if req.id_requerimento == novo_requerimento.id_requerimento),
                None
            )

            if existing_requerimento:
                if existing_requerimento != novo_requerimento:
                    self.current_requerimentos_externos.remove(existing_requerimento)
                    self.remove_requerimento_fornecedor_card(existing_requerimento.id_requerimento)
                else:
                    continue


            if novo_requerimento.status == "FINALIZADO" and not novo_requerimento.alocado:
                asyncio.create_task(self.adicionar_consumivel(novo_requerimento))
                API_UpdateRequerimentoAlocado(novo_requerimento.id_requerimento)
                asyncio.create_task(self.load_consumiveis_update())

            self.current_requerimentos_externos.append(novo_requerimento)
            self.add_requerimento_fornecedor_card(novo_requerimento)


    def remove_requerimento_fornecedor_card(self, requerimento_id):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, FornecedorCard) and widget.requerimento_fornecedor.id_requerimento == requerimento_id:
                widget.deleteLater()
            break
            
            
    async def adicionar_consumivel(self, requerimento: Requerimento_Fornecedor):
        try:
            consumiveis = [
                {
                    "nome_consumivel": consumivel.nome,
                    "quantidade": consumivel.quantidade_pedida
                }
                for consumivel in requerimento.consumiveis
            ]
            
            response = await API_UpdateStockConsumiveis(consumiveis)
            
            if response.success:
                Overlay.show_success(self, f"Stock atualizado com sucesso para o requerimento {requerimento.id_requerimento}!")
            else:
                Overlay.show_error(self, f"Erro ao atualizar Stock: {response.error_message}")
        
        except Exception as e:
            Overlay.show_error(self, f"Erro inesperado ao adicionar consumível: {str(e)}")

    def add_requerimento_fornecedor_card(self, requerimento_fornecedor):
        card = FornecedorCard(requerimento_fornecedor,self.consumivel_manager,page_stock=self.page_stock)
        self.scroll_layout.addWidget(card)
        
    async def load_consumiveis_update(self,):
        response = await API_GetConsumiveis()
        if response.success:
            items = response.data
            self.consumivel_manager.add_consumivel(items)
            self.consumivel_manager.realocar_todos_requerimentos()

    def reload_page_fornecedor(self):
        self.clear_layout(self.main_layout)
        self.setup_RequerimentoPage()
        self.load_requerimentos_fornecedor_wrapper()
        
    def load_requerimentos_fornecedor_wrapper(self):
        self.current_requerimentos_externos=[]
        asyncio.create_task(self.load_requerimentos_fornecedor())
        

    def show_create_fornecedor_page_wrapper(self):
        self.clear_layout(self.main_layout)
        asyncio.create_task(self.show_create_fornecedor_page())
        asyncio.create_task(self.requerimentoFornecedor_page())
    
        
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())



