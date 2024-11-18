from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QFont, QIcon, QCursor,QPixmap
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
from Class.requerimento import Requerimento
from Class.utilizador import Utilizador
from APP.UI.ui_functions import UIFunctions
import os
from APP.Label.Label import add_status_lable


class RequerimentoCard(QWidget):
    def __init__(self, user:Utilizador, requerimento: Requerimento):
        super().__init__()
        self.requerimento = requerimento
        self.expanded = False

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.layout().setSpacing(5)

        # Container principal
        self.container = QFrame()
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setStyleSheet("background-color: #F3F3F3; border: 1px solid #ddd; border-radius: 8px;")
        self.container.setMaximumHeight(120)
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
        id_label = QLabel(f"REQ-{requerimento.requerimento_id}")
        id_label.setFont(QFont("Arial", 16, QFont.Bold))
        id_label.setStyleSheet("color: #333;border:none;")
        left_layout.addWidget(id_label)

        data_pedido = (
            datetime.strptime(requerimento.data_pedido, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y %H:%M")
            if requerimento.data_pedido else "------------"
        )
        data_label = QLabel(data_pedido)
        data_label.setFont(QFont("Arial", 12))
        data_label.setStyleSheet("color: #555;border:none;")
        left_layout.addWidget(data_label)
        header_layout.addLayout(left_layout)

        # Centro: Status
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        status_label = add_status_lable(requerimento.status)
        status_layout.addWidget(status_label, alignment=Qt.AlignCenter)
        header_layout.addLayout(status_layout)

        # Direita: Botões de ação
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.setAlignment(Qt.AlignRight)

        if requerimento.status == 0:
            delete_button = QPushButton()
            recolored_icon_delete = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/close.png"), "#f54251"))
            delete_button.setIcon(recolored_icon_delete)
            delete_button.setIconSize(QSize(24, 24))
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setStyleSheet(self.button_style("#f54251"))
            #delete_button.clicked.connect(lambda: delete_item_callback(requerimento))
            actions_layout.addWidget(delete_button, alignment=Qt.AlignRight)

        download_button = QPushButton()
        download_button.setIcon(QIcon("./icons/MaterialIcons/picture_as_pdf.png"))
        download_button.setIconSize(QSize(24, 24))
        download_button.setCursor(QCursor(Qt.PointingHandCursor))
        download_button.setStyleSheet(self.button_style("#f54251"))
        #download_button.clicked.connect(lambda: download_pdf_callback(requerimento))
        actions_layout.addWidget(download_button, alignment=Qt.AlignRight)

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

        # Detalhes ocultos
        self.details_frame = QFrame()
        self.details_frame.setStyleSheet("border: none;")
        self.details_frame.setVisible(False)
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(10, 10, 10, 10)
        details_layout.setSpacing(5)

        setor_label = QLabel()
        setor_label.setText(f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Setor:</span> <span style='font-size:14px; color:#000000;'>{requerimento.setor_nome_localizacao or 'Não especificado'}</span>")
        setor_label.setFont(QFont("Arial"))
        details_layout.addWidget(setor_label)

        utilizador_pedido_label = QLabel()
        utilizador_pedido_label.setText(
            f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Solicitado por:</span> "
            f"<span style='font-size:14px; color:#555555;'>{requerimento.nome_utilizador_pedido or 'Desconhecido'}</span>"
        )
        utilizador_pedido_label.setFont(QFont("Arial"))
        details_layout.addWidget(utilizador_pedido_label)

        itens_label = QLabel()
        itens_label.setText(
            "<span style='font-size:16px; font-weight:bold; color:#000000;'>Itens Pedidos:</span>"
        )
        itens_label.setFont(QFont("Arial"))
        details_layout.addWidget(itens_label)


        if requerimento.itens_pedidos:
            for item in requerimento.itens_pedidos:
                nome_item = item.nome_item or "Item desconhecido"
                quantidade = item.quantidade or "Quantidade não especificada"
                tipo_item = item.tipo_item or "Tipo não especificado"

                # Seleciona o ícone correspondente
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
                    f"{nome_item}</span> "
                    f"<span style='font-size:14px; color:#555555;'>(Quantidade: {quantidade})</span>"
                )
                item_text_label.setFont(QFont("Arial"))
                item_layout.addWidget(item_text_label)

                details_layout.addLayout(item_layout)
        else:
            no_items_label = QLabel("<span style='font-size:14px; color:#555555;'>Nenhum item pedido.</span>")
            no_items_label.setFont(QFont("Arial"))
            no_items_label.setTextFormat(Qt.RichText)
            details_layout.addWidget(no_items_label)

        if requerimento.nome_utilizador_confirmacao and requerimento.data_confirmacao:
            confirmacao_label = QLabel()
            confirmacao_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>"
                f"Confirmado por:</span> "
                f"<span style='font-size:14px; color:#555555;'>{requerimento.nome_utilizador_confirmacao}</span> "
                f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(requerimento.data_confirmacao, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
            )
            confirmacao_label.setFont(QFont("Arial"))
            details_layout.addWidget(confirmacao_label)

        if requerimento.nome_utilizador_envio and requerimento.data_envio:
            envio_label = QLabel()
            envio_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>"
                f"Enviado por:</span> "
                f"<span style='font-size:14px; color:#555555;'>{requerimento.nome_utilizador_envio}</span> "
                f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(requerimento.data_envio, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
            )
            envio_label.setFont(QFont("Arial"))
            details_layout.addWidget(envio_label)


        self.container_layout.addWidget(self.details_frame)
        self.layout().addWidget(self.container)
        
        
        if requerimento.urgente and requerimento.status <=3:
            self.container.setStyleSheet("background-color: #f8d7da; border: 1px solid #f5c2c7; border-radius: 8px;")



    def toggle_details(self):
        self.expanded = not self.expanded
        self.details_frame.setVisible(self.expanded)
        self.container.setMaximumHeight(300 if self.expanded else 120)

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
