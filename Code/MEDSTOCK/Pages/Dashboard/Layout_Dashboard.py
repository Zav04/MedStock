
from app_modules import *
from PySide2.QtWidgets import *
from pages.p_Home import HomePage
from APP.WindowFunctions import WindowFunctions


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))

        self.initPages()
        self.initMenus()
        self.show()


    def initPages(self):

        self.page_home = HomePage()
        
        self.ui.stackedWidget.addWidget(self.page_home)
        self.ui.stackedWidget.setCurrentWidget(self.page_home)
    
    #TODO VERIFICAR ISTO DE FORMA DINAMICA
    def initMenus(self):
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "CRIAR NOVO UTILIZADOR", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
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
            # "btn_new_user": (self.page_add_user, "New User"),
            # "btn_widgets": (self.page_widgets, "Custom Widgets")
        }

        page_info = page_map.get(btnWidget.objectName())
        if page_info:
            page_widget, page_title = page_info
            
            self.ui.stackedWidget.setCurrentWidget(page_widget)

            UIFunctions.resetStyle(self, btnWidget.objectName())
            UIFunctions.labelPage(self, page_title)
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
