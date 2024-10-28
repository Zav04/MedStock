
from app_modules import *
from pages.Dashboard.Layout_Dashboard import Dashboard
from pages.Login.Layout_Login import Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    sys.exit(app.exec_())
