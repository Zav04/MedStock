from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from APP.Ui_Styles import Style
from Overlays.Overlay import Overlay
from API.API_GET_Request import API_GetItems
import asyncio

class ItemTablePage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 30, 20, 30)

        self.title = QLabel("Itens Disponíveis")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.main_layout.addWidget(self.title)

        self.main_layout.addSpacing(15)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Tipo", "Código", "Quantidade Disponível"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setGridStyle(1)
        self.table_widget.setFont(QFont("Arial", 11))
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setStyleSheet(Style.style_Table)

        self.table_widget.setShowGrid(False)
        self.table_widget.setGridStyle(Qt.SolidLine)

        self.main_layout.addWidget(self.table_widget)

        asyncio.run(self.load_items())

    async def load_items(self):
        response = await API_GetItems()
        if response.success:
            items = response.data
            self.table_widget.setRowCount(len(items))
            for row, item in enumerate(items):
                self.table_widget.setItem(row, 0, QTableWidgetItem(item.nome_item))
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.nome_tipo))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.codigo))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(item.quantidade_disponivel)))
        else:
            Overlay.show_error(self, response.error_message)
