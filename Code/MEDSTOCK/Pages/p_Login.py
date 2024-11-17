from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from APP.UI.ui_functions import UIFunctions
import os
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from API.API_POST_Request import API_Login
from Pages.ResetPassword.Layout_ResetPassword import ResetPassword

def login_button_clicked(email_input, password_input, central_page, full_page):
    from Pages.Dashboard.Layout_Dashboard import Dashboard
    email = email_input.text()
    password = password_input.text()
    response = API_Login(email, password)
    if response.success:
        full_page.close()
        dashboard = Dashboard()
        dashboard.show()
        Overlay.show_success(central_page, "Login Bem-Sucedido")
    else:
        Overlay.show_error(central_page, response.error_message)

class LoginPage(QWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.main_window = mainwindow
        self.is_password_visible = False
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(10, 30, 10, 30)


        icon_path_visibility_off = "./icons/MaterialIcons/visibility_off.png"
        icon_path_visibility_on = "./icons/MaterialIcons/visibility.png"
        

        self.original_icon = QIcon(icon_path_visibility_off)
        self.recolored_icon = QIcon(UIFunctions.recolor_icon(icon_path_visibility_off, "#4CAF50"))
        self.visible_icon = QIcon(UIFunctions.recolor_icon(icon_path_visibility_on, "#4CAF50"))


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


        self.toggle_action = QAction(self.original_icon, "", self)
        password_input.addAction(self.toggle_action, QLineEdit.TrailingPosition)


        password_input.focusInEvent = self.create_focus_event(password_input, True)
        password_input.focusOutEvent = self.create_focus_event(password_input, False)


        self.toggle_action.triggered.connect(lambda: self.toggle_password_visibility(password_input))

        main_layout.addWidget(password_input)

        main_layout.addSpacing(20)
        login_button = QPushButton("Login", self)
        login_button.setFixedSize(200, 60)
        login_button.setStyleSheet(Style.style_bt_QPushButton)

        main_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        main_layout.addSpacing(15)


        reset_password_text = QPushButton("Esqueci-me da Palavra-Passe", self)
        reset_password_text.setStyleSheet(Style.style_bt_TextEdit)
        main_layout.addWidget(reset_password_text, alignment=Qt.AlignCenter)
        

        reset_password_text.clicked.connect(self.open_reset_password_dialog)
        login_button.clicked.connect(lambda: login_button_clicked(email_input, password_input, self.parent(), mainwindow))
        email_input.returnPressed.connect(lambda: self.check_and_login(email_input, password_input, login_button))
        password_input.returnPressed.connect(lambda: self.check_and_login(email_input, password_input, login_button))

        self.setLayout(main_layout)

    def show_email_sent_overlay(self):
        Overlay.show_success(self, "E-mail de redefinição de palavra-passe enviado com sucesso")

    def open_reset_password_dialog(self):
        dialog = ResetPassword(self)
        dialog.exec_()

    def toggle_password_visibility(self, password_input):
        """Alterna a visibilidade da senha e ajusta o ícone de acordo."""
        self.is_password_visible = not self.is_password_visible
        if self.is_password_visible:
            password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_action.setIcon(self.visible_icon)
        else:
            password_input.setEchoMode(QLineEdit.Password)
            self.toggle_action.setIcon(self.recolored_icon if password_input.hasFocus() else self.original_icon)

    def create_focus_event(self, password_input, focus_in):
        """Define o ícone de visibilidade correto ao ganhar/perder foco."""
        def event(event):
            if focus_in:
                icon = self.recolored_icon if not self.is_password_visible else self.visible_icon
                self.toggle_action.setIcon(icon)
            else:
                icon = self.original_icon if not self.is_password_visible else self.visible_icon
                self.toggle_action.setIcon(icon)
            QLineEdit.focusInEvent(password_input, event) if focus_in else QLineEdit.focusOutEvent(password_input, event)
        return event

    def check_and_login(self, email_input, password_input, login_button):
        if email_input.text() and password_input.text():
            login_button.click()
