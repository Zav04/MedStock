from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

class FornecedorStatusLabel(QWidget):
    def __init__(self, status_text, color):
        super().__init__()
        
        self.setAutoFillBackground(True)
        self.setStyleSheet(f"background-color: {color.name()}; border-radius: 10px;")
        
        label = QLabel(status_text)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumSize(300, 30)
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.setContentsMargins(6, 4, 6, 4)
        self.setLayout(layout)

def get_status_description(status):
    status_mapping = {
        "EM ESPERA": ("Pedido em Espera", QColor("blue")),
        "EM PREPARAÇÃO": ("Em Preparação", QColor("orange")),
        "ENVIADO": ("Pedido Eenviado", QColor("#e3ca0e")),
        "FINALIZADO": ("Finalizado", QColor("green")),
    }
    return status_mapping.get(status, ("Status Desconhecido", QColor("grey")))

def add_status_lable(status):
    status_text, color = get_status_description(status)
    return FornecedorStatusLabel(status_text, color)

