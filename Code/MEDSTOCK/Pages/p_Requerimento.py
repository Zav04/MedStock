from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QScrollArea, QGridLayout, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.utilizador import Utilizador
from API.API_GET_Request import API_GetRequerimentosByUser, API_GetRequerimentosByResponsavel
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
        QTimer.singleShot(0, self.schedule_load_requerimentos)

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
        self.create_button.clicked.connect(self.show_create_requerimento_page)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

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

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def show_create_requerimento_page(self):
        # Limpa a janela atual
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

        content_layout = QHBoxLayout()

        left_frame = QFrame()
        left_layout = QGridLayout()
        left_frame.setLayout(left_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(left_frame)

        row, col = 0, 0
        for i in range(1, 101):
            item_label = DraggableLabel(f"Item{i}", f"Item{i}")
            left_layout.addWidget(item_label, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        drop_zone = DropZone(self)
        shopping_cart_label = DropLabel(drop_zone)

        right_layout.addWidget(shopping_cart_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(drop_zone)

        content_layout.addWidget(left_scroll_area)
        content_layout.addWidget(right_frame)

        create_page_layout.addLayout(content_layout)

        save_button = QPushButton("Salvar Requerimento")
        save_button.setFixedSize(200, 40)
        save_button.setStyleSheet(Style.style_bt_QPushButton)
        save_button.clicked.connect(lambda: self.save_requerimento(drop_zone))

        create_page_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(create_page_layout)


    def save_requerimento(self, drop_zone):
        requerimento_items = []
        for row in range(drop_zone.rowCount()):
            item_name = drop_zone.item(row, 0).text()
            quantidade = drop_zone.cellWidget(row, 1).value()
            requerimento_items.append((item_name, quantidade))

        print("Itens do Requerimento:", requerimento_items)
        self.reload_requerimentos()

    def schedule_load_requerimentos(self):
        asyncio.ensure_future(self.load_requerimentos(self.user))

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
        QTimer.singleShot(0, self.schedule_load_requerimentos)
