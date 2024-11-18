import sys
from Pages.Dashboard.Layout_Dashboard import Dashboard
from Pages.Login.Layout_Login import Login
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
import logging

#TODO JUST FOR TESTING
from Class.utilizador import Utilizador
#TODO JUST FOR TESTING

if __name__ == "__main__":
    load_dotenv()
    logging.getLogger("requests").disabled = True
    logging.getLogger("matplotlib").disabled = True 
    logging.getLogger("urllib3").disabled = True
    app = QApplication(sys.argv)
    # #TODO JUST FOR TESTING
    user = Utilizador(nome="Bruno Oliveira Rafael", email="Bruno.bx04@gmail.com", 
                    sexo="M", data_nascimento="1999-06-06", utilizador_id=12, role_id=1, role_nome="Administrador")
    # #TODO JUST FOR TESTING
    window = Dashboard(user=user)
    sys.exit(app.exec_())
