from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

class StatusLabel(QWidget):
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
        0: ("A Espera de Aprovação", QColor("grey")),
        1: ("Na Lista de Espera", QColor("orange")),
        2: ("Em Preparação", QColor("#bcbf06")),
        3: ("Pronto para Entrega", QColor("blue")),
        4: ("Finalizado", QColor("green")),
        5: ("Recusado", QColor("red")),
        6: ("Stand-By", QColor("orange")),
        7: ("Cancelado", QColor("red")),
        8: ("Em Validação", QColor("#e3ca0e")),
        9: ("Em Re-Avaliação", QColor("blue")),
        10:("Na Lista de Espera", QColor("orange")),
        11:("Pedido Externo", QColor("red"))
    }
    return status_mapping.get(status, ("Status Desconhecido", QColor("grey")))

def add_status_lable(status):
    status_text, color = get_status_description(status)
    return StatusLabel(status_text, color)

