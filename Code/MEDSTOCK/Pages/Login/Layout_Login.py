from PyQt5.QtWidgets import QMainWindow
from APP.UI.WindowFunctions import WindowFunctions
from Pages.p_Login import LoginPage
from .Ui_Login import Ui_Login


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self, self.ui.frame_top)
        
        self.page_login = LoginPage(self)
        self.ui.content_layout.addWidget(self.page_login)
        
        self.show()
