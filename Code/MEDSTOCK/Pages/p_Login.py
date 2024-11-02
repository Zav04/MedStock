from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QAction
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
import os
from APP.Ui_Styles import Style
from Overlays.Overlay import Overlay
from API.API_POST_Request import API_Login
from pages.Dashboard.Layout_Dashboard import Dashboard



def login_button_clicked(email_input, password_input,central_page,full_page):
    email = email_input.text()
    password = password_input.text()
    response= API_Login(email, password)
    if(response.success):
        full_page.close()
        dashboard = Dashboard()
        dashboard.show()
        Overlay.show_success(central_page, "Login Bem-Sucedido")
    else:
        Overlay.show_error(central_page, response.error_message)


def reset_password_button_clicked():
    print("Redefinir Palavra-Passe")

def recolor_icon(path, color):
    pixmap = QPixmap(path)
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(QColor(color))
    colored_pixmap.setMask(pixmap.mask())
    return QIcon(colored_pixmap)

class LoginPage(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.main_window = mainwindow
        
        self.is_password_visible = False
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(10, 30, 10, 30)

        icon_path = os.path.abspath("./icons/MedStock/Superior/PNG/Expand.png")
        img_login = QLabel(self)
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(QSize(1500, 450), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_login.setPixmap(pixmap)
        img_login.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(img_login)

        main_layout.addSpacing(20)

        email_input = QLineEdit(self)
        email_input.setPlaceholderText("Email")
        email_input.setFixedSize(500, 60)
        email_input.setStyleSheet(Style.style_QlineEdit)
        main_layout.addWidget(email_input)

        main_layout.addSpacing(15)

        password_input = QLineEdit(self)
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setFixedSize(500, 60)
        password_input.setStyleSheet(Style.style_QlineEdit)

        self.original_icon = QIcon("./icons/MaterialIcons/visibility_off.png")
        self.colored_icon = recolor_icon("./icons/MaterialIcons/visibility_off.png", "#4CAF50")
        self.visible_icon = recolor_icon("./icons/MaterialIcons/visibility.png", "#4CAF50")

        self.toggle_action = QAction(self.original_icon, "", self)
        self.toggle_action.triggered.connect(lambda: self.toggle_password_visibility(password_input))
        password_input.addAction(self.toggle_action, QLineEdit.TrailingPosition)

        password_input.focusInEvent = self.create_focus_event(password_input, True)
        password_input.focusOutEvent = self.create_focus_event(password_input, False)

        main_layout.addWidget(password_input)

        main_layout.addSpacing(20)
        login_button = QPushButton("Login", self)
        login_button.setFixedSize(200, 60)
        login_button.setStyleSheet(Style.style_bt_QPushButton)
        login_button.clicked.connect(lambda: login_button_clicked(email_input, password_input,self.parent(), mainwindow))
        main_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        main_layout.addSpacing(15)

        reset_password_text = QPushButton("Esqueci-me da Palavra-Passe", self)
        reset_password_text.clicked.connect(reset_password_button_clicked)
        reset_password_text.setStyleSheet(Style.style_bt_TextEdit)
        main_layout.addWidget(reset_password_text, alignment=Qt.AlignCenter)
        

        self.setLayout(main_layout)

    def toggle_password_visibility(self, password_input):
        self.is_password_visible = not self.is_password_visible
        if self.is_password_visible:
            password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_action.setIcon(self.visible_icon)
        else:
            password_input.setEchoMode(QLineEdit.Password)
            self.toggle_action.setIcon(self.colored_icon if password_input.hasFocus() else self.original_icon)

    def create_focus_event(self, password_input, focus_in):
        def event(event):
            if focus_in:
                icon = self.visible_icon if self.is_password_visible else self.colored_icon
                self.toggle_action.setIcon(icon)
            else:
                icon = self.visible_icon if self.is_password_visible else self.original_icon
                self.toggle_action.setIcon(icon)
            QLineEdit.focusInEvent(password_input, event) if focus_in else QLineEdit.focusOutEvent(password_input, event)
        return event
