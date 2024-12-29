from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QHBoxLayout, 
    QStyledItemDelegate,QLineEdit
)
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QIntValidator
from PyQt5.QtCore import Qt, QSize, QTimer
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from APP.UI.ui_functions import UIFunctions
from Class.ConsumivelManager import ConsumivelManager
from API.API_GET_Request import API_GetConsumiveis
from API.API_PUT_Request import API_UpdateConsumivel
from APP.PDF.Generate_PDF import GeneratePdfItens
import asyncio
import os

class ConsumiveisTablePage(QWidget):
    def __init__(self,consumivel_manager:ConsumivelManager):
        super().__init__()
        self.consumivel_manager = consumivel_manager
        self.editing_rows = set()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        self.title = QLabel("CONSUMÍVEIS DISPONÍVEIS")
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
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels([
            "Nome", "Tipo", "Código", 
            "Quantidade Total", "Quantidade Alocada", 
            "Quantidade Mínima", "Quantidade Pedido", "Ações"
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

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.load_items_wrapper)
        self.update_timer.start(60000)
        self.current_items = []

        asyncio.ensure_future(self.load_items())

    def load_items_wrapper(self):
        asyncio.ensure_future(self.load_items())
    
    async def load_items(self):
        response = await API_GetConsumiveis()
        if response.success:
            items = response.data
            self.consumivel_manager.add_consumivel(items)
            self.update_table(items)
        else:
            Overlay.show_error(self, response.error_message)

    def update_table(self, items):
        sorted_items = sorted(items, key=lambda item: item.consumivel_id)
        
        if sorted_items != self.current_items:
            self.current_items = sorted_items
            self.table_widget.setRowCount(len(sorted_items))
            self.table_widget.clearContents()

            for row, item in enumerate(self.current_items):
                item_name = QTableWidgetItem(item.nome_consumivel)
                item_name.setData(Qt.UserRole, item.consumivel_id) 
                item_name.setIcon(self.get_item_icon(item.nome_tipo))
                self.table_widget.setItem(row, 0, item_name)
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.nome_tipo))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.codigo))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(item.quantidade_total)))
                self.table_widget.setItem(row, 4, QTableWidgetItem(str(item.quantidade_alocada)))
                
                quantidade_minima_item = QTableWidgetItem(str(item.quantidade_minima))
                quantidade_minima_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(row, 5, quantidade_minima_item)

                quantidade_pedido_item = QTableWidgetItem(str(item.quantidade_pedido))
                quantidade_pedido_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(row, 6, quantidade_pedido_item)

                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)

                edit_button = QPushButton()
                edit_button.setObjectName(f"edit_button_{row}")
                edit_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/edit.png", "#4287f5")))
                edit_button.setIconSize(QSize(30, 30))
                edit_button.setStyleSheet("background-color: transparent; border: none;")
                edit_button.clicked.connect(lambda _, r=row: self.enable_editing(r))
                action_layout.addWidget(edit_button)
                action_widget.setLayout(action_layout)
                self.table_widget.setCellWidget(row, 7, action_widget)
                
            self.table_widget.setItemDelegateForColumn(5, NumericItemDelegate(self.table_widget))
            self.table_widget.setItemDelegateForColumn(6, NumericItemDelegate(self.table_widget))

            self.adjust_column_sizes()


    def enable_editing(self, row):
        if row in self.editing_rows:
            return

        self.update_timer.stop()
        nome_medicamento = self.table_widget.item(row, 0).text() if self.table_widget.item(row, 0) else "Desconhecido"

        self.editing_rows.add(row)

        for column in [5, 6]:
            item = self.table_widget.item(row, column)
            if item:
                item.setData(Qt.UserRole, item.text())

                item.setText("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(QColor("#ffff99")))

        edit_button = self.table_widget.cellWidget(row, 7).findChild(QPushButton, f"edit_button_{row}")
        if edit_button:
            edit_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/check.png", "#32CD32")))
            edit_button.clicked.disconnect()
            edit_button.clicked.connect(lambda _, r=row: asyncio.ensure_future(self.save_changes(r)))


        close_button = QPushButton()
        close_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/close.png", "#f54251")))
        close_button.setIconSize(QSize(30, 30))
        close_button.setStyleSheet("background-color: transparent; border: none;")
        close_button.clicked.connect(lambda _, r=row: self.cancel_editing(r))
        self.table_widget.cellWidget(row, 7).layout().addWidget(close_button)

        Overlay.show_information(self, f"Edição ativada para o medicamento: {nome_medicamento}.")

    async def save_changes(self, row):
        try:
            item_id = self.table_widget.item(row, 0).data(Qt.UserRole)
            quantidade_minima = int(self.table_widget.item(row, 5).text())
            quantidade_pedido = int(self.table_widget.item(row, 6).text())
            
            response = await API_UpdateConsumivel(item_id, quantidade_minima, quantidade_pedido)
            
            if response.success:
                Overlay.show_success(self, "Alterações guardadas com sucesso!")
                self.disable_editing(row)
                self.editing_rows.discard(row)
                if not self.editing_rows:
                    self.update_timer.start()
            else:
                self.cancel_editing(row)
                Overlay.show_error(self, "Erro ao guardar alterações: " + response.error_message)
        except ValueError:
            Overlay.show_error(self, "Valores inválidos. Insira apenas números.")


    def disable_editing(self, row):
        for column in [5, 6]:
            item = self.table_widget.item(row, column)
            if item:
                item.setBackground(QBrush(QColor(Qt.white)))
                item.setForeground(QBrush(QColor(Qt.black)))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        edit_button = self.table_widget.cellWidget(row, 7).findChild(QPushButton, f"edit_button_{row}")
        if edit_button:
            edit_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/edit.png", "#4287f5")))
            edit_button.clicked.disconnect()
            edit_button.clicked.connect(lambda _, r=row: self.enable_editing(r))

        close_button = self.table_widget.cellWidget(row, 7).layout().itemAt(1).widget()
        if close_button:
            close_button.deleteLater()
            
            
    def cancel_editing(self, row):
        for column in [5, 6]:
            item = self.table_widget.item(row, column)
            if item:
                item.setText(item.data(Qt.UserRole))
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(QColor(Qt.white)))
                item.setForeground(QBrush(QColor(Qt.black)))

        self.disable_editing(row)

        self.editing_rows.discard(row)
    
        if not self.editing_rows:
            self.update_timer.start()

        Overlay.show_information(self, "Edição cancelada e valores restaurados.")

    def get_item_icon(self, tipo):
        if tipo == "Medicamento":
            return QIcon("./icons/MaterialIcons/medicamento.png")
        elif tipo == "Vacinas":
            return QIcon("./icons/MaterialIcons/vacina.png")
        elif tipo == "Material Hospitalar":
            return QIcon("./icons/MaterialIcons/material_hospitalar.png")
        else:
            return QIcon("./icons/MaterialIcons/outro.png")

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

    def adjust_column_sizes(self):
        self.table_widget.resizeColumnsToContents()
        header = self.table_widget.horizontalHeader()

        for column in range(self.table_widget.columnCount()):
            header_text = self.table_widget.horizontalHeaderItem(column).text()
            content_width = header.sectionSize(column)
            header_width = self.fontMetrics().boundingRect(header_text).width() + 20
            optimal_width = max(content_width, header_width)
            
            if column >= self.table_widget.columnCount() - 5:
                header.setSectionResizeMode(column, QHeaderView.Stretch)
                self.center_column_content(column)
            else:
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                header.resizeSection(column, optimal_width)

    def center_column_content(self, column):
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, column)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
                
class NumericItemDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignCenter)
        editor.setValidator(QIntValidator(0, 99999999, parent))
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value is not None:
            editor.setText(str(value))
        else:
            editor.clear()

    def setModelData(self, editor, model, index):
        text = editor.text()
        model.setData(index, text, Qt.EditRole)
