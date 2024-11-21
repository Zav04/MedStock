from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QHBoxLayout, QAbstractItemView, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.utilizador import Utilizador
from API.API_GET_Request import API_GetRequerimentosByUser,API_GetRequerimentosByResponsavel
from APP.Card.Card import RequerimentoCard
from APP.UI.ui_styles import Style
import asyncio



class RequerimentoPage(QWidget):
    def __init__(self, user: Utilizador):
        super().__init__()
        self.user = user

        self.main_layout = QVBoxLayout(self)

        self.setup_header()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(Style.style_ScrollBar)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)
        QTimer.singleShot(0, self.schedule_load_requerimentos)

    def setup_header(self):
        title_layout = QHBoxLayout()
        self.title = QLabel("REQUERIMENTOS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.create_button = QPushButton("CRIAR NOVO REQUERIMENTO")
        self.create_button.setFixedSize(400, 40)
        self.create_button.setStyleSheet(Style.style_bt_QPushButton)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(15)

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
        card = RequerimentoCard(
            user=self.user,
            requerimento=requerimento,
        )
        self.scroll_layout.addWidget(card)
    
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def reload_requerimentos(self):
        asyncio.ensure_future(self.load_requerimentos(self.user))
