import random
import string
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from APP.Ui_Styles import Style
from API.API_GET_Request import API_GetRoles
from API.API_POST_Request import API_CreateUser, API_CreateUser_SendEmail
from Overlays.Overlay import Overlay



class CreateUserPage(QWidget):
    def __init__(self):
        super().__init__()
        DbRoles = API_GetRoles()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 30, 20, 30)

        title = QLabel("Criar Novo Utilizador")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        main_layout.addWidget(title)

        main_layout.addSpacing(15)

        name_label = QLabel("Nome")
        name_font = QFont("Arial", 12)
        name_label.setFont(name_font)
        name_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        name_input = QLineEdit()
        name_input.setFixedSize(300, 40)
        name_input.setPlaceholderText("Insira o nome")
        name_input.setStyleSheet(Style.style_QlineEdit)

        email_label = QLabel("Email")
        email_label.setFont(name_font)
        email_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        email_input = QLineEdit()
        email_input.setFixedSize(300, 40)
        email_input.setPlaceholderText("Insira o email")
        email_input.setStyleSheet(Style.style_QlineEdit)
        

        gender_label = QLabel("Genero")
        gender_label.setFont(name_font)
        gender_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        gender_input = QComboBox()
        gender_input.setFixedSize(300, 40)
        gender_input.addItem("Masculino", "M")
        gender_input.addItem("Feminino", "F")
        gender_input.setStyleSheet(Style.style_QComboBox)


        dob_label = QLabel("Data de Nascimento")
        dob_label.setFont(name_font)
        dob_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        dob_input = QDateEdit()
        dob_input.setFixedSize(300, 40)
        dob_input.setCalendarPopup(True)
        dob_input.setDate(QDate.currentDate())
        dob_input.setStyleSheet(Style.style_QDateEdit)


        role_label = QLabel("Cargo")
        role_label.setFont(name_font)
        role_label.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        role_input = QComboBox()
        role_input.setFixedSize(300, 40)
        
        if DbRoles.success==True:
             roles = DbRoles.data
             role_input.clear()
             for role in roles:
                role_input.addItem(role.nome_role, role.role_id)
        else:
            Overlay.show_error(self, DbRoles.error_message)
            
        role_input.setStyleSheet(Style.style_QComboBox)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(name_label)
        form_layout.addWidget(name_input)
        form_layout.addWidget(email_label)
        form_layout.addWidget(email_input)
        form_layout.addWidget(gender_label)
        form_layout.addWidget(gender_input)
        form_layout.addWidget(dob_label)
        form_layout.addWidget(dob_input)
        form_layout.addWidget(role_label)
        form_layout.addWidget(role_input)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        
        
        register_button = QPushButton("Registrar")
        register_button.setFixedSize(150, 40)
        register_button.setStyleSheet(Style.style_bt_QPushButton)
        register_button.clicked.connect(lambda: register_user(self,
            name_input.text(), email_input.text(), gender_input.currentData(), dob_input.date().toString("dd-MM-yyyy"), role_input.currentData()
        ))

        main_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        
        def register_user(self, name, email, gender, dob, role):            
            password=password_generator()
            response= API_CreateUser(name, email, password , gender, dob, role)
            if(response.success==True):
                Overlay.show_success(self, response.data)
                name_input.clear()
                email_input.clear()
                response=API_CreateUser_SendEmail(email,password)
                if(response.success==True):
                    Overlay.show_information(self, response.data)
                else:
                    Overlay.show_error(self, response.error_message)
            else:
                Overlay.show_error(self, response.error_message)




def password_generator():
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?/")
    remaining = random.choices(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/", k=5)
    senha = list(upper + digit + special + ''.join(remaining))
    random.shuffle(senha)
        
    return ''.join(senha)








