from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.utilizador import Utilizador
from API.API_GET_Request import API_GetRequerimentosByUser, API_GetRequerimentosByResponsavel
from API.API_GET_Request import API_GetSectors, API_GetItems
from APP.Card.Card import RequerimentoCard
from APP.UI.ui_functions import UIFunctions
from Pages.Requerimento.ui_DragAndDrop_Itens import DraggableLabel, DropZone, DropLabel
import asyncio


class RequerimentoPage(QWidget):
    def __init__(self, user: Utilizador):
        super().__init__()
        self.user = user
        self.main_layout = QVBoxLayout(self)
        self.setup_RequerimentoPage()
        QTimer.singleShot(0, self.load_requerimentos_wrapper)

    def setup_RequerimentoPage(self):
        title_layout = QHBoxLayout()

        self.title = QLabel("REQUERIMENTOS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.create_button = QPushButton("CRIAR NOVO REQUERIMENTO")
        self.create_button.setFixedSize(400, 40)
        self.create_button.setStyleSheet(Style.style_bt_QPushButton)
        self.create_button.clicked.connect(self.show_create_requerimento_page_wrapper)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        if self.user.role_nome == "Gestor Responsável" or self.user.role_nome == "Farmacêutico":
            self.create_button.hide()

        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(15)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)


    async def show_create_requerimento_page(self):
        self.clear_layout(self.main_layout)

        create_page_layout = QVBoxLayout()

        back_button = QPushButton()
        back_button.setFixedSize(100, 40)
        back_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/arrow_back.png", "#b5c6bf")))
        back_button.setStyleSheet(Style.style_bt_QPushButton)
        back_button.clicked.connect(self.reload_requerimentos)
        back_button.setText("Voltar")
        back_button.setIconSize(QSize(20, 20))
        create_page_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        content_layout = QVBoxLayout()

        left_frame = QFrame()
        left_layout = QGridLayout()
        left_frame.setLayout(left_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(left_frame)

        asyncio.create_task(self.fetch_items(left_layout))

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        drop_zone = DropZone(self)
        shopping_cart_label = DropLabel(drop_zone)

        right_layout.addWidget(shopping_cart_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(drop_zone)
        right_layout.addWidget(drop_zone.delete_button, alignment=Qt.AlignCenter)

        horizontal_content_layout = QHBoxLayout()
        horizontal_content_layout.addWidget(left_scroll_area)
        horizontal_content_layout.addWidget(right_frame)

        content_layout.addLayout(horizontal_content_layout)

        self.sector_input = QComboBox()
        self.sector_input.setFixedSize(500, 40)
        self.sector_input.setStyleSheet(Style.style_QComboBox)
        content_layout.addWidget(self.sector_input, alignment=Qt.AlignCenter)

        asyncio.create_task(self.update_sectors())

        create_button = QPushButton("Criar Requerimento")
        create_button.setFixedSize(500, 40)
        create_button.setStyleSheet(Style.style_bt_QPushButton)
        create_button.clicked.connect(lambda: self.create_requerimento(drop_zone))

        content_layout.addWidget(create_button, alignment=Qt.AlignCenter)

        create_page_layout.addLayout(content_layout)

        self.main_layout.addLayout(create_page_layout)


    async def fetch_items(self, left_layout):
        response = await API_GetItems()
        if response.success:
            items = response.data
            for i in reversed(range(left_layout.count())):
                widget = left_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            row, col = 0, 0
            for item in items:
                item_label = DraggableLabel(
                    item_id=item.item_id,
                    nome_item=item.nome_item,
                    tipo=item.nome_tipo,
                    quantidade_disponivel=item.quantidade_disponivel
                )
                left_layout.addWidget(item_label, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
        else:
            Overlay.show_error(self, response.error_message)

    def create_requerimento(self, drop_zone):
        requerimento_items = []
        for row in range(drop_zone.rowCount()):
            item_widget = drop_zone.item(row, 0)
            item_id = item_widget.data(Qt.UserRole)
            item_name = item_widget.text()
            quantidade = drop_zone.cellWidget(row, 1).value()
            requerimento_items.append({
                "item_id": item_id,
                "item_name": item_name,
                "quantidade": quantidade
            })

        setor_selecionado = self.sector_input.currentText()
        setor_id = self.sector_input.currentData()

        print(f"Setor Selecionado: {setor_selecionado} (ID: {setor_id})")
        print("Itens do Requerimento:", requerimento_items)

        self.reload_requerimentos()

    async def load_requerimentos(self, user: Utilizador):
        if user.role_nome == "Gestor Responsável":
            response = await API_GetRequerimentosByResponsavel(user.utilizador_id)
        else:
            response = await API_GetRequerimentosByUser(user.utilizador_id)

        if response.success:
            self.clear_layout(self.scroll_layout)
            requerimentos = response.data
            for requerimento in requerimentos:
                QTimer.singleShot(0, lambda req=requerimento: self.add_requerimento_card(req))
        else:
            Overlay.show_error(self, response.error_message)

    def add_requerimento_card(self, requerimento):
        card = RequerimentoCard(user=self.user, requerimento=requerimento)
        self.scroll_layout.addWidget(card)

    def reload_requerimentos(self):
        self.clear_layout(self.main_layout)
        self.setup_RequerimentoPage()
        QTimer.singleShot(0, self.load_requerimentos_wrapper)

    async def update_sectors(self):
        response = await API_GetSectors()
        if response.success:
            QTimer.singleShot(0, lambda: self.create_sectors(response.data))
        else:
            Overlay.show_error(self, response.error_message)

    def create_sectors(self, sectors):
        self.sector_input.clear()
        self.sector_input.addItem("Selecionar Setor", None)
        for sector in sectors:
            self.sector_input.addItem(f"{sector.nome_setor} - {sector.localizacao}", sector.setor_id)


            
    def load_requerimentos_wrapper(self):
        asyncio.ensure_future(self.load_requerimentos(self.user))
    
    
    def update_sectors_wrapper(self):
        asyncio.ensure_future(self.update_sectors())
    
    
    def show_create_requerimento_page_wrapper(self):
        asyncio.ensure_future(self.show_create_requerimento_page())
    
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

