
from PyQt5.QtWidgets import *
from Pages.p_Home import HomePage
from APP.UI.WindowFunctions import WindowFunctions
from APP.Overlays.Overlay import Overlay
from Pages.Dashboard.ui_dashboard import Ui_MainWindow
from APP.UI.ui_functions import UIFunctions
from Class.Utilizador import Utilizador
from Pages.Login.Layout_Login import Login
from Pages.p_Add_user import CreateUserPage
from Pages.p_Itens import ItemTablePage
from Pages.p_Requerimento import RequerimentoPage
from Pages.p_Add_Consumiveis import CreateConsumivelPage
from Pages.p_Add_Setor import CreateSetorPage
from Pages.p_Gestor_Setor import AssociateUserToSectorPage


class Dashboard(QMainWindow):
    def __init__(self, user: Utilizador):
        super(Dashboard, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user
        WindowFunctions.removeTitleBar(self, True)
        WindowFunctions.setupWindow(self, 'MedStock', "icons/MedStock/favicon.png")
        WindowFunctions.enableWindowDragging(self, self.ui.frame_top)
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))
        
        self.userIconName(user.nome)
        self.initPages()
        self.initMenus(role=user.role_nome)
        self.show()

    def userIconName(self,name:str):
        words = name.strip().split()
        
        if len(words) == 1:
            single_word = words[0]
            formatted_string = (single_word[0] + single_word[-1]).upper()
        else:
            first_word = words[0]
            last_word = words[-1]
            formatted_string = (first_word[0] + last_word[0]).upper()
        UIFunctions.userIcon(self, formatted_string)

    def initPages(self):
        self.page_home = HomePage()
        self.page_add_user = CreateUserPage()
        self.page_add_consumivel = CreateConsumivelPage()
        self.page_add_setor_hospitalar = CreateSetorPage()
        self.page_gestor_setor = AssociateUserToSectorPage()
        self.page_stock = ItemTablePage()
        self.page_requerimento = RequerimentoPage(self.user)
        self.ui.stackedWidget.addWidget(self.page_home)
        self.ui.stackedWidget.addWidget(self.page_add_user)
        self.ui.stackedWidget.addWidget(self.page_add_consumivel)
        self.ui.stackedWidget.addWidget(self.page_add_setor_hospitalar)
        self.ui.stackedWidget.addWidget(self.page_gestor_setor)
        self.ui.stackedWidget.addWidget(self.page_stock)
        self.ui.stackedWidget.addWidget(self.page_requerimento)
        self.ui.stackedWidget.setCurrentWidget(self.page_home)
        
    
    #TODO VERIFICAR ISTO DE FORMA DINAMICA
    def initMenus(self, role: str):
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/20x20/icons/20x20/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "LOG OUT", "btn_log_out", "url(:/16x16/icons/16x16/cil-account-logout.png)", False)
        UIFunctions.selectStandardMenu(self, "btn_home", UIFunctions.labelPage)
        
        #TODO Todas as Paginas
        #HOME com estatisticas - Todos
        #Criar novo utilizador - So admin
        #Pedido de Material - Medicos, Enfermeriros, Assistentes e Secretarios Clinicos
            #Lista de material que se pode escolher, ver como fazer isto, o mais complexo
        #Aceitar pedidos Material - Gestor das Alas
        #Validar pedidos e enviar- Farmaceuticos
        #Tabela a mostrar Quantidade de Itens existentes - Farmaceuticos
        #Se der tempo fazer graficos de tempo de demora, tempo de aceitação
        

        if role == "Administrador":
            #Falta Associar Utilizadores a Alas Hospitalares
            UIFunctions.addNewMenu(self, "CRIAR NOVO UTILIZADOR", "btn_new_user", "url(:/20x20/icons/20x20/cil-user-follow.png)", True)
            UIFunctions.addNewMenu(self, "CRIAR NOVO CONSUMIVEL", "btn_new_consumivel", "url(:/20x20/icons/20x20/pill.png)", True)
            UIFunctions.addNewMenu(self, "CRIAR NOVA ALA HOSPITALAR", "btn_new_setor", "url(:/20x20/icons/20x20/hospital.png)", True)
            UIFunctions.addNewMenu(self, "GESTOR DE ALA HOSPITALAR", "btn_gestor_setor", "url(:/20x20/icons/20x20/manage_accounts.png)", True)
            UIFunctions.addNewMenu(self, "ITENS STOCK", "btn_stock", "url(:/20x20/icons/20x20/cil-notes.png)", True)
            UIFunctions.addNewMenu(self, "REQUERIMENTOS", "btn_requerimento", "url(:/20x20/icons/20x20/cil-description.png)", True)
        elif role == "Gestor Responsável":
            UIFunctions.addNewMenu(self, "REQUERIMENTOS", "btn_requerimento", "url(:/20x20/icons/20x20/cil-description.png)", True)
        elif role == "Farmacêutico":
            UIFunctions.addNewMenu(self, "ITENS STOCK", "btn_stock", "url(:/20x20/icons/20x20/cil-notes.png)", True)
            UIFunctions.addNewMenu(self, "REQUERIMENTOS", "btn_requerimento", "url(:/20x20/icons/20x20/cil-description.png)", True)
        else:
            UIFunctions.addNewMenu(self, "REQUERIMENTOS", "btn_requerimento", "url(:/20x20/icons/20x20/cil-description.png)", True)
        self.ui.stackedWidget.setMinimumWidth(20)


    def Button(self):
        btnWidget = self.sender()
        if not btnWidget:
            return        
        
        page_map = {
            "btn_home": (self.page_home, "Home"),
            "btn_new_user": (self.page_add_user, "Novo Utilizador"),
            "btn_new_consumivel": (self.page_add_consumivel, "Novo Consumivel"),
            "btn_new_setor": (self.page_add_setor_hospitalar, "Nova Ala Hospitalar"),
            "btn_gestor_setor": (self.page_gestor_setor, "Gestor de Setor"),
            "btn_stock": (self.page_stock, "Stock"),
            "btn_requerimento": (self.page_requerimento, "Requerimento"),
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
