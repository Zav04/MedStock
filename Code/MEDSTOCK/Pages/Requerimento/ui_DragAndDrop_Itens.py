from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QSpinBox, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QFont
from PyQt5.QtCore import QMimeData, Qt
from APP.UI.ui_functions import UIFunctions
from APP.UI.ui_styles import Style


class DraggableLabel(QWidget):
    def __init__(self, text, item_name):
        super().__init__()
        self.item_name = item_name

        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("./icons/MaterialIcons/assignment_turned.png").scaled(64, 64, Qt.KeepAspectRatio))
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("border: none;")

        self.text_label = QLabel(text)
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
        self.setFixedSize(200, 150)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pixmap = self.create_combined_pixmap()
            mime_data = QMimeData()
            mime_data.setText(self.item_name)

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
        self.setHorizontalHeaderLabels(["Item", "Quantidade"])
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)
        self.setFont(QFont("Arial", 11))
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setStyleSheet(Style.style_Table)
        self.setShowGrid(False)
        self.setGridStyle(Qt.SolidLine)
        #self.setAcceptDrops(True)

    def add_item_to_list(self, item_name):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == item_name:
                spinbox = self.cellWidget(row, 1)
                spinbox.setValue(spinbox.value() + 1)
                return

        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(item_name))

        spinbox = QSpinBox()
        spinbox.setValue(1)
        spinbox.setMinimum(1)
        spinbox.setMaximum(999999)
        self.setCellWidget(row, 1, spinbox)


class DropLabel(QLabel):
    def __init__(self, drop_zone):
        super().__init__()
        self.drop_zone = drop_zone

        shopping_cart = "./icons/MaterialIcons/shopping_cart.png"
        color_icon = UIFunctions.recolor_icon(shopping_cart, "#4CAF50")
        self.setPixmap(QPixmap(color_icon).scaled(100, 100, Qt.KeepAspectRatio))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #4CAF50; padding: 10px;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        item_name = event.mimeData().text()
        self.drop_zone.add_item_to_list(item_name)
        event.accept()
