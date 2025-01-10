from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,QAction
from PyQt5.QtCore import Qt,pyqtSignal
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from API.API_POST_Request import API_ResetPassword


class ResetPasswordPage(QDialog):
    email_sent = pyqtSignal()
    def __init__(self,dialog):
        super().__init__()
        self.dialog = dialog

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Digite o seu email para redefinir a palavra-passe:")
        label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: rgb(0, 0, 0);
            """)
        layout.addWidget(label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedSize(450, 40)
        self.email_input.setStyleSheet(Style.style_QlineEdit)

        layout.addWidget(self.email_input)

        send_button = QPushButton("Enviar", self)
        send_button.setFixedSize(150, 40)
        send_button.setStyleSheet(Style.style_bt_QPushButton)
        send_button.clicked.connect(self.send_reset_password)
        layout.addWidget(send_button, alignment=Qt.AlignCenter)

    def send_reset_password(self):
        email = self.email_input.text()
        response= API_ResetPassword(email)
        if(response.success==False):
            Overlay.show_error(self, response.error_message)
        else:
            self.email_sent.emit()
            self.dialog.close()
