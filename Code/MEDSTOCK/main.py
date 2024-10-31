import sys
from pages.Dashboard.Layout_Dashboard import Dashboard
from pages.Login.Layout_Login import Login
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
import logging

if __name__ == "__main__":
    load_dotenv()
    logging.getLogger("requests").disabled = True
    logging.getLogger("matplotlib").disabled = True 
    logging.getLogger("urllib3").disabled = True
    app = QApplication(sys.argv)
    window = Dashboard()
    sys.exit(app.exec_())
