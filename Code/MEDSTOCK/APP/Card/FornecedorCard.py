from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QCursor,QPixmap
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
from Class.RequerimentoFornecedor import RequerimentoFornecedor
from Pages.p_Consumiveis import ConsumiveisTablePage
from Class.ConsumivelManager import ConsumivelManager
from APP.UI.ui_functions import UIFunctions
from APP.UI.ui_styles import Style
import os
import asyncio
from APP.Label.Label_Fornecedor import add_status_lable
from APP.Overlays.Overlay import Overlay


class FornecedorCard(QWidget):
    def __init__(self,requerimento_fornecedor: RequerimentoFornecedor,consumivel_manager: ConsumivelManager, page_stock : ConsumiveisTablePage):
        super().__init__()
        self.consumivel_manager = consumivel_manager
        self.page_stock = page_stock
        self.requerimento_fornecedor = requerimento_fornecedor
        self.expanded = False
        self.minimumHeight_Card = 180
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.layout().setSpacing(5)

        # Container principal
        self.container = QFrame()
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setStyleSheet("background-color: #F3F3F3; border: 1px solid #ddd; border-radius: 8px;")
        self.container.setMaximumHeight(self.minimumHeight_Card)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 15, 15, 15)
        self.container_layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        # Esquerda: ID e Data
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        id_label = QLabel(f"REQ-{self.requerimento_fornecedor.id_requerimento} - {self.requerimento_fornecedor.fornecedor_nome}")
        id_label.setFont(QFont("Arial", 16, QFont.Bold))
        id_label.setStyleSheet("color: #333;border:none;")
        left_layout.addWidget(id_label)

        data_pedido = (
            datetime.strptime(requerimento_fornecedor.data_requerimento, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M")
            if requerimento_fornecedor.data_requerimento else "------------"
        )
        data_label = QLabel(data_pedido)
        data_label.setFont(QFont("Arial", 12))
        data_label.setStyleSheet("color: #555;border:none;")
        left_layout.addWidget(data_label)
        header_layout.addLayout(left_layout)

        # Centro: Status
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)

        status_label = add_status_lable(self.requerimento_fornecedor.status)
        status_layout.addWidget(status_label, alignment=Qt.AlignCenter)

        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addLayout(status_layout)
        

        header_layout.addLayout(center_layout)

        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.setAlignment(Qt.AlignRight)

        self.details_button = QPushButton()
        recolored_icon_details = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/visibility.png"), "#4287f5"))
        self.details_button.setIcon(recolored_icon_details)
        self.details_button.setIconSize(QSize(24, 24))
        self.details_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.details_button.setStyleSheet(self.button_style("#4287f5"))
        self.details_button.clicked.connect(self.toggle_details)
        actions_layout.addWidget(self.details_button, alignment=Qt.AlignRight)

        header_layout.addLayout(actions_layout)
        self.container_layout.addLayout(header_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVisible(False)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.details_frame = QFrame()
        self.details_frame.setStyleSheet("border: none;")
        self.details_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.details_layout = QVBoxLayout(self.details_frame)
        self.details_layout.setContentsMargins(10, 10, 10, 10)
        self.details_layout.setSpacing(5)


        if self.requerimento_fornecedor.consumiveis:
            for item in self.requerimento_fornecedor.consumiveis:
                nome_consumivel = item.nome or "Item desconhecido"
                quantidade = item.quantidade_pedida or "Quantidade não especificada"
                tipo_item = item.categoria or "Tipo não especificado"
                if tipo_item == "Medicamento":
                    icon_path = "./icons/MaterialIcons/medicamento.png"
                elif tipo_item == "Vacinas":
                    icon_path = "./icons/MaterialIcons/vacina.png"
                elif tipo_item == "Material Hospitalar":
                    icon_path = "./icons/MaterialIcons/material_hospitalar.png"
                elif tipo_item == "Outros":
                    icon_path = "./icons/MaterialIcons/outro.png"
                else:
                    icon_path = None
                item_layout = QHBoxLayout()
                if icon_path:
                    icon_label = QLabel()
                    icon_label.setPixmap(QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    icon_label.setFixedSize(20, 20)
                    item_layout.addWidget(icon_label)
                item_text_label = QLabel()
                item_text_label.setText(
                    f"<span style='font-size:14px; color:#000000;'>"
                    f"{nome_consumivel}</span> "
                    f"<span style='font-size:14px; color:#555555;'>(Quantidade: {quantidade})</span>"
                )
                item_text_label.setFont(QFont("Arial"))
                item_layout.addWidget(item_text_label)
                self.details_layout.addLayout(item_layout)
        else:                
            no_items_label = QLabel("<span style='font-size:14px; color:#555555;'>Nenhum item pedido.</span>")
            no_items_label.setFont(QFont("Arial"))
            no_items_label.setTextFormat(Qt.RichText)
            self.details_layout.addWidget(no_items_label)


        self.details_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.details_frame.setLayout(self.details_layout)
        self.scroll_area.setWidget(self.details_frame)
        self.container_layout.addWidget(self.scroll_area)
        self.layout().addWidget(self.container)
        

    def toggle_details(self):
        self.expanded = not self.expanded

        if self.expanded:
            self.scroll_area.setVisible(True)
            self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.container.setMaximumHeight(500)
            self.scroll_area.setMaximumHeight(500)
        else:
            self.scroll_area.setVisible(False)
            self.container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.container.setMaximumHeight(self.minimumHeight_Card)
        
        self.container.updateGeometry()
        self.updateGeometry()


    def get_top_parent(widget):
        parent = widget
        while parent.parentWidget() is not None:
            parent = parent.parentWidget()
        return parent

    @staticmethod
    def button_style(color):
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:], 16)}, 51);
            }}
            QPushButton:pressed {{
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:], 16)}, 127);
            }}
        """
        
