from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QComboBox,
    QWidget, QFrame, QTableWidget, QTableWidgetItem, QAbstractItemView, QSpinBox
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap


class DraggableLabel(QLabel):
    def __init__(self, text, item_name):
        super().__init__(text)
        self.item_name = item_name
        self.setPixmap(QPixmap("./icons/item_icon.png").scaled(64, 64, Qt.KeepAspectRatio))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.setFixedSize(100, 100)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            mime_data = QMimeData()
            mime_data.setText(self.item_name)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap())
            drag.setHotSpot(event.pos())

            drag.exec_(Qt.MoveAction)


class DropZone(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Item", "Quantidade"])
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setStyleSheet("border: 1px solid black;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        item_name = event.mimeData().text()
        self.add_item_to_list(item_name)
        event.accept()

    def add_item_to_list(self, item_name):
        # Verificar se o item já existe na tabela
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == item_name:
                spinbox = self.cellWidget(row, 1)
                spinbox.setValue(spinbox.value() + 1)
                return

        # Adicionar nova linha para o item
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(item_name))

        spinbox = QSpinBox()
        spinbox.setValue(1)
        spinbox.setMinimum(1)
        self.setCellWidget(row, 1, spinbox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão de Requerimentos")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QHBoxLayout()

        # Itens no lado esquerdo
        left_frame = QFrame()
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)

        for i in range(1, 9):
            item_label = DraggableLabel(f"Item{i}", f"Item{i}")
            left_layout.addWidget(item_label)

        # Drop Zone no lado direito
        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        drop_zone = DropZone()
        right_layout.addWidget(drop_zone)

        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
