from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from APP.UI.ui_styles import Style
from API.API_POST_Request import API_CreateSetorHospitalar
from APP.Overlays.Overlay import Overlay


class CreateSetorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 30, 20, 30)

        # Título da página
        self.title = QLabel("Adicionar Setor Hospitalar")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(15)

        self.font_Label = QFont("Arial", 12)

        # Nome do setor
        self.name_label = QLabel("Nome do Setor")
        self.name_label.setFont(self.font_Label)
        self.name_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setFixedSize(500, 40)
        self.name_input.setPlaceholderText("Insira o nome do setor hospitalar")
        self.name_input.setStyleSheet(Style.style_QlineEdit)

        # Localização
        self.localizacao_label = QLabel("Localização")
        self.localizacao_label.setFont(self.font_Label)
        self.localizacao_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.localizacao_input = QLineEdit()
        self.localizacao_input.setFixedSize(500, 40)
        self.localizacao_input.setPlaceholderText("Insira a localização do setor hospitalar")
        self.localizacao_input.setStyleSheet(Style.style_QlineEdit)

        # Layout do formulário
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.addWidget(self.name_label)
        self.form_layout.addWidget(self.name_input)
        self.form_layout.addWidget(self.localizacao_label)
        self.form_layout.addWidget(self.localizacao_input)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addSpacing(20)

        # Botão de registro
        self.register_button = QPushButton("Criar")
        self.register_button.setFixedSize(150, 40)
        self.register_button.setStyleSheet(Style.style_bt_QPushButton)
        self.register_button.clicked.connect(self.criar_setor_hospitalar)
        self.main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def criar_setor_hospitalar(self):
        nome_setor = self.name_input.text()
        localizacao = self.localizacao_input.text()
        response = API_CreateSetorHospitalar(nome_setor, localizacao)
        if response.success:
            Overlay.show_success(self, response.data)
            self.name_input.clear()
            self.localizacao_input.clear()
        else:
            Overlay.show_error(self, response.error_message)

