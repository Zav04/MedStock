import random
import string
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from APP.UI.ui_styles import Style
from API.API_GET_Request import API_GetAllTipoConsumiveis
from API.API_POST_Request import API_CreateConsumivel
from APP.Overlays.Overlay import Overlay
import asyncio



class CreateConsumivelPage(QWidget):
    def __init__(self):
        super().__init__()
        self.tipos=[]
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 30, 20, 30)

        self.title = QLabel("ADICIONAR NOVO  CONSUMIVEL")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(15)

        self.font_Label=QFont("Arial", 12)
        
        self.name_label = QLabel("Nome")
        self.name_label.setFont(self.font_Label)
        self.name_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setFixedSize(500, 40)
        self.name_input.setPlaceholderText("Insira o nome do Consumivel")
        self.name_input.setStyleSheet(Style.style_QlineEdit)

        self.codigo_label = QLabel("Codigo")
        self.codigo_label.setFont(self.font_Label)
        self.codigo_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.codigo_input = QLineEdit()
        self.codigo_input.setFixedSize(500, 40)
        self.codigo_input.setMaxLength(33)
        self.codigo_input.setPlaceholderText("Insira o codigo do Consumivel")
        self.codigo_input.setStyleSheet(Style.style_QlineEdit)

        self.tipo_label = QLabel("Tipo de Consumivel")
        self.tipo_label.setFont(self.font_Label)
        self.tipo_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.tipo_input = QComboBox()
        self.tipo_input.setFixedSize(500, 40)
        self.tipo_input.setStyleSheet(Style.style_QComboBox)

        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.addWidget(self.name_label)
        self.form_layout.addWidget(self.name_input)
        self.form_layout.addWidget(self.codigo_label)
        self.form_layout.addWidget(self.codigo_input)
        self.form_layout.addWidget(self.tipo_label)
        self.form_layout.addWidget(self.tipo_input)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addSpacing(20)
        
        self.register_button = QPushButton("Criar")
        self.register_button.setFixedSize(150, 40)
        self.register_button.setStyleSheet(Style.style_bt_QPushButton)
        self.register_button.clicked.connect(self.criar_consumiveis)
        self.main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.update_tipos_thread = QTimer(self)
        self.update_tipos_thread.timeout.connect(self.update_tipos_wrapper)
        self.update_tipos_thread.start(60000)
        
        asyncio.create_task(self.update_tipos())
        
        self.setLayout(self.main_layout)
        
    def criar_consumiveis(self):  
        name = self.name_input.text()
        tipo = self.tipo_input.currentData()
        codigo = self.codigo_input.text()
        response = API_CreateConsumivel(name, codigo, tipo)          
            
        if response.success:
            Overlay.show_success(self, response.data)
            self.name_input.clear()
            self.codigo_input.clear()
            self.tipo_input.setCurrentIndex(0)
        else:
            Overlay.show_error(self, response.error_message)
        

    async def update_tipos(self):
        response = await API_GetAllTipoConsumiveis()
        if response.success:
            asyncio.create_task(self.create_tipos(response.data))
        else:
            Overlay.show_error(self, response.error_message)

    def create_tipos(self, tipos):
        if tipos != self.tipos:
            self.tipos = tipos
            self.tipo_input.clear()
            self.tipo_input.addItem("Selecione o Tipo", None)
            for tipo in tipos:
                self.tipo_input.addItem(tipo.nome_tipo, tipo.tipo_consumivel_id)

    def update_tipos_wrapper(self):
        asyncio.create_task(self.update_tipos())
