
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from API.API_GET_Request import API_GetRealocacoes
from APP.UI.ui_functions import UIFunctions
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from APP.PDF.Generate_PDF import GeneratePdfRealocacoes
import os
import asyncio
from datetime import datetime

class RealocacoesTablePage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_realocations = []
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        self.title = QLabel("REALOCAÇÕES")
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
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels([
            "Requerimento Origem", "Requerimento Destino", 
            "Nome Consumível", "Quantidade Realocada", "Data"
        ])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setFont(QFont("Arial", 11))
        self.table_widget.setSelectionMode(QTableWidget.NoSelection)
        self.table_widget.setStyleSheet(Style.style_Table)
        self.table_widget.setShowGrid(False)
        self.table_widget.setGridStyle(Qt.SolidLine)
        self.main_layout.addWidget(self.table_widget)
        
        UIFunctions.adjust_column_sizes(self.table_widget)
        
        asyncio.ensure_future(self.load_realocacoes())
        
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.load_realocacoes_wrapper)
        self.update_timer.start(60000)
        

    def load_realocacoes_wrapper(self):
        asyncio.ensure_future(self.load_realocacoes())

    async def load_realocacoes(self):
        response = await API_GetRealocacoes()
        if response.success:
            self.update_table(response.data)

    def update_table(self, rows):
        
        sorted_items = sorted(rows, key=lambda item: item.requerimento_origem)
        
        if sorted_items != self.current_realocations:
            self.current_realocations = sorted_items
            self.table_widget.setRowCount(len(rows))
            self.table_widget.clearContents()

            for row_index, row in enumerate(rows):
                origem_item = QTableWidgetItem(f"REQ- {str(row.requerimento_origem)}")
                origem_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, 0, origem_item)

                destino_item = QTableWidgetItem(f"REQ- {str(row.requerimento_destino)}")
                destino_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, 1, destino_item)

                consumivel_item = QTableWidgetItem(row.nome_consumivel)
                consumivel_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, 2, consumivel_item)

                quantidade_item = QTableWidgetItem(str(row.quantidade))
                quantidade_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, 3, quantidade_item)

                data_item = QTableWidgetItem(
                    datetime.strptime(row.data_redistribuicao, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')
                )
                data_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, 4, data_item)
            
    def choose_file_location_GeneratePdfItens(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar PDF", 
            "", 
            "PDF Files (*.pdf);;All Files (*)", 
            options=options
        )
        self.requeri
        if file_path:
            GeneratePdfRealocacoes(self, self.table_widget, file_path)
            Overlay.show_information(self, "PDF de Realocações Guardado na Localização " + file_path)
