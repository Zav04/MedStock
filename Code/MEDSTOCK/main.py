
from app_modules import *


class Dashboard(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('MedStock')
        UIFunctions.labelTitle(self, 'MedStock')
        self.setWindowIcon(QIcon("icons/MedStock/favicon.png"))
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################
        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 400, True))
        ## ==> END ##

        # Inicializar as Páginas
        self.initPages()

        # Inicializar o Menu
        self.initMenus()

        # Exibir a janela principal
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

        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)
                
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

        self.show()

    def Button(self):
        btnWidget = self.sender()
        if not btnWidget:
            return

        page_map = {
            "btn_home": (self.page_home, "Home"),
            # "btn_new_user": (self.page_add_user, "New User"),
            # "btn_widgets": (self.page_widgets, "Custom Widgets")
        }

        # Recupere a página e o título com base no objectName do botão
        page_info = page_map.get(btnWidget.objectName())
        if page_info:
            page_widget, page_title = page_info
            
            self.ui.stackedWidget.setCurrentWidget(page_widget)

            UIFunctions.resetStyle(self, btnWidget.objectName())
            UIFunctions.labelPage(self, page_title)
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


    def resizeEvent(self, event):
        return super(Dashboard, self).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = Dashboard()
    sys.exit(app.exec_())
