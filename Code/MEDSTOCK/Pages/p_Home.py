from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(10, 30, 10, 30)

        title = QLabel("<span style='color: #C0C0C0;'>BEM-VINDO</span><br><span style='color: #C0C0C0;'>AO</span><br><span style='color: #89c379;'>MEDSTOCK</span>")
        title_font = QFont("Arial", 40, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)


        main_layout.addStretch(1)


        box_layout = QHBoxLayout()
        box_layout.setSpacing(15)
        box_layout.setAlignment(Qt.AlignCenter)

        def create_box(icon_name, count, label_text):
            box = QFrame()
            box.setFixedWidth(220)
            box.setMinimumHeight(230)
            box.setFrameShape(QFrame.StyledPanel)
            box.setStyleSheet("""
                background-color: #d5d5d5; 
                border-radius: 15px; 
                color: #FFFFFF; 
                padding: 10px;
            """)

            box_layout = QVBoxLayout(box)
            box_layout.setAlignment(Qt.AlignCenter)
            box_layout.setSpacing(8)

            icon_path = os.path.abspath(icon_name)
            icon_label = QLabel()
            icon_pixmap = QPixmap(icon_path)
            icon_pixmap = icon_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(icon_label)

            count_label = QLabel(str(count))
            count_font = QFont("Arial", 22, QFont.Bold)
            count_label.setFont(count_font)
            count_label.setAlignment(Qt.AlignCenter)
            count_label.setStyleSheet("color: #89c379;")
            box_layout.addWidget(count_label)

            text_label = QLabel(label_text)
            text_label.setWordWrap(True)
            text_font = QFont("Arial", 12)
            text_label.setFont(text_font)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
            box_layout.addWidget(text_label)

            footer_label = QLabel("*Dados Ilustrativos")
            footer_label.setAlignment(Qt.AlignCenter)
            footer_label.setStyleSheet("color: #89c379; font-size: 11px; margin-top: 15px; font-weight: bold;")
            box_layout.addWidget(footer_label)

            return box


        boxes = [
            create_box('./icons/MaterialIcons/description.png', 99, "Total de Pedidos"),
            create_box('./icons/MaterialIcons/pending_actions.png', 199, "Pedidos em Espera de Aprovação"),
            create_box('./icons/MedStock/favicon.png', 29, "Pedidos em Aberto"),
            create_box('./icons/MedStock/favicon.png', 9, "Pedidos Pendentes"),
            create_box('./icons/MaterialIcons/assignment_turned.png', 373, "Pedidos Finalizados")
        ]

        for i, box in enumerate(boxes):
            box_layout.addWidget(box)
            if i < len(boxes) - 1:
                spacer = QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
                box_layout.addItem(spacer)

        main_layout.addLayout(box_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)
