import random
import string
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from APP.ui_styles import Style
from API.API_GET_Request import API_GetRoles
from API.API_POST_Request import API_CreateUser, API_CreateUser_SendEmail
from Overlays.Overlay import Overlay
import asyncio



class CreateUserPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 30, 20, 30)

        self.title = QLabel("Criar Novo Utilizador")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.main_layout.addWidget(self.title)

        self.main_layout.addSpacing(15)

        self.name_label = QLabel("Nome")
        self.name_font = QFont("Arial", 12)
        self.name_label.setFont(self.name_font)
        self.name_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setFixedSize(500, 40)
        self.name_input.setPlaceholderText("Insira o nome")
        self.name_input.setStyleSheet(Style.style_QlineEdit)

        self.email_label = QLabel("Email")
        self.email_label.setFont(self.name_font)
        self.email_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.email_input = QLineEdit()
        self.email_input.setFixedSize(500, 40)
        self.email_input.setPlaceholderText("Insira o email")
        self.email_input.setStyleSheet(Style.style_QlineEdit)
        

        self.gender_label = QLabel("Genero")
        self.gender_label.setFont(self.name_font)
        self.gender_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.gender_input = QComboBox()
        self.gender_input.setFixedSize(500, 40)
        self.gender_input.addItem("Masculino", "M")
        self.gender_input.addItem("Feminino", "F")
        self.gender_input.setStyleSheet(Style.style_QComboBox)


        self.dob_label = QLabel("Data de Nascimento")
        self.dob_label.setFont(self.name_font)
        self.dob_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.dob_input = QDateEdit()
        self.dob_input.setFixedSize(500, 40)
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        self.dob_input.setStyleSheet(Style.style_QDateEdit)


        self.role_label = QLabel("Cargo")
        self.role_label.setFont(self.name_font)
        self.role_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        self.role_input = QComboBox()
        self.role_input.setFixedSize(500, 40)
        
        self.role_input.setStyleSheet(Style.style_QComboBox)
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.addWidget(self.name_label)
        self.form_layout.addWidget(self.name_input)
        self.form_layout.addWidget(self.email_label)
        self.form_layout.addWidget(self.email_input)
        self.form_layout.addWidget(self.gender_label)
        self.form_layout.addWidget(self.gender_input)
        self.form_layout.addWidget(self.dob_label)
        self.form_layout.addWidget(self.dob_input)
        self.form_layout.addWidget(self.role_label)
        self.form_layout.addWidget(self.role_input)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addSpacing(20)
        
        
        self.register_button = QPushButton("Registrar")
        self.register_button.setFixedSize(150, 40)
        self.register_button.setStyleSheet(Style.style_bt_QPushButton)
        self.register_button.clicked.connect(lambda: self.register_user(
            self.name_input.text(), self.email_input.text(), self.gender_input.currentData(), self.dob_input.date().toString("dd-MM-yyyy"), 
            self.role_input.currentData()
        ))
        
        asyncio.run(self.update_role())
        self.main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        self.setLayout(self.main_layout)
        
    def register_user(self, name, email, gender, dob, role):            
        password=password_generator()
        response= API_CreateUser(name, email, password , gender, dob, role)
        if(response.success==True):
            Overlay.show_success(self, response.data)
            self.name_input.clear()
            self.email_input.clear()
            response=API_CreateUser_SendEmail(email,password)
            if(response.success==True):
                Overlay.show_information(self, response.data)
            else:
                Overlay.show_error(self, response.error_message)
        else:
            Overlay.show_error(self, response.error_message)
    async def update_role(self):
        DbRoles = await API_GetRoles()
        if DbRoles.success==True:
            roles = DbRoles.data
            self.role_input.clear()
            for role in roles:
                self.role_input.addItem(role.nome_role, role.role_id)
        else:
            Overlay.show_error(self, DbRoles.error_message)




def password_generator():
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?/")
    remaining = random.choices(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/", k=5)
    pw = list(upper + digit + special + ''.join(remaining))
    random.shuffle(pw)
        
    return ''.join(pw)








