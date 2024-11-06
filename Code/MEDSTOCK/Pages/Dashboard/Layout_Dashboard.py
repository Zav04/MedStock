
from PyQt5.QtWidgets import *
from Pages.p_Home import HomePage
from APP.WindowFunctions import WindowFunctions
from Overlays.Overlay import Overlay
from Pages.Dashboard.ui_dashboard import Ui_MainWindow
from APP.ui_functions import UIFunctions
from Pages.Login.Layout_Login import Login
from Pages.p_Add_user import CreateUserPage
from Pages.p_Itens import ItemTablePage


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self, self.ui.frame_top)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))
        self.initPages()
        self.initMenus()
        self.show()


    def initPages(self):

        self.page_home = HomePage()
        self.page_add_user = CreateUserPage()
        self.page_stock = ItemTablePage()
        self.ui.stackedWidget.addWidget(self.page_home)
        self.ui.stackedWidget.addWidget(self.page_add_user)
        self.ui.stackedWidget.addWidget(self.page_stock)
        
        self.ui.stackedWidget.setCurrentWidget(self.page_home)
    
    #TODO VERIFICAR ISTO DE FORMA DINAMICA
    def initMenus(self):
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "CRIAR NOVO UTILIZADOR", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
        UIFunctions.addNewMenu(self, "ITENS STOCK", "btn_stock", "url(:/16x16/icons/16x16/cil-notes.png)", True)
        UIFunctions.addNewMenu(self, "LOG OUT", "btn_log_out", "url(:/16x16/icons/16x16/cil-account-logout.png)", False)
        UIFunctions.selectStandardMenu(self, "btn_home", UIFunctions.labelPage)
        self.ui.stackedWidget.setMinimumWidth(20)

        #TODO VERIFICAR ISTO DE FORMA DINAMICA
        UIFunctions.userIcon(self, "BO")


    def Button(self):
        btnWidget = self.sender()
        if not btnWidget:
            return



        #TODO Todas as Paginas
        #HOME com estatisticas - Todos
        #Criar novo utilizador - So admin
        #Pedido de Material - Medicos, Enfermeriros, Assistentes e Secretarios Clinicos
            #Lista de material que se pode escolher, ver como fazer isto, o mais complexo
        #Aceitar pedidos Material - Gestor das Alas
        #Validar pedidos e enviar- Farmaceuticos
        #Tabela a mostrar Quantidade de Itens existentes - Farmaceuticos
        #Se der tempo fazer graficos de tempo de demora, tempo de aceitação
        
        
        page_map = {
            "btn_home": (self.page_home, "Home"),
            "btn_new_user": (self.page_add_user, "Novo Utilizador"),
            "btn_stock": (self.page_stock, "Stock"),
            "btn_log_out": None
        }
        
        if btnWidget.objectName() == "btn_log_out":
            self.logout()
            return

        page_info = page_map.get(btnWidget.objectName())
        if page_info:
            page_widget, page_title = page_info
            
            self.ui.stackedWidget.setCurrentWidget(page_widget)
            UIFunctions.resetStyle(self, btnWidget.objectName())
            UIFunctions.labelPage(self, page_title)
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            
            
    def logout(self):
        self.close()
        self.login_window = Login()
        self.login_window.show()
