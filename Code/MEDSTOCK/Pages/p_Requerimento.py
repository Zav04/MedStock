from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QHBoxLayout, QAbstractItemView, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.utilizador import Utilizador
from API.API_GET_Request import API_GetRequerimentosByUser
from APP.Card.Card import RequerimentoCard
from APP.UI.ui_styles import Style
import asyncio



class RequerimentoPage(QWidget):
    def __init__(self, user: Utilizador):
        super().__init__()
        self.user = user

        # Layout principal
        self.main_layout = QVBoxLayout(self)

        # Cabeçalho fixo
        self.setup_header()

        # Cria a área de rolagem
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(Style.style_ScrollBar)

        # Conteúdo da área de rolagem
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)

        # Adiciona a área de rolagem ao layout principal
        self.main_layout.addWidget(self.scroll_area)

        # Configurar a página inicial
        self.setLayout(self.main_layout)
        asyncio.run(self.load_requerimentos(self.user.utilizador_id))

    def setup_header(self):
        """Configura o cabeçalho fixo no topo da página."""
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

        # Adiciona o cabeçalho ao layout principal
        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(15)

    async def load_requerimentos(self, user_id):
        response = await API_GetRequerimentosByUser(user_id)
        if response.success:
            requerimentos = response.data

            for requerimento in requerimentos:
                card = RequerimentoCard(
                    user=self.user,
                    requerimento=requerimento,
                )
                self.scroll_layout.addWidget(card)
        else:
            Overlay.show_error(self, response.error_message)
