from PyQt5.QtWidgets import QMainWindow
from APP.WindowFunctions import WindowFunctions
from pages.p_Login import LoginPage
from .Ui_Login import Ui_Login


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

        # Inicializar as propriedades da janela
        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self)
        
        # Criar a página de login e adicioná-la ao layout de frame_content
        self.page_login = LoginPage(self)
        self.ui.content_layout.addWidget(self.page_login)  # Adicionar ao layout de frame_content
        
        self.show()
