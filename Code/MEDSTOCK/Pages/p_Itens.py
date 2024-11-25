from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from API.API_GET_Request import API_GetItems
from APP.PDF.Generate_PDF import GeneratePdfItens
import asyncio
import os

class ItemTablePage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        self.title = QLabel("ITENS DISPONÍVEIS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(15)
        
        self.download_button = QPushButton()
        self.download_button.setFixedSize(40, 40)
        icon_path = os.path.abspath("./icons/MaterialIcons/picture_as_pdf.png")
        self.download_button.setIcon(QIcon(icon_path))
        self.download_button.setIconSize(QSize(30, 30))
        self.download_button.setStyleSheet("background-color: transparent; border: 2px solid #F3F3F3;")
        self.download_button.clicked.connect(self.choose_file_location_GeneratePdfItens)
        self.main_layout.addWidget(self.download_button, alignment=Qt.AlignRight)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Tipo", "Código", "Quantidade Disponível"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setFont(QFont("Arial", 11))
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setStyleSheet(Style.style_Table)
        self.table_widget.setShowGrid(False)
        self.table_widget.setGridStyle(Qt.SolidLine)

        self.main_layout.addWidget(self.table_widget)
        asyncio.run(self.load_items())

        QTimer.singleShot(0, lambda: asyncio.ensure_future(self.load_items()))

    async def load_items(self):
        response = await API_GetItems()
        self.table_widget.clearContents()
        if response.success:
            items = response.data
            self.table_widget.setRowCount(len(items))
            for row, item in enumerate(items):
                icon = QIcon()
                if item.nome_tipo == "Medicamento":
                    icon = QIcon("./icons/MaterialIcons/medicamento.png")
                elif item.nome_tipo == "Vacinas":
                    icon = QIcon("./icons/MaterialIcons/vacina.png")
                elif item.nome_tipo == "Material Hospitalar":
                    icon = QIcon("./icons/MaterialIcons/material_hospitalar.png")
                elif item.nome_tipo == "Outros":
                    icon = QIcon("./icons/MaterialIcons/outro.png")

                item_name_with_icon = QTableWidgetItem(item.nome_item)
                item_name_with_icon.setIcon(icon)

                self.table_widget.setItem(row, 0, item_name_with_icon)
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.nome_tipo))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.codigo))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(item.quantidade_disponivel)))
        else:
            Overlay.show_error(self, response.error_message)

    def choose_file_location_GeneratePdfItens(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar PDF", 
            "", 
            "PDF Files (*.pdf);;All Files (*)", 
            options=options
        )
        if file_path:
            GeneratePdfItens(self, self.table_widget, file_path)
            Overlay.show_information(self, "PDF guardado na localização "+file_path)
