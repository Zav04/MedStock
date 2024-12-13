from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QSpinBox,  QHeaderView, QPushButton
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QFont, QIcon
from PyQt5.QtCore import QMimeData, Qt,QSize
from APP.UI.ui_functions import UIFunctions
from APP.UI.ui_styles import Style


class DraggableLabel(QWidget):
    def __init__(self, consumivel_id, nome_consumivel, tipo_consumivel, quantidade_disponivel):
        super().__init__()
        self.consumivel_id = consumivel_id
        self.nome_consumivel = nome_consumivel
        self.tipo_consumivel = tipo_consumivel
        self.quantidade_disponivel = quantidade_disponivel

        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setAlignment(Qt.AlignCenter)

        if tipo_consumivel == "Medicamento":
            icon_path = "./icons/MaterialIcons/medicamento.png"
        elif tipo_consumivel == "Vacinas":
            icon_path = "./icons/MaterialIcons/vacina.png"
        elif tipo_consumivel == "Material Hospitalar":
            icon_path = "./icons/MaterialIcons/material_hospitalar.png"
        elif tipo_consumivel == "Outros":
            icon_path = "./icons/MaterialIcons/outro.png"
        else:
            icon_path = "./icons/MaterialIcons/default.png"

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio))
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("border: none;")

        self.text_label = QLabel(f"{self.nome_consumivel}")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("color: black; font-weight: bold; font: 14pt Arial; border: none;")

        container_layout.addWidget(self.icon_label)
        container_layout.addWidget(self.text_label)

        container.setStyleSheet("""
            border: 2px dashed #b5c6bf;
            border-radius: 10px;
            background-color: transparent;
        """)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setFixedSize(215, 150)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pixmap = self.create_combined_pixmap()
            mime_data = QMimeData()
            mime_data.setText(f"{self.consumivel_id}|{self.nome_consumivel}|{self.quantidade_disponivel}")

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.MoveAction)

    def create_combined_pixmap(self):
        combined_pixmap = QPixmap(self.width(), self.height())
        combined_pixmap.fill(Qt.transparent)

        painter = QPainter(combined_pixmap)
        self.icon_label.render(painter, targetOffset=self.icon_label.pos())
        self.text_label.render(painter, targetOffset=self.text_label.pos())
        painter.end()
        return combined_pixmap


class DropZone(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Consumivel", "Quantidade"])
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)
        self.setFont(QFont("Arial", 11))
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setStyleSheet(Style.style_Table)
        self.setShowGrid(False)
        self.setGridStyle(Qt.SolidLine)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.selected_row = None

        self.delete_button = QPushButton("Excluir Consumivel")
        self.delete_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/delete_forever.png", "#FFFFFF")))
        self.delete_button.setIconSize(QSize(30, 30))
        self.delete_button.setFixedSize(300, 40)
        self.delete_button.setStyleSheet(Style.style_bt_QPushButton_Delete)
        self.delete_button.hide()
        self.delete_button.clicked.connect(self.delete_selected_row)
        self.itemSelectionChanged.connect(self.show_delete_button)


    def add_consumivel_to_list(self, consumivel_id, consumivel_name, quantidade_disponivel):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == consumivel_name:
                spinbox = self.cellWidget(row, 1)
                
                #TODO QUANDO FOR PARA FAZER SEM LIMITES DE QUANTIDADE
                spinbox.setValue(min(spinbox.value() + 1, quantidade_disponivel))
                #TODO QUANDO FOR PARA FAZER SEM LIMITES DE QUANTIDADE
                return

        row = self.rowCount()
        self.insertRow(row)

        consumivel_widget = QTableWidgetItem(consumivel_name)
        consumivel_widget.setData(Qt.UserRole, consumivel_id)
        self.setItem(row, 0, consumivel_widget)

        spinbox = QSpinBox()
        spinbox.setStyleSheet(Style.style_SpinBox)
        spinbox.setValue(1)
        spinbox.setMinimum(1)
        spinbox.setMaximum(quantidade_disponivel)
        self.setCellWidget(row, 1, spinbox)

    def show_delete_button(self):
        selected_consumivels = self.selectedItems()
        if selected_consumivels:
            self.selected_row = self.currentRow()
            self.delete_button.show()
        else:
            self.delete_button.hide()

    def delete_selected_row(self):
        if self.selected_row is not None:
            self.removeRow(self.selected_row)
            self.selected_row = None
            self.delete_button.hide()
            self.clearSelection()


class DropLabel(QLabel):
    def __init__(self, drop_zone):
        super().__init__()
        self.drop_zone = drop_zone

        self.default_icon = "./icons/MaterialIcons/shopping_cart.png"
        self.hover_icon = "./icons/MaterialIcons/shopping_cart_hover.png"
        self.update_icon(self.default_icon)

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #4CAF50; padding: 10px;")
        self.setFixedWidth(730)
        self.setAcceptDrops(True)

    def update_icon(self, icon_path):
        color_icon = UIFunctions.recolor_icon(icon_path, "#4CAF50")
        self.setPixmap(QPixmap(color_icon).scaled(100, 100, Qt.KeepAspectRatio))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            self.update_icon(self.hover_icon)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.update_icon(self.default_icon)

    def dropEvent(self, event):
        if event.mimeData().hasText():
            data = event.mimeData().text().split("|")
            consumivel_id, consumivel_name, quantidade_disponivel = data[0], data[1], int(data[2])
            self.drop_zone.add_consumivel_to_list(consumivel_id,consumivel_name, quantidade_disponivel)
            self.update_icon(self.default_icon)
            event.accept()
