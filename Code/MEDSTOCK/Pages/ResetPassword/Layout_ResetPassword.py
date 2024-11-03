# Layout_ResetPassword.py
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from APP.WindowFunctions import WindowFunctions
from pages.p_ResetPassword import ResetPasswordPage
from .Ui_ResetPassword import Ui_ResetPassword
from PyQt5.QtCore import Qt

class ResetPassword(QDialog):
    def __init__(self, parent):
        super(ResetPassword, self).__init__(parent)
        self.ui = Ui_ResetPassword()
        
        self.ui.setupUi(self)
        
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Redefinição de Palavra Passe - MedStock")
        self.setWindowIcon(QIcon("icons/MedStock/favicon.png"))
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        WindowFunctions.enableWindowDragging(self)
        
        self.page_reset_password = ResetPasswordPage(self)
        self.ui.content_layout.addWidget(self.page_reset_password)
        
        self.page_reset_password.email_sent.connect(self.parent().show_email_sent_overlay)
        
        self.ui.btn_close.clicked.connect(self.close)
