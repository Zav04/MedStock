from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QHBoxLayout, QAbstractItemView
from PyQt5.QtGui import QFont, QIcon, QCursor,QColor,QBrush
from PyQt5.QtCore import Qt, QSize
from APP.ui_styles import Style
from Overlays.Overlay import Overlay
from APP.ui_functions import UIFunctions
from Class.utilizador import Utilizador
from Class.requerimento import Requerimento
from Label.Label import add_status_to_table
from API.API_GET_Request import API_GetRequerimentosByUser
from APP.Generate_PDF import GeneratePdfItens
import asyncio
import os
from datetime import datetime

class RequerimentoTablePage(QWidget):
    def __init__(self, user: Utilizador):
        super().__init__()
        self.user=user
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(self.main_layout)
        self.setup_main_layout()
        
        
        
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self.clear_layout(sub_layout)
    def setup_main_layout(self):        
        self.clear_layout(self.main_layout)
        
        title_layout = QHBoxLayout()
        self.title = QLabel("REQUERIMENTOS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.create_button = QPushButton("CRIAR NOVO REQUERIMENTO")
        self.create_button.setFixedSize(400, 40)
        self.create_button.setStyleSheet(Style.style_bt_QPushButton)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(15)


        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels([
            "ID Requerimento", "Setor", "Nome Remetente", 
            "Data do Pedido", "Data de Confirmação", 
            "Data de Envio", "Estado", "Ações"
        ])

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setFont(QFont("Arial", 11))
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        self.table_widget.setStyleSheet(Style.style_Table_Requerimento)

        self.main_layout.addWidget(self.table_widget)
        asyncio.run(self.load_requerimentos(self.user.utilizador_id))
        

    async def load_requerimentos(self, user_id):        
        response = await API_GetRequerimentosByUser(user_id)
        if response.success:
            requerimentos = response.data
            self.table_widget.setRowCount(len(requerimentos))
            for row, requerimento in enumerate(requerimentos):
                self.table_widget.setItem(row, 0, QTableWidgetItem("REQ-" + str(requerimento.requerimento_id)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(requerimento.setor_nome_localizacao or "------------"))
                self.table_widget.setItem(row, 2, QTableWidgetItem(requerimento.nome_utilizador_pedido or "------------"))
                
                data_pedido_str = (
                    datetime.strptime(requerimento.data_pedido, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y %H:%M")
                    if requerimento.data_pedido else "------------"
                )
                self.table_widget.setItem(row, 3, QTableWidgetItem(data_pedido_str))
                
                data_confirmacao_str = (
                    datetime.strptime(requerimento.data_confirmacao, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y %H:%M")
                    if requerimento.data_confirmacao else "------------"
                )
                self.table_widget.setItem(row, 4, QTableWidgetItem(data_confirmacao_str))
                
                
                data_envio_str = (
                    datetime.strptime(requerimento.data_envio, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y %H:%M")
                    if requerimento.data_envio else "------------"
                )
                self.table_widget.setItem(row, 5, QTableWidgetItem(data_envio_str))
                
                add_status_to_table(self.table_widget, row, 6,requerimento.status)
                

                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)

                details_button = QPushButton()
                recolored_icon_details = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/visibility.png"), "#4287f5"))
                details_button.setIcon(recolored_icon_details)
                details_button.setIconSize(QSize(24, 24))
                details_button.setCursor(QCursor(Qt.PointingHandCursor))
                details_button.setStyleSheet(self.button_style("#4287f5"))
                details_button.clicked.connect(lambda _, r=requerimento: self.view_details(r))

                download_button = QPushButton()
                download_button.setIcon(QIcon(os.path.abspath("./icons/MaterialIcons/picture_as_pdf.png")))
                download_button.setIconSize(QSize(24, 24))
                download_button.setCursor(QCursor(Qt.PointingHandCursor))
                download_button.setStyleSheet(self.button_style("#6464FF"))
                download_button.clicked.connect(lambda _, r=requerimento: self.download_pdf(r))

                delete_button = QPushButton()
                recolored_icon_delete = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/close.png"), "#f54251"))
                delete_button.setIcon(recolored_icon_delete)
                delete_button.setIconSize(QSize(24, 24))
                delete_button.setCursor(QCursor(Qt.PointingHandCursor))
                delete_button.setStyleSheet(self.button_style("#f54251"))
                delete_button.clicked.connect(lambda _, r=requerimento: self.delete_item(r))

                action_layout.addWidget(details_button)
                action_layout.addWidget(download_button)
                action_layout.addWidget(delete_button)
                action_layout.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(row, 7, action_widget)

                if requerimento.urgente and requerimento.status <= 3:
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        if item is None:
                            item = QTableWidgetItem("")
                            self.table_widget.setItem(row, col, item)
                        item.setData(Qt.BackgroundRole, QBrush(QColor("#d6b2b2")))
            self.table_widget.viewport().update()
            self.adjust_column_sizes()
        else:
            Overlay.show_error(self, response.error_message)

    def view_details(self, requerimento):
        self.clear_layout(self.main_layout)

        detailed_layout = QVBoxLayout()
        detailed_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel(f"Detalhes do Requerimento ID: {requerimento.requerimento_id}")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        detailed_layout.addWidget(title, alignment=Qt.AlignCenter)

        detalhes = QLabel(f"Setor: {requerimento.setor_nome_localizacao}\n"
                          f"Remetente: {requerimento.nome_utilizador_pedido}\n"
                          f"Data do Pedido: {requerimento.data_pedido}\n"
                          f"Status: {requerimento.status}")
        detalhes.setFont(QFont("Arial", 12))
        detailed_layout.addWidget(detalhes)

        back_button = QPushButton("Voltar")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        back_button.clicked.connect(self.setup_main_layout)
        detailed_layout.addWidget(back_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(detailed_layout)

#TODO GERAR PDF
    def download_pdf(self, row):
        # item_name = self.table_widget.item(row, 0).text()
        options = QFileDialog.Options()
        # file_path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", f"{item_name}.pdf", "PDF Files (*.pdf);;All Files (*)", options=options)
        # if file_path:
        #     GeneratePdfItens(self, self.table_widget, file_path)
        #     Overlay.show_information(self, f"PDF para '{item_name}' gerado com sucesso!")
        Overlay.show_information(self, "IMPLEMENTAR PDF REQUERIMENTO")

#TODO CANCELAR REQUERIMENTO
    def delete_item(self):
            Overlay.show_information(self, "IMPLEMENTAR DELETE REQUERIMENTO")
    
    
    def adjust_column_sizes(self):
        header = self.table_widget.horizontalHeader()
        for col in range(self.table_widget.columnCount()):
            max_content_width = max(self.table_widget.sizeHintForColumn(col), header.sectionSizeHint(col))
            if max_content_width > header.sectionSizeHint(col):
                header.setSectionResizeMode(col, QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)

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
