
from PyQt5.QtWidgets import *
from pages.p_Home import HomePage
from APP.WindowFunctions import WindowFunctions
from Overlays.Overlay import Overlay
from pages.Dashboard.Ui_Dashboard import Ui_MainWindow
from APP.Ui_Functions import UIFunctions
from pages.Login.Layout_Login import Login


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))

        self.initPages()
        self.initMenus()
        self.show()


    def initPages(self):

        self.page_home = HomePage()
        self.page_add_user = HomePage()
        self.ui.stackedWidget.addWidget(self.page_home)
        self.ui.stackedWidget.addWidget(self.page_add_user)
        self.ui.stackedWidget.setCurrentWidget(self.page_home)
    
    #TODO VERIFICAR ISTO DE FORMA DINAMICA
    def initMenus(self):
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "CRIAR NOVO UTILIZADOR", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
        UIFunctions.addNewMenu(self, "LOG OUT", "btn_log_out", "url(:/16x16/icons/16x16/cil-account-logout.png)", False)
        UIFunctions.selectStandardMenu(self, "btn_home", UIFunctions.labelPage)
        self.ui.stackedWidget.setMinimumWidth(20)

        #TODO VERIFICAR ISTO DE FORMA DINAMICA
        UIFunctions.userIcon(self, "BO")


    def Button(self):
        btnWidget = self.sender()
        if not btnWidget:
            return

        page_map = {
            "btn_home": (self.page_home, "Home"),
            "btn_new_user": (self.page_add_user, "New User"),
            "btn_log_out": None
        }
        
        if btnWidget.objectName() == "btn_log_out":
            self.logout()
            return

        page_info = page_map.get(btnWidget.objectName())
        if page_info:
            page_widget, page_title = page_info
            
            self.ui.stackedWidget.setCurrentWidget(page_widget)
            Overlay.show_success(self.ui.stackedWidget, "Login Bem-Sucedido")
            Overlay.show_warning(self.ui.stackedWidget, "Login Bem-Sucedido")
            Overlay.show_error(self.ui.stackedWidget, "Login Bem-Sucedido")
            Overlay.show_information(self.ui.stackedWidget, "Login Bem-Sucedido")
            UIFunctions.resetStyle(self, btnWidget.objectName())
            UIFunctions.labelPage(self, page_title)
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            
            
    def logout(self):
        self.close()
        self.login_window = Login()
        self.login_window.show()
